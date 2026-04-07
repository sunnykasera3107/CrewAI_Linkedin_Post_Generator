import requests, json
import time
import yaml

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

    def scrape(self):
        self._scrap_job_list_()
        
    
    def _scrap_job_list_(self):
        jobs = []

        for skill in self._config.get("skills"):
            try:
                req = self.session.get(
                    f"https://remoteok.com/api?tag={skill}",
                    timeout=10,
                    allow_redirects=True
                )
                job_list = req.json()
                jobs = jobs + job_list[1:]
            except Exception as e:
                print(f"error: {str(e)}")

            time.sleep(5)
        self._save_job_(jobs, "data/raw_jobs/remoteok_jobs.json")
        return jobs
    
    def _save_job_(self, jobs, file_name):
        try:
            with open(file_name, "w") as file:
                json.dump(jobs, file)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    remoteok = RemoteOk()
    remoteok.scrape()