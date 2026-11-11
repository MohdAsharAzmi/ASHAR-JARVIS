
def generate_reply(
    message: str,
    language: str = "hinglish",
    personality: str = "professional"
) -> str:

    message = message.strip()

    if not message:
        return "Please tell me something."

    return (
        "JARVIS received your message: "
        + message
        + ". Language preference: "
        + language
        + ". Personality: "
        + personality
        + ". Actual AI brain is not connected yet."
    )
