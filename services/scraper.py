import os, json, yaml
from typing import List, Any
# from scrapers.remoteok import RemoteOk

class Scraper:

    def __init__(self, query: str, scrapers_list: List[Any] = []):
        self.scrapers_list = scrapers_list
        self._raw_path = "data/raw_jobs"
        # self._filtered_path = "data/filtered_jobs"
        self._run_(query)

    def scrape(self, query):
        with open("config/settings.yaml", "r") as f:
            self._config = yaml.safe_load(f)

        if self.scrapers_list:
            for scraper in self.scrapers_list:
                scraper.scrape(query)
                        
        # job_list = ""
        # for filepath in os.listdir(self._raw_path):
        #     filepath = os.path.join(self._raw_path, filepath)
        #     try:
        #         with open(filepath, "r") as f:
        #             job_list = json.load(f)
        #     except Exception:
        #         pass
  
        # file_path = os.path.join(self._filtered_path, "jobs.json")
        # self._save_processed_job_(job_list, file_path)

        # return json.dumps(job_list)

    def _save_processed_job_(self, jobs, file_name):
        try:
            with open(file_name, "w") as file:
                json.dump(jobs, file)
        except Exception as e:
            print(f"Error: {str(e)}")
    
    def _run_(self, query):
        print("✅ NEW SCRAPER RUNNING")
        return self.scrape(query)

if __name__ == "__main__":
    # sc = Scraper(scrapers_list=[RemoteOk()])
    # print(sc)
    pass