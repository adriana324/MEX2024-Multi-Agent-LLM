import json 
import os
import regex as re
from datasets import load_dataset
from prompts import *
from pathlib import Path


def get_generated_code(generated_sol: str):
        """Helper function used to retrieve generated code from a response message
        args:
            generated_sol: (str) A generated solution. 
        """
        pattern = "```\n*python\n*[\s\S]*\n*```" 
        #pattern = "```\n*python\n*[\s\S]*\n*```|```\n*[\s\S]*\n*```" #Use this filter if you notice that the returned prompt dosent use '```python' around the code. 
        match = re.search(pattern,generated_sol)
        gen_code = match.group()
        return gen_code

def refactor_code(codeblock:str, both_parts:bool = True):
    """Function used to remove the ``` parts of the code. Specify if it is upper or both parts that should be removed.
       Used before executing the code and storing the the solution. 
    args:
            codeblock: (str) A generated codeblock with ```[code]``` format. 
            both_parts: (bool) Set to True if both the parts '```python ```' should be removed from the string. Set to false to only remove the upper part '```python'.
    """

    python_pattern = "```\n*python\n*"
    match_python = re.search(python_pattern, codeblock) #Check that the codeblock contains python keyword.    
    
    if match_python: 
        python_part = match_python.group()
        if not(both_parts):
            codeblock = codeblock.strip().replace(python_part, "") #Remove only upper part ("```python ") from the string
        else: 
            codeblock = codeblock.strip().replace(python_part, "").replace("```", "") #Removes the whole "```python " part from the string

    else: #Try with a generic code pattern (no language specified) 
        if not(both_parts):
            codeblock = codeblock.strip().replace("```", "") #Remove only upper part ("```` ") from the string
        else:
            codeblock = codeblock.strip().replace("```", "").replace("```", "") #Removes the whole "``` " part from the string 

    return codeblock


def write_sol_to_file(file_name:str, final_solution:str, initial_solution:str, id:str):
    """Helper function that generates a json object and writes it to a file for a given task.
    args:
        file_name: (str) Name of the file. 
        generated_sol: (str) A generated solution. 
        id: (int) id of the task.
    """
    #Generate a json object
    json_res = {
        'task_id' : id,
        'final_solution' : final_solution,
        'initial_solution' : initial_solution,
        }
    json_res = json.dumps(json_res)
    
    #Append content to file
    working_directory =  os.path.dirname(__file__)
    parent_directory = os.path.dirname(working_directory)
    if not os.path.exists(parent_directory+'/generated_solutions'):
            os.makedirs(parent_directory+'/generated_solutions')
    with open(parent_directory+'/generated_solutions/' +  file_name, 'a') as f:
        f.write(json_res + '\n')


def get_dataset(dataset_name:str ='kattis', difficulty:str = 'easy'):
    """Helper function to retrieve dataset and their needed field names
    args:
        dataset_name: (str) Name of dataset to be loaded. Set to Kattis || HumanEval || APPS.
        difficulty: (str) Difficulty level for the APPS and Kattis dataset. APPS: 'introductory' || 'interview' || 'competition'. Kattis: 'easy' | 'medium' | 'hard'.
    """
    if dataset_name.lower() == 'humaneval' or dataset_name.lower() == 'apps':
        dataset, question_field, id_field = _load_tasks_from_dataset(dataset_name, difficulty)
    elif dataset_name.lower() == 'kattis':
        working_directory =  os.getcwd()
        parent_directory = os.path.dirname(working_directory)
        dataset_file_path = '/kattis_dataset/all_problems.json'
        f = open(parent_directory+dataset_file_path)
        data = json.load(f)
        dataset = data[difficulty]
        question_field = "description"
        id_field = "problem_name"
    else:
        raise ValueError("Only supports datasets APPS, Humaneval and local Kattis dataset")
    return dataset, question_field, id_field

                    

def _load_tasks_from_dataset(dataset_name:str = 'humaneval', difficulty:str = 'introductory'):
    """Function used to load given dataset from HugginFace. Difficulty level must be set for APPS dataset.   
    args:
        dataset_name: (str) Name of dataset to be loaded. Set to HumanEval || APPS.
        difficulty: (str) Difficulty level for the APPS dataset. Set to 'introductory' || 'interview' || 'competition'.

    returns:
        dataset: (object) Loaded tasks from the given dataset. 
        question_field: (str) Name of the field to extract the task description from the dataset. 
        id_field: (str) Name of the field to extract the task id from the dataset. 

    """
    if dataset_name.lower() == 'humaneval':
        ds_humaneval = load_dataset("openai_humaneval")
        dataset = ds_humaneval['test']
        question_field = 'prompt'
        id_field = 'task_id'
    elif dataset_name.lower() == 'apps':
        apps_eval = load_dataset("codeparrot/apps", split='test')
        dataset = apps_eval.filter(lambda x: x['difficulty'] == difficulty) #Filter out questions from a given level
        question_field = 'question'
        id_field = 'problem_id'
    else: 
        raise ValueError("Only the datasets HumanEval & APPS supported. Set dataset_name to either HumanEval or APPS" ) 
    
    return dataset, question_field, id_field



