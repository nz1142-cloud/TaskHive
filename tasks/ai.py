from django.conf import settings


def generate_risk_assessment(title, description):
    """
    Generate the top two project risks using OpenAI.

    If the API key is missing or the API request fails,
    the function returns a safe fallback message.
    """

    if not settings.OPENAI_API_KEY:
        return (
            "AI risk assessment is unavailable because "
            "OPENAI_API_KEY is not configured."
        )

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        prompt = f"""
You are a project management assistant.

Analyze the following freelance project.

Project title:
{title}

Project description:
{description}

Identify the top 2 practical risks for this project.

For each risk:
1. Give the risk name.
2. Explain it briefly.
3. Give one short recommendation.

Keep the answer concise and easy to understand.
"""

        response = client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=(
                "You are a helpful project risk assessment assistant."
            ),
            input=prompt,
        )

        return response.output_text.strip()

    except Exception:
        return (
            "The AI risk assessment could not be generated right now."
        )
