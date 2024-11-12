from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from prompts import (PROGRAMMER_PROMPT, TEST_DESIGNER_PROMPT, DEBUGGER_PROMPT, PROGRAMMER_COT_PROMPT, TEST_DESIGNER_COT_PROMPT, DEBUGGER_COT_PROMPT)

class Agents():
    """Class contains functions used to setup the different agents (Programmer, Tester, Debugger, Assistant) with their corresponding prompts."""

    @staticmethod
    def setup_programmer(llm, llm_name:str ='llama', prompting_technique:str="zero-shot"):
        if prompting_technique.lower() == "cot" :
            custom_template = PROGRAMMER_COT_PROMPT  +  "\n Solve the following *Problem* \n {problem}" #GPT Template
        else: 
            custom_template = PROGRAMMER_PROMPT + "\n Solve the following *Problem* \n {problem}" #Zero-shot

        if 'llama' in llm_name.lower():
            custom_template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|><|eot_id|><|start_header_id|>user<|end_header_id|>" + custom_template + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"   
        
        programmer_prompt = PromptTemplate(
            template=custom_template,
            input_variables = ["problem"])
    
        programmer_agent = programmer_prompt | llm | StrOutputParser() #Programmer agent
        return programmer_agent

    @staticmethod
    def setup_tester(llm, llm_name:str ='llama', prompting_technique:str="zero-shot"):
        if prompting_technique.lower() == "cot":
            custom_template = TEST_DESIGNER_COT_PROMPT
        else:
            custom_template = TEST_DESIGNER_PROMPT

        if 'llama' in llm_name.lower():
            custom_template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|><|eot_id|><|start_header_id|>user<|end_header_id|>" + custom_template + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        tester_prompt = PromptTemplate(
            template=custom_template,
            input_variables = ["problem", "code"])
        tester_agent = tester_prompt | llm | StrOutputParser()
        return tester_agent

    @staticmethod
    def setup_debugger(llm, llm_name:str ='llama', prompting_technique:str="zero-shot"):
        if prompting_technique.lower() == "zero-shot":
            custom_template = DEBUGGER_PROMPT
        elif prompting_technique.lower() == "cot":
            custom_template = DEBUGGER_COT_PROMPT
        if 'llama' in llm_name.lower():
            custom_template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|><|eot_id|><|start_header_id|>user<|end_header_id|>" + custom_template + "<|eot_id|><|start_header_id|>assistant<|end_header_id|>"

        debugger_prompt = PromptTemplate(
            template= custom_template,
            input_variables = ["code", "error", "problem", "tests"])
        debugger_agent = debugger_prompt | llm | StrOutputParser()
        return debugger_agent
