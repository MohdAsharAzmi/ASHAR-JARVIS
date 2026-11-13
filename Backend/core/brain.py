
import re


# ASHAR JARVIS — Independent Brain V1

AGENT_KEYWORDS = {
    "research": [
        "research", "search", "internet", "find information",
        "look up", "maloomat", "talash", "jaankari",
        "jankari", "latest news", "kis bare mein"
    ],
    "coding": [
        "code", "coding", "program", "python", "javascript",
        "html", "css", "debug", "error", "bug", "website",
        "web development", "programming"
    ],
    "creative": [
        "image", "photo", "picture", "video", "animation",
        "design", "poster", "thumbnail", "creative"
    ],
    "memory": [
        "remember", "save this", "forget", "memory",
        "yaad rakh", "yaad rakho", "bhool jao",
        "save kar lo", "delete memory"
    ]
}


def count_matches(text, keywords):
    score = 0

    for keyword in keywords:
        if " " in keyword:
            if keyword in text:
                score += 2
        else:
            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):
                score += 1

    return score


def select_agent(message):
    text = message.lower().strip()

    scores = {}

    for agent_name, keywords in AGENT_KEYWORDS.items():
        scores[agent_name] = count_matches(text, keywords)

    best_agent = max(scores, key=scores.get)

    if scores[best_agent] == 0:
        return "general"

    return best_agent


def generate_reply(
    message,
    language="hinglish",
    personality="professional",
    history=None
):
    message = message.strip()
    history = history or []

    if not message:
        return "Please tell me something."

    text = message.lower()

    # Greeting detection
    greetings = [
        "hello", "hi", "hey", "salam",
        "assalamualaikum", "good morning",
        "good evening"
    ]

    if any(word in text.split() for word in greetings):
        return (
            "Wa Alaikum Assalam! "
            "ASHAR JARVIS Independent Brain V1 is online. "
            "How can I help you?"
        )

    # Help command
    if text in ["help", "commands", "what can you do"]:
        return (
            "I am ASHAR JARVIS Independent Brain V1.\n\n"
            "Available modules:\n"
            "1. General Assistant\n"
            "2. Coding Agent\n"
            "3. Research Agent (not connected yet)\n"
            "4. Creative Agent (not connected yet)\n"
            "5. Memory Agent (not connected yet)\n\n"
            "My brain can identify your request and select "
            "the relevant module. More capabilities are coming."
        )

    # Select the correct agent
    selected_agent = select_agent(message)

    # General Assistant
    if selected_agent == "general":
        return (
            "I understood your message, but my language model "
            "is not connected yet.\n\n"
            "My independent brain is active. I can identify "
            "some types of requests and route them to modules.\n\n"
            "Tell me your request in a little more detail."
        )

    # Coding Agent
    if selected_agent == "coding":
        return (
            "Coding Agent selected.\n\n"
            "I can help organize coding tasks and understand "
            "basic programming requests. My full coding engine "
            "is still under development.\n\n"
            "Please share your code or explain what you want to build."
        )

    # Research Agent
    if selected_agent == "research":
        return (
            "Research Agent selected.\n\n"
            "Live internet search is not connected in this version. "
            "I will not pretend that I searched the internet.\n\n"
            "You can share text or information here for analysis."
        )

    # Creative Agent
    if selected_agent == "creative":
        return (
            "Creative Agent selected.\n\n"
            "I can help plan designs, image ideas and animation concepts. "
            "Direct image or video generation is not connected yet.\n\n"
            "Describe your creative idea."
        )

    # Memory Agent
    if selected_agent == "memory":
        return (
            "Memory Agent selected.\n\n"
            "Permanent memory storage is not connected yet. "
            "I will not claim that I saved or deleted anything.\n\n"
            "The memory module will be built in a later step."
        )

    return "Request received. ASHAR JARVIS is processing your message."
