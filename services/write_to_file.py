from crewai.tools import BaseTool
from datetime import datetime
import os

class WriteToFile(BaseTool):
    name: str = "Write to File"
    description: str = "Writes given content to a text file"

    def _run(self, query: str) -> str:
        print("✅ NEW WRITER RUNNING")
        filename = os.path.join("data/generated_posts", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-linkedin-post.txt")
        try:
            with open(filename, "w") as file:
                file.write(self.clean_text(query))
        except Exception as e:
            print(f"Error: {str(e)}")

        return f"Content successfully written to {query}"
    
    def clean_text(self, text: str) -> str:
        return (
            text.replace("\u2011", "-")
                .replace("\u2013", "-")
                .replace("\u2014", "-")
        )

if __name__ == "__main__":
    writefile = WriteToFile()
    writefile._run("asldkfjasdlkf")