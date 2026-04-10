import requests, json
import time
import yaml
from bs4 import BeautifulSoup

class RemoteOk:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        with open("config/settings.yaml", "r") as f:
            self._config = yaml.safe_load(f)

    def scrape(self, query):
        self.query = query
        self._scrap_job_list_()
        
    
    def _scrap_job_list_(self):
        jobs = []
        
        try:
            for skill in self._config.get("skills"):
                print(f"https://remoteok.com/api?tag={skill}")
                req = self.session.get(
                    f"https://remoteok.com/api?tag={skill}",
                    timeout=10,
                    allow_redirects=True
                )
                job_list = req.json()

                for job in job_list[1:2]:
                    new_job = []
                    for col in self._config.get("data"):
                        soup = BeautifulSoup(job.get(col) if col != "tags" else ",".join(job.get(col)), "html.parser")
                        clean_text = soup.get_text(separator=" ", strip=True) 
                        new_job.append(f"{col}: {clean_text}")
                    if len(new_job) > 0:
                        jobs.append("\n".join(new_job))
                    
        except Exception as e:
            print(f"error: {str(e)}")

        time.sleep(5)
        self._save_job_("\n\n".join(jobs), f"data/raw_jobs/{self.query}-remoteok_jobs.txt")
        return "\n\n".join(jobs)
    
    def _save_job_(self, jobs, file_name):
        try:
            with open(file_name, "w") as file:
                json.dump(jobs, file)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    remoteok = RemoteOk()
    remoteok.scrape()