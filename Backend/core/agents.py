
import os
from urllib.parse import urlparse
from google import genai
from google.genai import types


class GeneralAgent:
    def run(self, **kwargs):
        return {
            "agent": "general",
            "status": "ready"
        }


class ResearchAgent:

    def run(self, task: str = "", **kwargs):

        task = task.strip()

        if not task:
            raise ValueError("Research task cannot be empty")

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing.")

        model = os.getenv(
            "AI_MODEL",
            "gemini-2.5-flash"
        )

        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model=model,
                contents=(
                    "Research the following topic using Google Search. "
                    "Give a clear, accurate and detailed report. "
                    "Use current information where relevant. "
                    "Do not invent facts or sources. "
                    "Clearly mention uncertainty when information is unclear.\n\n"
                    "Research topic: " + task
                ),
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ],
                    temperature=1.0,
                    max_output_tokens=3000
                )
            )

            report = response.text or (
                "Gemini did not return a research report."
            )

            sources = []
            seen_urls = set()
            search_queries = []

            candidates = response.candidates or []

            if candidates:
                metadata = (
                    candidates[0].grounding_metadata
                )

                if metadata:
                    search_queries = (
                        metadata.web_search_queries or []
                    )

                    chunks = (
                        metadata.grounding_chunks or []
                    )

                    for chunk in chunks:

                        web_source = getattr(
                            chunk, "web", None
                        )

                        if not web_source:
                            continue

                        title = (
                            getattr(web_source, "title", "")
                            or "Web source"
                        )

                        url = (
                            getattr(web_source, "uri", "")
                            or ""
                        )

                        if not url:
                            continue

                        parsed_url = urlparse(url)

                        if parsed_url.scheme not in (
                            "http", "https"
                        ):
                            continue

                        if not parsed_url.netloc:
                            continue

                        normalized_url = url.rstrip("/").lower()

                        if normalized_url in seen_urls:
                            continue

                        seen_urls.add(normalized_url)

                        sources.append({
                            "title": title,
                            "url": url,
                            "domain": parsed_url.netloc
                        })

            return {
                "agent": "research",
                "status": "research_completed",
                "task": task,
                "model": model,
                "search_engine": "Google Search Grounding",
                "report": report,
                "total_sources": len(sources),
                "sources": sources,
                "search_queries": search_queries,
                "message": (
                    "Gemini research completed using "
                    "Google Search Grounding."
                )
            }

        except Exception as error:

    error_code = getattr(error, "code", "Unknown")
    error_message = getattr(error, "message", None)

    if not error_message:
        error_message = str(error)

    safe_message = str(error_message).replace(
        api_key,
        "[REDACTED]"
    )

    print("Research error type:", type(error).__name__)
    print("Research error code:", error_code)
    print("Research error details:", safe_message[:1000])

    raise RuntimeError(
        "Gemini research failed. Check Render logs."
    ) from None

class CodingAgent:
    def run(self, task: str = "", **kwargs):
        return {
            "agent": "coding",
            "status": "registered",
            "task": task,
            "message": "Coding capabilities are not connected yet."
        }


class CreativeAgent:
    def run(
        self,
        task: str = "",
        media_type: str = "image",
        **kwargs
    ):
        return {
            "agent": "creative",
            "status": "registered",
            "task": task,
            "media_type": media_type,
            "message": "Creative models are not connected yet."
        }


class MemoryAgent:
    def run(self, action: str = "status", **kwargs):
        return {
            "agent": "memory",
            "status": "registered",
            "action": action,
            "message": "Persistent memory storage is not connected yet."
        }


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


agent_manager = AgentManager()

agent_manager.register_agent("general", GeneralAgent())
agent_manager.register_agent("research", ResearchAgent())
agent_manager.register_agent("coding", CodingAgent())
agent_manager.register_agent("creative", CreativeAgent())
agent_manager.register_agent("memory", MemoryAgent())
