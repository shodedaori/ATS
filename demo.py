import os
import pytest
from tqdm import tqdm

from data import load_opc_dataset, load_given_opc_data
from generate.core import generate_solution
from generate.code import generate_simple_code, generate_readable_code, generate_robust_code
from generate.test_case import generate_test_suite
from utils.code import get_func_name, get_python_code, get_extra_info


def main():
    dataset = load_opc_dataset(10)

    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")

    for data in tqdm(dataset):
        seq_id = data['seq_id']
        data_path = os.path.join(test_path, f"task_{seq_id}")
        os.makedirs(data_path, exist_ok=True)

        generate_test_suite(data_path, data["instruction"], k=6)


def eval():
    dataset = load_given_opc_data(19434228727)
    seq_id = dataset["seq_id"]

    my_path = os.getcwd()
    test_path = os.path.join(my_path, "tests")    
    data_path = os.path.join(test_path, f"task_{seq_id}")

    k = 2
    style_name = ['simple']
    for name in style_name:
        this_path = os.path.join(data_path, name)
        assert os.path.exists(this_path), f"Path {this_path} does not exist."

        passed = 0

        for i in range(k):
            test_file = os.path.join(this_path, f"test_{i}.py")
            assert os.path.exists(test_file), f"Test file {test_file} does not exist."

            exit_code = pytest.main(['-vs', test_file, '--tb=short'])
            if exit_code == 0:
                print(f"{name} test_{i} passed.")
                passed += 1
            else:
                print(f"{name} test_{i} failed.")


if __name__ == "__main__":
    main()
