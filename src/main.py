from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os 
from langchain_openai import ChatOpenAI
from multi_agent.agents import Agents
from multi_agent.workflow import Workflow
from datasets import load_dataset
from utils import *

#Set up environment 
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LANGCHAIN API KEY'] = os.getenv('LANGCHAIN_API_KEY')

#Set up LLM parameters 
TEMPERATURE = 0.1 #Value given in Llama research paper (code generation).
TOP_P = 0.95      #Value given in Llama research paper (code generation).
LLAMA_MODEL = "llama3-70b-8192"
FILENAME = "test.jsonl" #Name of the jsonl file to store solutions
DATASET_NAME = 'humaneval' #Dataset to be used for the experiment. Set to humaneval | apps | kattis
NO_TASKS = 40           #No. tasks to try 
DIFFICULTY = "easy"   #Difficulty lvl of the tasks. APPS: 'introductory' || 'interview' || 'competition'. Kattis|HumanEval: 'easy' | 'medium' | 'hard'.
DOCKER = True           #Set if Docker should be used when executing the generated code.
PROMPTING_TECH = "zero-shot" #Set the prompting techinque that should be used (zero-shot | CoT )
STORE_SOLUTION = True #Set if the solution should be stored in a jsonl file. 
MAX_LOOPS = 5         #No. of maximum loops through the debugger

#Set up LLM
GROQ_LLM = ChatGroq( 
    temperature=TEMPERATURE,
    model_kwargs = {"top_p":TOP_P}, #Value given in Llama research paper. #, "seed": RANDOM_SEED
    model=LLAMA_MODEL
)

GPT4_LLM = ChatOpenAI(
    temperature=0.1,
    model = "gpt-4o"
)

def setup_multi_agent_system(filename:str, use_docker:bool = True, prompting_technique:str = "zero-shot", store_solution:bool = True):
    """Function used to setup the multi-agent system.
    args:
        filename: (str) Name of the file where the solutions will be stored (needs to be a jsonl file)
        use_docker: (bool) Set to True if Docker should be used to execute the generated code. 
        prompting_technique: (str): Specify the prompting technique that should be used. Either zero-shot | CoT 
    """
    #Setup agents 
    programmer_agent = Agents.setup_programmer(GROQ_LLM, 'llama',prompting_technique)
    tester_agent = Agents.setup_tester(GROQ_LLM, 'llama',prompting_technique)
    debugger_agent = Agents.setup_debugger(GROQ_LLM, 'llama',prompting_technique)
    workflow = Workflow.setup_workflow(programmer_agent=programmer_agent,tester_agent=tester_agent,debugger_agent=debugger_agent,filename=filename, max_loops=MAX_LOOPS, docker=use_docker, store_as_jsonl=store_solution)
    
    multi_agent_sys = workflow.compile()
    return multi_agent_sys


def generate_solution(multi_agent_sys:object, problem_descripton:str, problem_id:str):
    """Function used to generate a solution for a given problem using a given multi-agent LLM system. The solution gets stored in a jsonl file. 
    args:
        multi_agent_sys: (object) A LLM based multi agent system object that is compiled using Langchain. 
        problem_id: (str): ID of the task or name of the task.
        problem_descripton: (str) Description of the problem.
    """
    tries = 0
    while tries < 5:
        try:
            #Stream to check what is going on (retry if we get exception e.g. ReadTimeoutError )
            inputs = {"problem": problem_descripton, "num_steps":0 , "num_loops":0, 'problem_id':problem_id}
            for outputs in multi_agent_sys.stream(inputs):
                for key,value in outputs.items():
                    print(f"Finished running: {key}:" )
            break
        except Exception as e:
            print(f"{e} occurred, retrying...")
            tries += 1


def generate_multiple_solutions(multi_agent_sys:object, dataset_name:str ='kattis', no_tasks:int = 40, difficulty:str = 'easy'):
    """Function used to generate solutions for a given dataset using a given multi-agent LLM system. The solutions are stored in a jsonl file. 
    args:
        multi_agent_sys: (object) A LLM based multi agent system object that is compiled using Langchain. 
        dataset_name: (str) Name of dataset to be loaded. Set to HumanEval || APPS || Kattis.
        no_tasks: (int) Indicates the number of tasks the system should attempt to generate a solution for. 
        difficulty: (str) Difficulty level for the APPS and Kattis dataset. APPS: 'introductory' || 'interview' || 'competition'. Kattis: 'easy' | 'medium' | 'hard'.
    """
    dataset, question_field, id_field = get_dataset(dataset_name, difficulty) #Retrieve dataset and their corresponding fields. 

    #Go through tasks from given dataset.
    for i in range(no_tasks):
        task = dataset[i]
        problem_descripton = task[question_field]
        problem_id = task[id_field]
        generate_solution(multi_agent_sys, problem_descripton, problem_id)


#-------------------------------GENERATE SOLUTIONS (MULTI-AGENT & SINGLE AGENT) -------------------------------
multi_agent_sys = setup_multi_agent_system(FILENAME, DOCKER, PROMPTING_TECH, STORE_SOLUTION)
generate_multiple_solutions(multi_agent_sys, DATASET_NAME, NO_TASKS, DIFFICULTY)

