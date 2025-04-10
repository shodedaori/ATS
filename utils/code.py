from typing import List, Optional, Dict, Any


def get_python_code(text: str):
    code = text.split("```python")[1].split("```")[0]
    return code


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
            func_name = line.strip()
            break

    if func_name is None:
        raise ValueError("Function name not found in the response")

    return func_name


def get_extra_info(code: str) -> str:
    snippet = code.split('\ndef')[0].strip()
    snippet = f"```python\n{snippet}\n```"

    return snippet


def remove_special_tokens(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []
    special_tokens = "8u9U10I"
    for line in lines:
        if special_tokens in line:
            continue
        cleaned_lines.append(line)
    
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text
