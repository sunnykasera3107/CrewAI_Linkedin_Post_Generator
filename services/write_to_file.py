from crewai.tools import BaseTool
from datetime import datetime
import os

class WriteToFile(BaseTool):
    name: str = "Write to File"
    description: str = "Writes given content to a text file"

    def _run(self, content: str) -> str:
        print("✅ NEW WRITER RUNNING")
        filename = os.path.join("data/generated_posts", f"{datetime.now().strftime('%Y%m%d_%H%M%S')}-linkedin-post.txt")
        print(filename)
        try:
            with open(filename, "w") as file:
                file.write(content)
        except Exception as e:
            print(f"Error: {str(e)}")

        return f"Content successfully written to {filename}"
    

if __name__ == "__main__":
    writefile = WriteToFile()
    writefile._run("asldkfjasdlkf")