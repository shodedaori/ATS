from openai import OpenAI


def generate_response(
        prompt, 
        model="gpt-4o", 
        api_key="YOUR API KEY"
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


def generate_solution(prompt):
    code_prefix = "Finish this coding task in Python (please add type annotations for all variables):\n"
    code_prompt = f"{code_prefix}{prompt}"

    response = generate_response(code_prompt)

    return response    


def generate_properties(prompt, solution):
    code_prefix = "Here's your coding task:\n"
    solution_prefix = "Here's a possible solution:\n"
    property_prefix = "Your job is to help me complete a property-based testing suite. Generate the properties the coding task should satisfy.\nFor each property, provide a condition that the input should satisfy, and a condition that the output should satisfy. Outputs a list of properties and its input, and output condition without examples. Each property consists of 3 lines. The first line should contain '**Property <number> : <content of the property>'. The second line should contain '**Input Condition:**', and the third line should contain '**Output Condition:**'.\n"

    property_prompt = f"{code_prefix}{prompt}\n\n{solution_prefix}{solution}\n\n{property_prefix}"

    response = generate_response(property_prompt)

    return response


def generate_test_code(prompt, solution, prop, func_name):
    code_prefix = "Here's your coding task:\n"
    solution_prefix = "Here's a possible solution:\n"
    property_prefix = "Here is the property we want to test for our solution:\n"
    test_code_prefix = f"Your job is to help me complete a testing suite. Based on the given solution and propterty, generate a test case to verity the given property. In the testing, you first need to randomly generate inputs that satisfy the input condition in the given property, then you need to check whether the output satisfies the output condition in the given property. Run a loop test 100 times within the test case. Outputs a test function without any explanation. In the test function, you should import {func_name} and other classes in the solution from '8u9U10I.py'.\n"

    test_code_prompt = f"{code_prefix}{prompt}\n\n{solution_prefix}{solution}\n\n{property_prefix}{prop}\n\n{test_code_prefix}"
    response = generate_response(test_code_prompt)
    
    return response


def generate_fix(prompt, test_case, property):
    code_prefix = "Here's my coding task:\n"
    test_case_prefix = "Here's my test case:\n"
    property_prefix = "Here's the property I want to test:\n"
    fix_prefix = "This test case raise an error. Check whether the function is wrong or the test case is wrong. If the function is wrong, outputs FUNCTION first and outputs a new function code without explanation. If the test case is wrong, outputs TEST first and outputs a new test function code without explanation. If they are both wrong, outputs FUNCTION AND TEST first, and outputs a new function code and a new test function separately without explanation.\n"

    fix_prompt = f"{code_prefix}{prompt}\n\n{test_case_prefix}```python{test_case}```\n\n{property_prefix}{property}\n\n{fix_prefix}"
    
    response = generate_response(fix_prompt)

    return response
