import os
from generate.core import generate_properties, generate_test_code, generate_solution
from generate.code import generate_readable_code, generate_simple_code, generate_robust_code
from utils.code import get_func_name, get_properties_list, get_python_code, get_extra_info, remove_special_tokens


def generate_test_case(prompt, response, k=4):
    ai_prop = generate_properties(prompt, response)
    func_name = get_func_name(response)
    prop_list = get_properties_list(ai_prop)
    prop_list = prop_list[:k]
    print(f"Generated {len(prop_list)} properties.")

    test_case = []

    for i, prop in enumerate(prop_list):

        test_code = generate_test_code(prompt, response, prop, func_name)
        test_code = test_code.split("```python")[1].split("```")[0]

        # Add the property to the test code
        test_code = f'"""\n{prop}\n"""\n{test_code}'
        test_code = remove_special_tokens(test_code)
        # Add the test code to the list
        test_case.append(test_code)

    return prop_list, test_case 


def write_test_case(folder_path, code, test_cases, prop_list):
    for i, test_case in enumerate(test_cases):
        with open(f"{folder_path}/test_code_{i}.txt", "w") as f:
            f.write(test_case)

        with open(f"{folder_path}/property_{i}.txt", "w") as f:
            f.write(prop_list[i])

        with open(f"{folder_path}/test_{i}.py", "w") as f:
            f.write(code)
            f.write('\n')

            f.write(test_case)
            f.write('\n')


def generate_test_suite(folder_path, prompt, k=4):

    solution = generate_solution(prompt)
    standard_code = get_python_code(solution)

    with open(os.path.join(folder_path, "prompt.txt"), "w") as f:
        f.write(prompt)

    func_name = get_func_name(standard_code)
    extra_info = get_extra_info(standard_code)

    addtional_style_names = ['simple', 'robust']
    addtional_style_func = [generate_simple_code, generate_robust_code]
    
    style_names = ['standard']
    style_code = [standard_code]

    for name, func in zip(addtional_style_names, addtional_style_func):
        code = func(prompt, func_name, extra_info)
        style_names.append(name)
        style_code.append(code)

    props, test_cases = generate_test_case(prompt, standard_code, k)
    for name, code in zip(style_names, style_code):
        this_path = os.path.join(folder_path, name)
        os.makedirs(this_path, exist_ok=True)
        
        with open(os.path.join(this_path, "func_code.txt"), "w") as f:
            f.write(code)

        if name != 'standard':
            continue

        write_test_case(this_path, code, test_cases, props)
