from typing import List, Dict, Any
import os
from openai import OpenAI


def generate_response(
        prompt, 
        model="gpt-4o-mini", 
        api_key="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"
    ):
    """
    Generate a response from the OpenAI API.

    Args:
        prompt (str): The input prompt for the AI model.
        model (str): The model to use for generation.
        api_key (str): The API key for authentication.

    Returns:
        str: The generated response from the model.
    """
    client = OpenAI(api_key=api_key)

    # Generate a response using the specified model
    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text


def generate_properties(prompt, solution):
    code_prefix = "Here's your coding task:\n"
    solution_prefix = "Here's a possible solution:\n"
    property_prefix = "Your job is to help me complete a property-based testing suite. Generate the properties the coding task should satisfy.\nFor each property, provide a condition that the input should satisfy, and a condition that the output should satisfy. Outputs a list of properties and its input, and output condition without examples.\n"

    property_prompt = f"{code_prefix}{prompt}\n\n{solution_prefix}{solution}\n\n{property_prefix}"

    response = generate_response(property_prompt)

    return response


def generate_test_code(prompt, solution, prop, func_name):
    code_prefix = "Here's your coding task:\n"
    solution_prefix = "Here's a possible solution:\n"
    property_prefix = "Here is the property we want to test for our solution:\n"
    test_code_prefix = f"Your job is to help me complete a testing suite. Based on the given solution and propterty, generate a test case to verity the given property. In the testing, you first need to randomly generate inputs that satisfy the input condition in the given property, then you need to check whether the output satisfies the output condition in the given property. Run a loop test 100 times within the test case. Outputs a test function without any explanation. In the test function, you should import {func_name} from 'func.py'.\n"

    test_code_prompt = f"{code_prefix}{prompt}\n\n{solution_prefix}{solution}\n\n{property_prefix}{prop}\n\n{test_code_prefix}"
    response = generate_response(test_code_prompt)
    
    return response

def write_into_function(seq_id, response):
    folder_path = f"task/run_{seq_id}/"
    os.makedirs(folder_path, exist_ok=True)

    code = response.split("```python")[1].split("```")[0]
    with open(f"{folder_path}func.py", "w") as f:
        f.write(code)

    with open(f"{folder_path}__init__.py", "w") as f:
        f.write("")


def get_properties_list(props: str) -> List[str]:
    lines = props.splitlines()
    prop_list = []

    current_prop = None

    for line in lines:
        if line.find("Property") != -1 and line.find(":") != -1:
            current_prop = [line.strip()]
        elif current_prop is not None:
            if line.find("Input Condition") != -1 and line.find(":") != -1:
                current_prop.append(line.strip())
            elif line.find("Output Condition") != -1 and line.find(":") != -1:
                current_prop.append(line.strip())

                prop_str = "\n".join(current_prop)
                prop_list.append(prop_str)
                current_prop = None
            else:
                raise ValueError("Invalid property format")
    
    return prop_list


def get_func_name(response: str) -> str:
    lines = response.splitlines()
    func_name = None

    for line in lines:
        if line.startswith("def "):
            func_name = line.split("(")[0][4:].strip()
            break

    if func_name is None:
        raise ValueError("Function name not found in the response")

    return func_name


def write_test_code(seq_id, prompt, response, k=5):
    ai_prop = generate_properties(prompt, response)
    print(ai_prop)
    func_name = get_func_name(response)
    prop_list = get_properties_list(ai_prop)
    prop_list = prop_list[:k]
    print(f"Generated {len(prop_list)} properties.")

    for i, prop in enumerate(prop_list):
        folder_path = f"task/run_{seq_id}/"
        os.makedirs(folder_path, exist_ok=True)

        test_code = generate_test_code(prompt, response, prop, func_name)
        test_code = test_code.split("```python")[1].split("```")[0]
        prop_prefix = f'"""\n{prop}\n"""\nfrom typing import List, Dict, Any\nfrom .func import {func_name}\n'
        test_code = prop_prefix + test_code
        with open(f"{folder_path}test_{i}.py", "w") as f:
            f.write(test_code)


if __name__ == "__main__":

    seq_id = "2"

    prop = """### Property 1: Missing Number Exists in Range
**Input Condition**: The list `numbers` must contain distinct integers ranging from `0` to `n`, with exactly one integer missing.
**Output Condition**: The output must be an integer that exists within the range `[0, n]`, specifically the missing integer.
    """
    # Example usage
    prefix = "Finish this coding task in Python (please add type annotations for all variables):\n"
    prompt = "Write a function to find the missing number in a given list of numbers ranging from 0 to n."
    prompt = f"{prefix}{prompt}"
    # print(prompt)
    with open("example_response.txt", "r") as f:
        response = f.read()

    write_test_code(seq_id, prompt, response)
    exit(0)

    # print(response)



    # generate_properties(prompt, response)
    generate_test_code(prompt, response, prop)

