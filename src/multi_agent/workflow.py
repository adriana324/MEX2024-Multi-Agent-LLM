from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from utils import write_sol_to_file, get_generated_code
from multi_agent.execute_code import CodeExecution
from functools import partial
from subprocess import TimeoutExpired
from requests.exceptions import ConnectionError, Timeout
import regex as re
from utils import *


class Workflow():

    """ The Workflow class contains functions needed to setup the multi-agent workflow. """

    class GraphState(TypedDict):
        """
        Represents the state of our graph. 
        """
        problem: str        #The given problem
        problem_id:str      #The problem id
        code:str            #The generated code.
        tests:str           #The generated test cases.
        exec_msg:str        #The latest execution message.
        num_steps:int       #The number of steps taken.
        num_loops:int       #The number of times it has looped between execution and debugger
        initial_code: str   #The first generated code (before debugging). 


    @staticmethod
    def programmer(state:GraphState, programmer_agent):
        """Programmer node - used to generate code"""
        print("----GENERATE CODE----")
        num_steps = int(state['num_steps'])
        num_steps += 1
        problem = state['problem']

        response = programmer_agent.invoke({"problem":problem})
        code = get_generated_code(response)

        print(response) #Test
        print("Stored code")
        print(code) #Test

        return {"code":code, "initial_code":code, "num_steps":num_steps}

    @staticmethod
    def tester(state:GraphState, tester_agent):
        """Tester node - generate tests for the provided code"""
        print("----GENERATE TESTS----")
        problem = state['problem']
        code = state['code']
        num_steps = int(state['num_steps'])
        num_steps += 1

        response = tester_agent.invoke({"problem":problem, "code": code})
        print(response) #Test

        tests = get_generated_code(response)
        
        print("Stored tests")
        print(tests) #Test

        return {"tests":tests, "num_steps":num_steps}

    @staticmethod
    def debugger(state:GraphState, debugger_agent):
        """Debugger node - used to debug the provided code"""
        print("----DEBUG CODE----")
        error = state['exec_msg']
        num_steps = int(state['num_steps'])
        num_steps += 1
        num_loops = int(state['num_loops'])
        num_loops += 1
        code = state["code"]
        tests = state['tests']
        problem = state['problem']

        tries = 0
        while tries < 2:
            try:
                response = debugger_agent.invoke({"code":code, "error": error, "problem": problem,"tests":tests}) 
                extracted_code = get_generated_code(response)
                break
            except Exception as e:
                print(f"{e} occurred, with debugger. Retrying...")
                print(response) #Test

                extracted_code = code #Keep old code if debugger can't generate new code. 
                tries += 1

        print(response) #Test
        print("Stored debugged code")
        print(extracted_code) #Test

        return {"code":extracted_code, "num_steps":num_steps, "num_loops":num_loops}

    @staticmethod
    def code_executer(state:GraphState, docker:bool):
        """Executor node - combines the code and test cases and executes it as one codeblock."""
        print("----Execute code----")
        code = state['code']
        tests = state['tests']
        codeblock = CodeExecution.combine_two_codeblocks(code,tests)
        
        result = CodeExecution.exec_python_codeblock(codeblock, docker=docker)
        num_steps = int(state['num_steps'])
        num_steps += 1

        print(result) #Test
        
        return {"exec_msg":result, "num_steps":num_steps}


    @staticmethod
    def check_execution(state:GraphState, max_loops:int):
        """Conditional edge - used to check the execution message and decides the route"""
        print("----Decide if debugging is needed----")
        exec_msg = state['exec_msg']
        num_loops = state['num_loops'] #Get how many times it code has been debugged

        #Check if execution message is of type bytes to decode it.
        if isinstance(exec_msg, bytes):
            decoded_exec_msg = exec_msg.decode()
        else:
            decoded_exec_msg = exec_msg

        #Conditional logic
        if num_loops >= max_loops:
            return "max loops reached"
        elif isinstance(decoded_exec_msg, TimeoutExpired):
            print("TimeoutExpired , execution timed out after 30 seconds")
            return "error"
        elif isinstance(decoded_exec_msg, Timeout) or isinstance(decoded_exec_msg, ConnectionError):
            print("ConnectionError, Docker execution timed out")
            return "error"
        elif "Traceback " in decoded_exec_msg or 'SyntaxError' in decoded_exec_msg or 'Error' in decoded_exec_msg :
            print("Error \n" + decoded_exec_msg)
            return "error"
        else:
            print("Passed all tests")
            return "sucessfull"

    @staticmethod
    def assistant(state:GraphState, filename:str, store_as_jsonl:bool):
        """Assistant node - saves the final version of the code"""
        print("---- END ----")
        problem_id = state['problem_id']
        code = state['code']
        initial_code = state['initial_code']

        print("Initial code")
        print(initial_code)
        print("Final code")
        print(code)

        if store_as_jsonl:
            #Fromat
            final_code = refactor_code(codeblock=code, both_parts=True)
            initial_code = refactor_code(codeblock=initial_code, both_parts=True)

            #Save solution to files (as jsonl)
            write_sol_to_file(file_name=filename, final_solution=final_code, initial_solution=initial_code, id=problem_id) #multi-agent

        num_steps = int(state['num_steps'])
        num_steps += 1
        return {"code":final_code, "num_steps":num_steps}

    #Util
    @staticmethod
    def _state_printer(state:GraphState):
        """print the state"""
        print("---STATE PRINTER---")
        print(f"Problem: {state['problem']} \n")
        print(f"Final code: {state['code']} \n")
        print(f"Execution message: {state['exec_msg']} \n")
        print(f"No. steps: {state['num_steps']} \n")
        print(f"No. loops: {state['num_loops']} \n")


    #--------------------Build Graph--------------------
    @staticmethod
    def setup_workflow(programmer_agent, tester_agent,debugger_agent, filename:str = "", max_loops:int = 5, docker:bool = True, store_as_jsonl:bool = True):
        """Sets up the workflow of the multi_agent system"""
        workflow = StateGraph(Workflow.GraphState)

        #Partial functions (used to fix some arguments) 
        tester_func = partial(Workflow.tester,tester_agent=tester_agent)
        debugger_func = partial(Workflow.debugger,debugger_agent=debugger_agent)
        assistant_func = partial(Workflow.assistant, filename=filename, store_as_jsonl=store_as_jsonl)
        check_execution_func = partial(Workflow.check_execution,max_loops=max_loops)
        code_executer_func = partial(Workflow.code_executer, docker=docker)
        programmer_func = partial(Workflow.programmer,programmer_agent=programmer_agent)


        #Define the nodes 
        workflow.add_node("tester", tester_func)
        workflow.add_node("debugger", debugger_func)
        workflow.add_node("code_executor", code_executer_func)
        workflow.add_node("assistant", assistant_func)
        workflow.add_node("programmer", programmer_func)

        #Set entry point for the graph
        workflow.set_entry_point("programmer") 

        #Add edges Controll the flow
        workflow.add_edge("programmer","tester")
        workflow.add_edge("tester","code_executor")

        #Conditional edge - go from tester to execution conditional edge. Choses if it goes to debugger or end.  
        workflow.add_conditional_edges(
            "code_executor",
            check_execution_func,
            {
                "error": "debugger", #If code_executor returns "Error", then go to debugger node
                "sucessfull": "assistant", #If code_executor returns "Sucessfull", then go to final node 
                "max loops reached":"assistant" #If we have looped too many times, save the final version.
            }
        )

        workflow.add_edge("debugger","code_executor")
        workflow.add_edge("assistant",END)

        return workflow


