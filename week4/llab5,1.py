import inspect
import os
import subprocess
import requests

# System prompts
SURROUND = "You will be provided with a Python function enclosed with {{{ Function }}}."
SINGLE_TASK = "Generate a Google Style Python docstring including Args and Returns."


# Singleton implementation
class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


# Create user prompt
def get_user_prompt(func: callable) -> str:

    return f"""
FUNCTION: {{{{{{ {inspect.getsource(func)} }}}}}}
GOOGLE STYLE DOCSTRING:
"""


def ollama_generate(prompt: str, model: str = "llama2") -> str:
    """Generate a response using Ollama's REST API.

    Requires Ollama server running on localhost:11434.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]


if __name__ == "__main__":

    use_ollama = os.environ.get("USE_OLLAMA", "0") == "1"

    if use_ollama:
        # nothing to validate for Ollama, just call the CLI later
        client = None
    else:
        from openai import OpenAI
        # Ensure API key is available
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.\n" \
                               "Please export your API key before running the script.")

        # Initialize OpenAI client with the key
        client = OpenAI(api_key=api_key)

    if use_ollama:
        # Ollama accepts a single plain-text prompt rather than a chat payload
        prompt_text = f"{SURROUND} {SINGLE_TASK}\n\n" + get_user_prompt(Singleton.__call__)
        try:
            response = ollama_generate(prompt_text, model="llama2")
            print("Generated Docstring (Ollama):\n")
            print(response)
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("\nGenerated prompt (since Ollama is not available):")
            print(prompt_text)
    else:
        completion = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[
                {"role": "system", "content": f"{SURROUND} {SINGLE_TASK}"},
                {"role": "user", "content": get_user_prompt(Singleton.__call__)},
            ],
        )

        print("Generated Docstring:\n")
        print(completion.choices[0].message.content)