def generate_reply(message: str) -> str:
    """
    JARVIS ka AI brain.
    Filhaal temporary response dega.
    Baad mein Cloud AI ya Local AI connect karenge.
    """

    message = message.strip()

    if not message:
        return "Please tell me something."

    return (
        "I received your message: "
        + message
        + ". My AI brain is under development."
    )
