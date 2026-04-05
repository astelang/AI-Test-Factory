import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from langchain_openai import ChatOpenAI

# 1. LOAD CREDENTIALS
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")

# 2. INITIALIZE THE AI BRAIN (The "CrewAI" way to avoid Validation Errors)
# We wrap the model in the CrewAI LLM class to ensure compatibility
my_ai_brain = LLM(
    model=model_name,
    api_key=api_key
)

# 3. DEFINE THE AGENTS (The Personnel)

# Agent A: The Analyst (Logic)
analyst = Agent(
    role='Business Requirement Analyst',
    goal='Identify all business rules and logical conditions from the requirement.',
    backstory='Expert in banking and telecom functional specs. You find the core "If-Then" rules.',
    llm=my_ai_brain,
    verbose=True
)

# Agent B: The SDET (Gherkin & Selenium)
developer = Agent(
    role='Lead SDET Architect',
    goal='Convert rules into Gherkin scenarios and high-quality Python Selenium code.',
    backstory='Expert in BDD and Page Object Model. You write clean, executable automation scripts.',
    llm=my_ai_brain,
    verbose=True
)

# Agent C: The Healer (Stability)
healer = Agent(
    role='Self-Healing Engineer',
    goal='Audit the generated code for fragile locators and suggest robust fixes.',
    backstory='You prevent flaky tests by replacing weak XPaths with stable CSS selectors or IDs.',
    llm=my_ai_brain,
    verbose=True
)

# 4. READ THE REQUIREMENT FILE
# Ensure you have a file named 'input_requirement.txt' in your folder
with open("input_requirement.txt", "r") as file:
    user_requirement = file.read()

# 5. DEFINE THE TASKS (The Workflow)

task_analysis = Task(
    description=f"Analyze this requirement and list the logic: {user_requirement}",
    expected_output="A structured list of business rules and system states.",
    agent=analyst
)

task_automation = Task(
    description="Based on the rules, write Gherkin scenarios and a Python Selenium script.",
    expected_output="A professional Gherkin doc and a complete Python Selenium script.",
    agent=developer
)

task_healing = Task(
    description="Review the Selenium code and provide a 'Healed' version with stable locators.",
    expected_output="A report showing potential errors and the corrected, resilient code.",
    agent=healer
)

# 6. ASSEMBLE THE CREW
qa_crew = Crew(
    agents=[analyst, developer, healer],
    tasks=[task_analysis, task_automation, task_healing],
    process=Process.sequential
)

# 7. EXECUTE & SAVE
print("### STARTING THE SELF-HEALING QA FACTORY ###")
result = qa_crew.kickoff()

# Save the final output to a report file
with open("Final_AI_Test_Report.txt", "w") as f:
    f.write(str(result))

print("\n### SUCCESS: Final report saved to Final_AI_Test_Report.txt ###")