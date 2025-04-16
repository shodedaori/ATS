import os


def generate_test_case_from_code(function_code, refer_folder, cases_folder):
    n_test_case = 0
    for name in os.listdir(refer_folder):
        if name.startswith('test_code_') and name.endswith('.txt'):
            n_test_case += 1
    
    print(f"Number of test cases: {n_test_case}")

    for i in range(n_test_case):
        with open(os.path.join(refer_folder, f'property_{i}.txt'), 'r') as f:
            prop = f.read()

        with open(os.path.join(refer_folder, f'test_code_{i}.txt'), 'r') as f:
            test_case = f.read()

        with open(os.path.join(cases_folder, f'test_{i}.py'), 'w') as f:
            f.write(function_code)
            f.write('\n')
            f.write(f'"""\n{prop}\n"""\n')
            f.write(test_case)
