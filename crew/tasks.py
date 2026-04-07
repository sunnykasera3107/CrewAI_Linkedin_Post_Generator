from crewai import Task
from crewai.project import CrewBase, task
from crew.agents import CrewAgents
import yaml

@CrewBase
class CrewTasks:

    tasks_config_path = "config/tasks.yaml"

    def __init__(self, agents_obj: CrewAgents = CrewAgents()):
        self.agents_obj = agents_obj

    def get_config(self):
        with open("crew/"+self.tasks_config_path, "r") as f:
            tasks_config = yaml.safe_load(f)
        return tasks_config
    
    @task
    def scraper(self) -> Task:
        config = self.get_config()
        return Task(
            config=config['scraper_task'],    # type: ignore[index]
            agent=self.agents_obj.scraper()
        )
    
    @task
    def researcher(self) -> Task:
        config = self.get_config()
        return Task(
            config=config['researcher_task'],   # type: ignore[index]
            agent=self.agents_obj.researcher(),
            context=[self.scraper()]
        )
    
    @task
    def writer(self) -> Task:
        config = self.get_config()
        return Task(
            config=config['writer_task'],   # type: ignore[index]
            agent=self.agents_obj.writer(),
            context=[self.researcher()] 
        )
    
    
    
