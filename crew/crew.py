from crewai import Crew, Process, LLM
from crewai.project import CrewBase, crew
from crew.agents import CrewAgents
from crew.tasks import CrewTasks


@CrewBase
class CrewCrew:
    
    def __init__(self):
        self.agents_obj = CrewAgents()
        self.tasks_obj = CrewTasks(self.agents_obj)
    
    def get_llm(self):
        return LLM(
            model="ollama/gpt-oss:20b",
            base_url="http://localhost:11434"
        )

    @crew
    def crew(self) -> Crew:
        """Creates new linkedin post generation crew"""

        return Crew(
            agents=[
                self.agents_obj.rag_agent(),
                self.agents_obj.researcher(),
                self.agents_obj.writer()
            ],
            tasks=[
                self.tasks_obj.rag_task(),
                self.tasks_obj.researcher(),
                self.tasks_obj.writer()
            ],
            process=Process.sequential,
            verbose=True,
            # planning=True,
            # planning_llm=self.get_llm()
        )
    