
class GeneralAgent:
    def run(self, **kwargs):
        return {"agent": "general", "status": "ready"}




class ResearchAgent:
    def run(self, task: str = "", **kwargs):
        task = task.strip()

        if not task:
            raise ValueError("Research task cannot be empty")

        params = {
            "action": "query",
            "list": "search",
            "srsearch": task,
            "srlimit": 5,
            "srprop": "snippet|timestamp",
            "format": "json",
            "formatversion": 2
        }

        url = (
            "https://en.wikipedia.org/w/api.php?"
            + urlencode(params)
        )

        request = Request(
            url,
            headers={
                "User-Agent": "AsharJARVIS/1.0 (research assistant)"
            }
        )

        try:
            with urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))

            results = data.get("query", {}).get("search", [])

            sources = []

            for item in results:
                title = item.get("title", "")
                snippet = unescape(
                    re.sub(
                        r"<[^>]+>",
                        "",
                        item.get("snippet", "")
                    )
                )

                sources.append({
                    "title": title,
                    "snippet": snippet,
                    "url": (
                        "https://en.wikipedia.org/wiki/"
                        + quote(title.replace(" ", "_"))
                    )
                })

            return {
                "agent": "research",
                "status": "search_completed",
                "task": task,
                "total_sources": len(sources),
                "sources": sources,
                "message": (
                    "Wikipedia search completed. "
                    "These are search results, not a verified final report."
                )
            }

        except (HTTPError, URLError, TimeoutError) as error:
            raise RuntimeError(
                "Wikipedia search failed: " + str(error)
            )




class CodingAgent:
    def run(self, task: str = "", **kwargs):
        return {
            "agent": "coding",
            "status": "registered",
            "task": task,
            "message": "Coding capabilities are not connected yet."
        }


class CreativeAgent:
    def run(self, task: str = "", media_type: str = "image", **kwargs):
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
