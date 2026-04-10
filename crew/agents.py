from crewai import Agent, LLM
from crewai.project import CrewBase, agent
from services.serper import SearchSerper
from services.write_to_file import WriteToFile
from services.rag_pipeline import RAGPipeline
import yaml

@CrewBase
class CrewAgents:

    agents_config_path = "config/agents.yaml"

    def __init__(self):
        self.serper_tool = SearchSerper()
        self.filewriter = WriteToFile()
        self.rag_pipeline = RAGPipeline()

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
    def rag_agent(self) -> Agent:
        config = self.get_config()
        return Agent(
            config=config['rag_agent'],   # type: ignore[index]
            tools=[self.rag_pipeline],
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