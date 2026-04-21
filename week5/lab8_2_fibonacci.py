import requests

SYSTEM_PROMPT = """
You are provided with:
1. A Python function signature enclosed with {{{ FUNCTION }}}
2. Example signatures {{{ FUNCTION_i }}} and implementations {{{ CODE_i }}}

Your task is to implement the function.
"""

USER_PROMPT = """
FUNCTION_1: {{{ def get_area(radius: float) -> float: }}}
CODE_1: {{{ def get_area(radius: float) -> float:
    area: float = 3.14 * radius ** 2
    return area }}}

FUNCTION_2: {{{ def get_arithmetic_mean(x1: float, x2: float) -> float: }}}
CODE_2: {{{ def get_arithmetic_mean(x1: float, x2: float) -> float:
    arithmetic_mean: float = (x1 + x2) / 2
    return arithmetic_mean }}}

FUNCTION: {{{ def print_fibonacci_sequence(n: int) -> None: }}}

CODE:
"""


def ollama_generate(prompt, model="gemma3:1b"):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    data = res.json()
    if "error" in data:
        raise ValueError(f"Ollama error: {data['error']}")
    return data["response"]


if __name__ == "__main__":
    full_prompt = SYSTEM_PROMPT + "\n" + USER_PROMPT
    try:
        response = ollama_generate(full_prompt)
        # Extract code from ```python ... ```
        import re
        match = re.search(r'```python\s*(.*?)\s*```', response, re.DOTALL)
        if match:
            print(match.group(1).strip())
        else:
            print(response.strip())
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure Ollama is running and the model is installed.")