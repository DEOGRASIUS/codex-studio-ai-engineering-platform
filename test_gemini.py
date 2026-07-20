import os
from dotenv import load_dotenv

from agents.providers.gemini import generate_with_gemini


load_dotenv()


result = generate_with_gemini(
    "You are a helpful assistant.",
    "Explain what Django is in two sentences."
)


print(result)