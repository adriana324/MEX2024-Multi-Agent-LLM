# MEX2024 Multi Agent LLM
*The system in this repository was created as part of a thesis experiment*

This repository contains a LLM-based multi-agent system that is designed to be used for code generation. 
In the directory 'generated_solutions' all the solutions generated for the problems found in 'kattis_dataset/all_problems.json' can be found. 
The files in 'generated_solutions' contain two solutions for each assignment: 
1. The inital solution generated by Llama 3-70b. 
2. The final solutions produced after going through the entrie multi-agent system pipeline, completly powered by Llama 3-70b. 


## System configuration 
- The required packages are listed in the req.txt file. It is recomended to use a package manager, such as Miniconda, to install all the dependencies. 

- To generate solutions execute the **main.py** file. Change the  parameters found on top of thefile as needed before executing it. 

- To output a generated solution execute the file **read_solutions.py**. Configure it so that it has the correct file_path and task_name.  


### Environment file 
The system requires both GROQ and LangChain API keys. To use the system, create a .env file in the src directory and add your API keys as follows: 
```python
LANGCHAIN_API_KEY = "your_langchain_api_key" 
GROQ_API_KEY = "your_groq_api_key"
```

### Datasets 
The dataset that was used in the experiment is 'kattis_dataset/all_problems.json'. 
However, the system is also able to generate solutions for the coding problems found on the HumanEval and APPS datasets
by changing the constant value of 'DATASET_NAME' found in **main.py** to 'humaneval' or 'apps'.

### Docker 
The system is configured to execute the generated code in a docker container, however this is optional. 
Set the constant named 'DOCKER' in the **main.py** to False to instead use Pythons subprocess module. 

The Docker image used for the code execution is "python:3.9-slim". Either download the image from [here](https://hub.docker.com/_/python)
or if you want to use a different image, change the image name in the function **__exec_codeblock_in_docker()** found in the file **execute_code.py**. 


## Disclaimer 
This system is configured to use Meta's Llama 3 model, please read through their [open-source licensce](https://www.llama.com/llama3/license/) before use. 