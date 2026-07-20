"""Google Gemini AI provider with retry and fallback support."""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()


PRIMARY_MODEL = "gemini-flash-latest"

FALLBACK_MODEL = "gemini-2.0-flash"


MAX_RETRIES = 3


def generate_with_gemini(system_prompt, user_input):
    """
    Generate content using Google Gemini.

    Includes:
    - retry handling
    - temporary outage protection
    - model fallback
    """


    api_key = os.getenv(
        "GEMINI_API_KEY"
    )


    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY is missing."
        )



    client = genai.Client(
        api_key=api_key
    )



    prompt = f"""
System Instructions:

{system_prompt}


User Request:

{user_input}
"""



    models = [
        PRIMARY_MODEL,
        FALLBACK_MODEL,
    ]



    last_error = None



    for model in models:


        for attempt in range(
            1,
            MAX_RETRIES + 1
        ):


            try:


                response = client.models.generate_content(

                    model=model,

                    contents=[
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": prompt
                                }
                            ],
                        }
                    ],
                )



                content = (
                    response.text.strip()
                    if response.text
                    else ""
                )



                if content:

                    return content



                raise ValueError(
                    "Gemini returned empty response."
                )



            except ServerError as exc:


                last_error = exc



                print(
                    f"Gemini {model} unavailable. "
                    f"Retry {attempt}/{MAX_RETRIES}"
                )


                time.sleep(
                    attempt * 3
                )



            except Exception as exc:


                last_error = exc

                break



    raise RuntimeError(
        f"Gemini generation failed after retries: {last_error}"
    )