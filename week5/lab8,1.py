import requests

# ===== PROMPT =====
PROMPT = """
CONTEXT: You are provided with:
1. Python snippet enclosed with ```python OLD ```
2. Examples enclosed with ```python OLD_i ``` followed by ```python REFACTORED_i ```

TASK: Refactor the snippet to a log message.

OLD_1: ```python
print('Process started for config.txt with verbose=True')
```
REFACTORED_1: ```python
logger.info('Processing started', extra={'verbose': True, 'file': 'config.txt'})
```

OLD_2: ```python
print('Warning! Could not load user U-232 data from user_info.csv')
```
REFACTORED_2: ```python
logger.warning('User data failed to load', extra={'user': 'U-232', 'file': 'user_info.csv'})
```

OLD: ```python
print('Error! File not found: passwords.txt')
```
REFACTORED:
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
    try:
        response = ollama_generate(PROMPT)
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