from crewai import Agent, LLM
from crewai.project import CrewBase, agent
from crewai_tools import ScrapeWebsiteTool
from services.scrapers.remoteok import RemoteOk
from services.scraper import Scraper
from services.serper import SearchSerper
from services.write_to_file import WriteToFile
import yaml

@CrewBase
class CrewAgents:

    agents_config_path = "config/agents.yaml"

    def __init__(self):
        self.scraper_tool = Scraper(scrapers_list=[RemoteOk()])
        self.serper_tool = SearchSerper()
        self.filewriter = WriteToFile()

    def get_config(self):
        with open("crew/"+self.agents_config_path, "r") as f:
            agents_config = yaml.safe_load(f)
        return agents_config
    
    def get_llm(self):
        return LLM(
            model="ollama/gpt-oss:20b",
            base_url="http://localhost:11434"
        )

    @agent
    def scraper(self) -> Agent:
        config = self.get_config()
        return Agent(
            config=config['scraper'],   # type: ignore[index]
            tools=[self.scraper_tool],
            llm=self.get_llm()
        )
    
    @agent
    def researcher(self) -> Agent:
        config = self.get_config()
        return Agent(
            config=config['researcher'],   # type: ignore[index]
            tools=[self.serper_tool],
            llm=self.get_llm()
        )
    
    @agent
    def writer(self) -> Agent:
        config = self.get_config()
        return Agent(
            config=config['writer'],   # type: ignore[index]
            tools=[self.filewriter],
            llm=self.get_llm()
        )