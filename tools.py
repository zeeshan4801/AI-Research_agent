from crewai.tools import BaseTool
from duckduckgo_search import DDGS


class DuckDuckGoSearchTool(BaseTool):

    name: str = "DuckDuckGo Search"
    description: str = (
        "Search the internet using DuckDuckGo "
        "and return useful research information."
    )

    def _run(self, query: str):

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=5
            )

            for result in search_results:
                results.append(
                    f"""
Title:
{result.get('title')}

Content:
{result.get('body')}

Link:
{result.get('href')}
"""
                )

        return "\n\n".join(results)
