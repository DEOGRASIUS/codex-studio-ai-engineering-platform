from agents.providers.router import generate_with_ai


result = generate_with_ai(
    "You are a helpful software assistant.",
    "Explain what Django is in one sentence."
)

print(result)