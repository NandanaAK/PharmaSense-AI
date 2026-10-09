from google import genai
import os
import json
from datetime import datetime


api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

log_file = os.path.join(
    project_folder,
    "logs",
    "llm_calls.jsonl"
)


def log_llm_call(prompt, response):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": "gemini-3.8-flash",
        "prompt": prompt,
        "response": response
    }

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")

    print("✓ LLM call logged successfully")


def call_llm(prompt):

    print("Sending request to Gemini...")

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    response = interaction.output_text

    print("Gemini response received.")

    log_llm_call(prompt, response)

    return response


if __name__ == "__main__":

    response = call_llm(
        "Say hello from PharmaSense AI in one sentence."
    )

    print("\nGemini Response:")
    print(response)