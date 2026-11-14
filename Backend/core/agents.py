
import os
import re

from core.memory_store import (
    save_memory,
    get_memories,
    search_memories,
    delete_memory
)

from core.providers import get_ai_provider


# ==========================================
# GENERAL AGENT
# ==========================================

class GeneralAgent:

    def run(self, message="", **kwargs):

        return {
            "agent": "general",
            "status": "ready",
            "task": message,
            "message": "General Assistant is ready."
        }


# ==========================================
# RESEARCH AGENT
# ==========================================

class ResearchAgent:

    def run(self, task="", **kwargs):

        task = (task or "").strip()

        if not task:
            raise ValueError("Research task cannot be empty")

        return {
            "agent": "research",
            "status": "offline_mode",
            "task": task,
            "analysis": {
                "topic": task,
                "word_count": len(task.split()),
                "research_type": "general research"
            },
            "research_plan": [
                "Understand the research question",
                "Identify important subtopics",
                "Collect reliable information",
                "Compare available evidence",
                "Prepare a final report"
            ],
            "message": (
                "Research Agent analysed your request. "
                "Live internet search is not connected yet."
            )
        }


# ==========================================
# CODING AGENT V6
# ==========================================

class CodingAgent:

    def run(self, task="", **kwargs):

        task = (task or "").strip()

        if not task:
            raise ValueError("Coding task cannot be empty")

        text = task.lower()

        # LANGUAGE DETECTION

        languages = {
            "python": ["python", ".py"],
            "javascript": ["javascript", ".js"],
            "html": ["html", ".html"],
            "css": ["css", ".css"],
            "java": ["java", ".java"],
            "c++": ["c++", "cpp"],
            "c": ["language c"]
        }

        detected_language = "not specified"

        for language, keywords in languages.items():

            for word in keywords:

                if word.startswith("."):

                    if word in text:
                        detected_language = language
                        break

                elif re.search(
                    r"\b" + re.escape(word) + r"\b",
                    text
                ):

                    detected_language = language
                    break

            if detected_language != "not specified":
                break

        # TASK TYPE DETECTION

        if any(word in text for word in [
            "debug",
            "error",
            "bug",
            "fix",
            "not working",
            "problem"
        ]):

            task_type = "debugging"

        elif any(word in text for word in [
            "explain",
            "meaning",
            "samjhao",
            "how does",
            "what is",
            "variables",
            "variable",
            "data type",
            "data types",
            "datatype",
            "datatypes",
            "print",
            "input",
            "output"
        ]):

            task_type = "code explanation"

        elif any(word in text for word in [
            "write code",
            "generate code",
            "code likho",
            "code banao"
        ]):

            task_type = "code generation"

        elif any(word in text for word in [
            "build",
            "create",
            "make",
            "develop",
            "website",
            "project"
        ]):

            task_type = "project development"

        else:

            task_type = "coding assistance"

        # ======================================
        # PYTHON PRINT + INPUT
        # ======================================

        has_print = (
            "print" in text
            or "output" in text
        )

        has_input = (
            "input" in text
            or "user input" in text
        )

        if (
            detected_language == "python"
            and task_type == "code explanation"
            and has_print
            and has_input
        ):

            return {
                "agent": "coding",
                "status": "offline_answer",
                "programming_language": "python",
                "task_type": "code explanation",
                "topic": "print and input",
                "answer": """
PYTHON PRINT() AND INPUT()

1. print()

print() ka use screen par output
dikhane ke liye hota hai.

Example:

print("Hello World")

Output:

Hello World


2. input()

input() ka use user se information
lene ke liye hota hai.

Example:

name = input("Enter your name: ")

Yahan user apna naam enter karega.


3. PRINT() + INPUT() TOGETHER

Dono functions ko ek saath use kar sakte hain.

Example:

name = input("Enter your name: ")

print("Hello", name)

Agar user Ashar enter karta hai,
to output hoga:

Hello Ashar


IMPORTANT:

input() normally data ko string ke form
mein return karta hai.

Agar number lena ho:

age = int(input("Enter age: "))

Decimal number ke liye float() use karo:

price = float(input("Enter price: "))


PRACTICE:

Ek program banao jo:

1. User se uska favourite game pooche.
2. Us game ka naam variable mein store kare.
3. print() se game ka naam display kare.
""",
                "message": "Coding Agent V6 answered offline."
            }

        # ======================================
        # PYTHON PRINT
        # ======================================

        if (
            detected_language == "python"
            and task_type == "code explanation"
            and has_print
        ):

            return {
                "agent": "coding",
                "status": "offline_answer",
                "programming_language": "python",
                "task_type": "code explanation",
                "topic": "print",
                "answer": """
PYTHON PRINT()

Python mein print() function ka use
screen par output display karne ke liye hota hai.

Example:

print("Hello World")

Output:

Hello World


Numbers bhi display kar sakte hain:

print(100)

Output:

100


Variables bhi print kar sakte hain:

name = "Ashar"

print(name)

Output:

Ashar


Multiple values:

name = "Ashar"
score = 100

print(name, score)

Output:

Ashar 100


PRACTICE:

print() ka use karke apna naam
aur favourite subject display karo.
""",
                "message": "Coding Agent V6 answered offline."
            }

        # ======================================
        # PYTHON INPUT
        # ======================================

        if (
            detected_language == "python"
            and task_type == "code explanation"
            and has_input
        ):

            return {
                "agent": "coding",
                "status": "offline_answer",
                "programming_language": "python",
                "task_type": "code explanation",
                "topic": "input",
                "answer": """
PYTHON INPUT()

Python mein input() function ka use
user se information lene ke liye hota hai.

Example:

name = input("Enter your name: ")

print(name)


PROGRAM KAISE KAAM KARTA HAI?

1. input() user se naam poochta hai.
2. User apna naam enter karta hai.
3. Naam variable mein store hota hai.
4. print() naam ko display karta hai.


IMPORTANT:

input() se milne wali value default
roop se string hoti hai.

Number ke liye int() use karo:

age = int(input("Enter age: "))

Decimal number ke liye float() use karo:

price = float(input("Enter price: "))


PRACTICE:

Ek program banao jo user se uska
favourite colour pooche aur phir
print() se colour display kare.
""",
                "message": "Coding Agent V6 answered offline."
            }

        # ======================================
        # PYTHON DATA TYPES
        # ======================================

        if (
            detected_language == "python"
            and task_type == "code explanation"
            and any(word in text for word in [
                "data type",
                "data types",
                "datatype",
                "datatypes"
            ])
        ):

            return {
                "agent": "coding",
                "status": "offline_answer",
                "programming_language": "python",
                "task_type": "code explanation",
                "topic": "data types",
                "answer": """
PYTHON DATA TYPES

Data type batata hai ki variable mein
kis tarah ka data store hai.

1. int

Integer numbers ke liye.

Example:
age = 18

2. float

Decimal numbers ke liye.

Example:
price = 99.5

3. str

Text store karne ke liye.

Example:
name = "Ashar"

4. bool

True ya False values ke liye.

Example:
is_active = True

5. list

Multiple values store karne ke liye.

Example:
games = ["Minecraft", "Chess"]

6. tuple

Ordered values ka collection.

Example:
colors = ("Red", "Blue")

7. dict

Key-value pairs store karne ke liye.

Example:
student = {
    "name": "Ashar",
    "score": 100
}

8. set

Unique values ka collection.

Example:
numbers = {1, 2, 3}

DATA TYPE CHECK KARNA

type() function se data type check
kar sakte hain.

Example:

score = 100

print(type(score))
""",
                "message": "Coding Agent V6 answered offline."
            }

        # ======================================
        # PYTHON VARIABLES
        # ======================================

        if (
            detected_language == "python"
            and task_type == "code explanation"
            and any(word in text for word in [
                "variable",
                "variables"
            ])
        ):

            return {
                "agent": "coding",
                "status": "offline_answer",
                "programming_language": "python",
                "task_type": "code explanation",
                "topic": "variables",
                "answer": """
PYTHON VARIABLES

Variable ek container ki tarah hota hai
jisme hum data store karte hain.

Example:

name = "Ashar"
score = 100
city = "Lucknow"

Yahan:

- name mein Ashar store hai.
- score mein 100 store hai.
- city mein Lucknow store hai.

Python mein variable banane ke liye
alag se data type declare nahi karna padta.

Example:

score = 100
score = 200

Ab score ki value 200 hai.

VARIABLE NAMING RULES

- Naam letter ya underscore se shuru hona chahiye.
- Naam number se shuru nahi ho sakta.
- Spaces allowed nahi hain.
- Python keywords ko variable name nahi bana sakte.
""",
                "message": "Coding Agent V6 answered offline."
            }

        # ======================================
        # OPTIONAL EXTERNAL AI
        # ======================================

        external_ai_allowed = (
            os.getenv(
                "ALLOW_EXTERNAL_AI",
                "false"
            ).lower() == "true"
        )

        provider_name = os.getenv(
            "AI_PROVIDER",
            "offline"
        ).lower()

        if external_ai_allowed and provider_name != "offline":

            try:

                provider = get_ai_provider()

                prompt = (
                    "You are a professional coding tutor. "
                    "Explain programming concepts clearly. "
                    "Use simple Hinglish when appropriate. "
                    "Give accurate examples and explain them. "
                    "User request: " + task
                )

                answer = provider.generate(
                    message=prompt,
                    language="hinglish",
                    personality="professional",
                    history=[]
                )

                return {
                    "agent": "coding",
                    "status": "ai_response",
                    "programming_language": detected_language,
                    "task_type": task_type,
                    "answer": answer,
                    "message": "Coding Agent used the configured AI provider."
                }

            except Exception as error:

                print(
                    "Coding AI error:",
                    str(error)
                )

        # ======================================
        # OFFLINE GUIDANCE
        # ======================================

        guidance = {
            "debugging": [
                "Read the complete error message.",
                "Check the line number.",
                "Check spelling and syntax.",
                "Check variable names.",
                "Test the code again."
            ],

            "code explanation": [
                "Identify the programming concept.",
                "Understand its purpose.",
                "Study a small example.",
                "Run the example.",
                "Modify it and observe the result."
            ],

            "code generation": [
                "Understand the required output.",
                "Plan the program structure.",
                "Choose the required language.",
                "Build the solution step by step.",
                "Test the final program."
            ],

            "project development": [
                "Define project requirements.",
                "Plan the file structure.",
                "Build the basic interface.",
                "Implement project functionality.",
                "Test and improve the project."
            ],

            "coding assistance": [
                "Identify the programming language.",
                "Understand the problem.",
                "Break it into smaller steps.",
                "Test a small solution.",
                "Improve the implementation."
            ]
        }

        return {
            "agent": "coding",
            "status": "offline_guidance",
            "programming_language": detected_language,
            "task_type": task_type,
            "task": task,
            "guidance": guidance[task_type],
            "message": (
                "Coding Agent V6 prepared offline guidance. "
                "This request needs a more advanced coding engine "
                "for a complete solution."
            )
        }


# ==========================================
# CREATIVE AGENT
# ==========================================

class CreativeAgent:

    def run(self, task="", media_type="image", **kwargs):

        task = (task or "").strip()

        if not task:
            raise ValueError("Creative task cannot be empty")

        allowed_types = [
            "image",
            "video",
            "animation",
            "design"
        ]

        if media_type not in allowed_types:
            media_type = "image"

        return {
            "agent": "creative",
            "status": "concept_prepared",
            "task": task,
            "media_type": media_type,
            "creative_plan": [
                "Understand the creative requirement",
                "Identify the visual style",
                "Plan the composition",
                "Choose colours and typography",
                "Prepare the final creative direction"
            ],
            "message": (
                "Creative Agent prepared a "
                + media_type
                + " project plan. Generation tools are not connected yet."
            )
        }


# ==========================================
# MEMORY AGENT
# ==========================================

class MemoryAgent:

    def run(self, action="status", task="", **kwargs):

        task = (task or "").strip()
        text = task.lower()

        if text.startswith((
            "save:",
            "remember:",
            "yaad rakho:"
        )):

            content = task.split(":", 1)[1].strip()

            if not content:
                raise ValueError("Memory content is empty")

            result = save_memory(content)

            return {
                "agent": "memory",
                "status": "saved",
                "memory": result,
                "message": "Memory successfully saved."
            }

        if text.startswith((
            "search:",
            "find:"
        )):

            query = task.split(":", 1)[1].strip()

            results = search_memories(query)

            return {
                "agent": "memory",
                "status": "search_completed",
                "results": results,
                "message": "Memory search completed."
            }

        if text in (
            "list",
            "show",
            "show all",
            "list memories"
        ):

            results = get_memories()

            return {
                "agent": "memory",
                "status": "retrieved",
                "total": len(results),
                "memories": results,
                "message": "Saved memories retrieved."
            }

        if text.startswith("delete:"):

            memory_id = task.split(":", 1)[1].strip()

            if not memory_id.isdigit():
                raise ValueError("Provide a valid memory ID")

            deleted = delete_memory(int(memory_id))

            return {
                "agent": "memory",
                "status": "deleted" if deleted else "not_found",
                "memory_id": int(memory_id),
                "message": (
                    "Memory deleted."
                    if deleted
                    else "Memory ID not found."
                )
            }

        return {
            "agent": "memory",
            "status": "waiting_for_command",
            "supported_commands": [
                "save: your information",
                "search: keyword",
                "list",
                "delete: memory_id"
            ],
            "message": "Please use a supported memory command."
        }


# ==========================================
# AGENT MANAGER
# ==========================================

class AgentManager:

    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def get_agent(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    def run_agent(self, name, **kwargs):

        agent = self.get_agent(name)

        if agent is None:
            raise ValueError("Agent not found: " + name)

        if not hasattr(agent, "run"):
            raise TypeError("Agent does not have a run method")

        return agent.run(**kwargs)


# ==========================================
# REGISTER ALL AGENTS
# ==========================================

agent_manager = AgentManager()

agent_manager.register_agent(
    "general",
    GeneralAgent()
)

agent_manager.register_agent(
    "research",
    ResearchAgent()
)

agent_manager.register_agent(
    "coding",
    CodingAgent()
)

agent_manager.register_agent(
    "creative",
    CreativeAgent()
)

agent_manager.register_agent(
    "memory",
    MemoryAgent()
)
