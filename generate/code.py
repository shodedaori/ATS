from generate.core import generate_response
from utils.code import get_python_code


def generate_readable_code(prompt, func_name, extra_info=None):
    code_prefix = "Here's your coding task:\n"
    instruction_prefix = f"Here are some additional requirements for the code: you should add type hints for all the input and output parameters of the function. You should also add docstrings for the function, including a description of the function, its parameters, and its return value. The docstring should be formatted according to the Google style guide.\nThe name of the function should be {func_name}. Outputs the function without explanation.\n"

    if extra_info:
        instruction_prefix += f"Here is the code snippet you should refer:\n{extra_info}\n"

    code_prompt = f"{code_prefix}{prompt}\n\n{instruction_prefix}"

    response = generate_response(code_prompt)
    code = get_python_code(response)

    return code


def generate_simple_code(prompt, func_name, extra_info=None):
    code_prefix = "Here's your coding task:\n"
    instruction_prefix = f"Here are some additional requirements for the code: keep the programming logic in the function as simple and straightforward as possible.Make this program understandable even for beginners.\nThe name of the function should be {func_name}. Outputs the function without explanation.\n"

    if extra_info:
        instruction_prefix += f"Here is the code snippet you should refer:\n{extra_info}\n"

    code_prompt = f"{code_prefix}{prompt}\n\n{instruction_prefix}"

    response = generate_response(code_prompt)
    code = get_python_code(response)

    return code


def generate_robust_code(prompt, func_name, extra_info=None):
    code_prefix = "Here's your coding task:\n"
    instruction_prefix = f"Here are some additional requirements for the code: make the program as robust as possible. Handle all possible exceptions and edge cases. \nThe name of the function should be {func_name}. Outputs the function without explanation.\n"

    if extra_info:
        instruction_prefix += f"Here is the code snippet you should refer:\n{extra_info}\n"

    code_prompt = f"{code_prefix}{prompt}\n\n{instruction_prefix}"

    response = generate_response(code_prompt)
    code = get_python_code(response)

    return code