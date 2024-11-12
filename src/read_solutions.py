import os
import json 

def read_specific_json_from_file(file_name:str, id:str):
    """Function used to read a specific json object from a given jsonl file."""
    working_directory =  os.path.dirname(__file__)
    file_path = working_directory+file_name
    with open(file_path, 'r') as json_file:
        json_list = list(json_file)

    for json_line in json_list:
        json_object = json.loads(json_line)
        if json_object.get('task_id') == id:
            return json_object


def validate_jsonl(file_path):
    """ Helper function used to check if the contents of a jsonl file are correctly formatted. 
        If an error is found, then the line number for where the error lies is printed. 
    args:
        file_path: (str) The jsonl file path. 
    """
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            try:
                json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {line_num}: {e}")
                print(line)


#-------------------------------PRINT OUT SOLUTIONS FROM JSONL FILE-------------------------------
#Print out solution that is stored on jsonl file
file = '/generated_solutions/kattis_hard_llama3_CoT.jsonl'
task_name = "The Wire Ghost"
solution = read_specific_json_from_file(file, task_name)
print("Singel Agent solution:")
print(solution['initial_solution'])
print("Multi-Agent solution:")
print(solution['final_solution'])
