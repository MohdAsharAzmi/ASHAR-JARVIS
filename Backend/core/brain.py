def generate_reply(
    message: str,
    language: str = "hinglish",
    personality: str = "professional",
    history: list = None
) -> str:

    message = message.strip()
    history = history or []

    if not message:
        return "Please tell me something."

    previous_count = len(history)

    return (
        "JARVIS received your message: "
        + message
        + ". Language preference: "
        + language
        + ". Personality: "
        + personality
        + ". Previous messages received: "
        + str(previous_count)
        + ". Actual AI brain is not connected yet."
    )
    
