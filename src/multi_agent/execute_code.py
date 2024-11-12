import subprocess
import docker
import regex as re
import tempfile
import os
from subprocess import TimeoutExpired
from requests.exceptions import ConnectionError, Timeout
from utils import get_generated_code, refactor_code

class CodeExecution():
    """Class contains functions needed to execute code from a LLMs response message. """

    @staticmethod
    def __create_temp_file(message:str, suffix:str='.py'):
        """Creates a temporary file, use suffix to specify if it is a .py file or .txt etc"""
        working_directory =  os.path.dirname(__file__)
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False,dir=working_directory+'/temp')
        with open(file=tmp.name, mode='w') as f:
            f.write(message)
        return tmp.name
    
    @staticmethod
    def __remove_temp_file(temp_filename):
        """Function to remove a given file """
        # Check if the file exists before attempting to delete it
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print("Temporary file deleted successfully.")
        else:
            print("The temporary file does not exist.")

    @staticmethod
    def combine_two_codeblocks(message1:str, message2:str):
        """ Function used to combine code and testcases into one codeblock.
        args:
            message1: (str) Response containing the generated code. 
            message2: (str) Response containing the generated test cases.  
        """
        code = get_generated_code(message1)
        code = code.rsplit('```',1)[0] #Split once from the right and keep the left part. This is to remove the last '```' from the codeblock (needed to combine two codeblocks into one). 

        pattern = "if __name__ == (\"|\')__main__(\"|\'):[\s\S]* main\(\)"
        match = re.search(pattern, code) #Check that the codeblock contains if __name__ == main part.    
        if match:
            main_part = match.group()
            code = code.replace(main_part,"") #Removes the part that makes the main function execute (as we will instead run unittest)

        tests = get_generated_code(message2)
        tests = refactor_code(codeblock=tests, both_parts=False) #Only remove upper part, e.g. ```python " from the string.

        codeblock = code+"\n"+tests #Add tests at the end of the code string.
        
        print("------Combined codeblock------------")
        print(codeblock)

        return codeblock

    @staticmethod
    def exec_python_codeblock(codeblock:str,  docker:bool=False, timeout:int=30):
        """ Function used to execute code from a response message
        args:
            codeblock: (str) A Python codeblock. 
            docker: (bool) Set to True to use Docker. 
            timout: (int) Execution timeout. 
        """

        codeblock = refactor_code(codeblock=codeblock, both_parts=True) #Removes the whole "```python ```" part from the string.

        tmp_file = CodeExecution.__create_temp_file(codeblock)
        try: 
            if docker: 
                result = CodeExecution.__exec_codeblock_in_docker(tmp_file)
            else:
                result = subprocess.run(["python", tmp_file], capture_output=True, timeout=timeout, text=True)
                result = result.stderr
        except Exception as e:
            if isinstance(e, TimeoutExpired):
                result = "TimeoutExpired , execution timed out after 30 seconds"
            elif isinstance(e, Timeout) or isinstance(e, ConnectionError):
                result = "ConnectionError, Docker execution timed out"
            else:
                result = e
        finally:
            CodeExecution.__remove_temp_file(tmp_file)
        return result


    @staticmethod
    def __exec_codeblock_in_docker(temp_file):
        """ Helper function used to execute code in a python file using Docker.  
        args:
            temp_file: The name of the Python scirpt file that should be executed. 
        returns: 
            Returns an encoded message, containing the execution message (e.g. an error message). 
        """

        # Mount the temporary file into the container
        volumes = {os.path.abspath(temp_file): {'bind': temp_file, 'mode': 'rw'}}

        # Run the Docker container with the Python code
        client = docker.from_env()


        # Docker image to use
        image_name = "python:3.9-slim"
        container = client.containers.run(
            image_name,
            command=["python", temp_file],
            volumes=volumes,
            remove=False,
            stdout=True,
            stderr=True,
            detach=True
        )

        try:
            #Get log data
            result = container.logs(follow=True)
            
        finally:
            #Stop and remove container after execution
            container.stop()
            container.remove()
            
        
        return result