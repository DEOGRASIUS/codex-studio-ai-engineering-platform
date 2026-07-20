"""
AI Provider Router.

Controls which AI service
Codex Studio uses.
"""


import os


from agents.providers.gemini import (
    generate_with_gemini,
)



def generate_with_ai(
    system_prompt,
    user_input
):
    """
    Route AI requests to providers.
    """


    provider = os.getenv(
        "AI_PROVIDER",
        "gemini"
    ).lower()



    providers = {

        "gemini":
            generate_with_gemini,

    }



    if provider not in providers:


        raise ValueError(
            f"Unsupported AI provider: {provider}"
        )



    generator = providers[provider]



    return generator(
        system_prompt,
        user_input
    )