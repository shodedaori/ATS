import os
import pytest
import json
from tqdm import tqdm

from data import load_opc_dataset, load_given_opc_data
from generate.core import generate_solution, generate_fix
from generate.code import generate_simple_code, generate_readable_code, generate_robust_code
from generate.test_case import generate_test_suite
from utils.code import get_func_name, get_python_code, get_extra_info
from utils.write import generate_test_case_from_code


def generate_test():
    # dataset = load_opc_dataset(1)  # a random dataset
    dataset = [load_given_opc_data(33722442615)]

    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")

    for data in tqdm(dataset):
        seq_id = data['seq_id']
        data_path = os.path.join(test_path, f"task_{seq_id}")
        os.makedirs(data_path, exist_ok=True)

        generate_test_suite(data_path, data["instruction"], k=6)


def eval():
    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")    

    test_summary = list()
    
    for name in os.listdir(test_path):
        task_path = os.path.join(test_path, name)
        
        print(f"Evaluating {name}...")
        
        test_res = dict()
        test_res['name'] = name
        test_res['style'] = list()

        for style_name in os.listdir(task_path):
            style_path = os.path.join(task_path, style_name)

            if not os.path.isdir(style_path):
                continue

            style_res = dict()
            style_res['name'] = style_name
            style_res['passed'] = []
            style_res['failed'] = []            

            for test_file in os.listdir(style_path):
                if not (test_file.endswith('.py') and test_file.startswith('test_')):
                    continue


                test_file_path = os.path.join(style_path, test_file)
                exit_code = pytest.main(['-vs', test_file_path, '--tb=short'])
                
                if exit_code == 0:
                    style_res['passed'].append(test_file)
                else:
                    style_res['failed'].append(test_file)                

            test_res['style'].append(style_res)

        test_summary.append(test_res)
        
    with open('test_summary.json', 'w') as f:
        json.dump(test_summary, f, indent=4)


def fix_standard_test(task_name, test_number):
    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")
    task_path = os.path.join(test_path, task_name)

    with open(os.path.join(task_path, "prompt.txt"), 'r') as f:
        prompt = f.read()
    
    standard_path = os.path.join(task_path, "standard")
    
    with open(os.path.join(standard_path, f"test_{test_number}.py"), 'r') as f:
        test_snippet = f.read()

    with open(os.path.join(standard_path, f"property_{test_number}.txt"), 'r') as f:
        test_property = f.read()

    fix = generate_fix(prompt, test_snippet, test_property)
    
    # write the old snippet into a new file
    with open(os.path.join(standard_path, f"test_{test_number}_old.txt"), 'w') as f:
        f.write(test_snippet)

    if fix.startswith("FUNCTION AND TEST"):
        # get new function code and new test code
        raise NotImplementedError("Function and test fix not implemented yet")
    elif fix.startswith("FUNCTION"):
        # get new function code
        function_code = fix.split("```python")[1].split("```")[0]
        
        with open(os.path.join(standard_path, f"func_code.txt"), 'r') as f:
            old_function_code = f.read()
        
        with open(os.path.join(standard_path, f"func_code_old.txt"), 'w') as f:
            f.write(old_function_code)

        with open(os.path.join(standard_path, f"func_code.txt"), 'w') as f:
            f.write(function_code)

        generate_test_case_from_code(function_code, standard_path, standard_path)
        

    elif fix.startswith("TEST"):
        # get new test code
        test_code = fix.split("```python")[1].split("```")[0]
        with open(os.path.join(standard_path, f"test_code_{test_number}.txt"), 'w') as f:
            f.write(test_code)

        with open(os.path.join(standard_path, f"func_code.txt"), 'r') as f:
            function_code = f.read()

        test_case = f'{function_code}\n"""{test_property}"""\n{test_code}'
        
        with open(os.path.join(standard_path, f"test_{test_number}.py"), 'w') as f:
            f.write(test_case)

    else:
        raise ValueError("Invalid fix format")
    

def test_other_style(task_name, style_name):
    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")
    task_path = os.path.join(test_path, task_name)

    standard_path = os.path.join(task_path, "standard")
    style_path = os.path.join(task_path, style_name)

    with open(os.path.join(style_path, "func_code.txt"), 'r') as f:
        function_code = f.read()

    generate_test_case_from_code(function_code, standard_path, style_path)


if __name__ == "__main__":
    # generate_test()
    # fix_standard_test("task_33722442615", 4)
    # test_other_style("task_33722442615", 'simple')
    pass