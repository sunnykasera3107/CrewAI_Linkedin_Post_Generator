import os, json
import serpapi
from crewai.tools import BaseTool

from utilities import convert_json_txt

class SearchSerper(BaseTool):
    name: str ="Search using serper"
    description: str ="Search for user query using serper"
    
    def _run(self, query: str) -> str:
        print("✅ NEW SERPER RUNNING")
        self._client = serpapi.Client(api_key=os.getenv("SERPER_API_KEY"))
        results = self._client.search({
            "engine": "google",
            "google_domain": "google.com",
            "q": query,
            "num": 5
        })

        searched_results = []

        for result in results['organic_results']:
            searched_results.append({
                "title": result.get("title"),
                "link": result.get("link"),
                "snippet": result.get("snippet")
            })

        return convert_json_txt(searched_results)
    


if __name__ == "__main__":
    serper_tool = SearchSerper()
    print(serper_tool._run("site:remoteok.io Python developer"))
    