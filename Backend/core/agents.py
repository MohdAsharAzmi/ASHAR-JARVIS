
from urllib.parse import urlparse
from ddgs import DDGS


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

        try:
            search_results = DDGS(timeout=15).text(
                query=task,
                region="in-en",
                safesearch="moderate",
                max_results=8,
                backend="auto"
            )

            sources = []
            seen_urls = set()

            for item in search_results or []:

                title = item.get("title", "").strip()
                url = (
                    item.get("href")
                    or item.get("url")
                    or ""
                ).strip()

                snippet = (
                    item.get("body")
                    or item.get("snippet")
                    or ""
                ).strip()

                if not title or not url:
                    continue

                parsed_url = urlparse(url)

                if parsed_url.scheme not in ("http", "https"):
                    continue

                if not parsed_url.netloc:
                    continue

                normalized_url = url.rstrip("/").lower()

                if normalized_url in seen_urls:
                    continue

                seen_urls.add(normalized_url)

                sources.append({
                    "title": title,
                    "snippet": snippet,
                    "url": url,
                    "domain": parsed_url.netloc
                })

            return {
                "agent": "research",
                "status": (
                    "search_completed"
                    if sources else "no_results"
                ),
                "task": task,
                "search_engine": "DDGS metasearch",
                "total_sources": len(sources),
                "sources": sources,
                "message": (
                    "Web search completed. Results are "
                    "search listings, not independently "
                    "verified facts. Full webpage analysis "
                    "is not connected yet."
                    if sources else
                    "No search results were returned. "
                    "Please try again with different keywords."
                )
            }

        except Exception as error:

            print("Research search error:", str(error))

            raise RuntimeError(
                "Web research failed. Please retry later."
            ) from error


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
