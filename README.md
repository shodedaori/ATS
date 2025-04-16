# ATS
AI Test Suite (Automated Test Suite Generation and Code Fix)

## How to use demo

First, you should install all library from requirements.txt and specify your configuration in `generate/core.py`. Specify the LLM you want to use and your OpenAI api key. 

```python
def generate_response(
        prompt, 
        model="gpt-4.5-preview", # or "gpt-4o"
        api_key="YOU API KEY"
    ):
```

Then, you can run `demo.py` to to generate test suits for tasks in `opc-sft-stage2` dataset.

To test the demo, you need to give the task first. You can use the function `generate_test()` to generate test suits. You can specify the sequence id of a data or generate a random list.

After the generation of the test suits, you need to run pytest in `tests/task_xxx/standard` folder. For failed test cases you need to use function `fix_standard_test` in the `demo.py`. Example code is like this:

```python
fix_standard_test("task_33722442615", 4)  # fix test_4.py in tests/task_33722442615/standard
```

The fix is not guaranteed, you may need to fix a lot of times.

If you want to generate test cases for robust or simple version of the code, you need to use function `test_other_style` in the `demo.py`. Example code is like this:

```python
test_other_style("task_33722442615", 'simple')  # generate test cases in tests/task_33722442615/simple
```