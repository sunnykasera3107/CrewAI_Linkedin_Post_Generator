from crew.crew import CrewCrew
import yaml

def main():
    crew = CrewCrew()
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    skills = {"skills": ",".join(config.get("skills"))}
    print(skills)
    crew.crew().kickoff(inputs=skills)
    print("Linkedin post generated")


if __name__ == "__main__":
    main()