from crew.crew import CrewCrew
# import yaml, os
def main():
    crew = CrewCrew()
    skill = input("Enter number of skill only one at a time: ")
    crew.crew().kickoff(inputs={"query": skill})
    print("Linkedin post generated")


if __name__ == "__main__":
    main()