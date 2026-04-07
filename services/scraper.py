import os, json, yaml
from crewai.tools import BaseTool
from typing import List, Any

class Scraper(BaseTool):
    name: str ="scraping_job_titles"
    description: str ="Scraping Job titles and skills sets"

    scrapers_list: List[Any] = []
    _raw_path = "data/raw_jobs"
    _filtered_path = "data/filtered_jobs"

    def scrape(self):
        with open("config/settings.yaml", "r") as f:
            self._config = yaml.safe_load(f)

        if self.scrapers_list:
            for scraper in self.scrapers_list:
                scraper.scrape()
                
        jobs = []
        for filepath in os.listdir(self._raw_path):
            filepath = os.path.join(self._raw_path, filepath)
            try:
                with open(filepath, "r") as f:
                    job_list = json.load(f)
            except Exception:
                pass

            # keys = self._config.get("data")
            for job in job_list:
                for skill in self._config.get("skills"):
                    if skill in job.get("position"):
                        jobs.append(job.get("position"))
  
        file_path = os.path.join(self._filtered_path, "jobs.json")
        self._save_processed_job_(jobs, file_path)

        return ", ".join(jobs[:3])
    
    def _save_processed_job_(self, jobs, file_name):
        try:
            with open(file_name, "w") as file:
                json.dump(jobs, file)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _run(self, query: str):
        print("✅ NEW SCRAPER RUNNING")
        return self.scrape()

if __name__ == "__main__":
    sc = Scraper()
    sc.scrape()