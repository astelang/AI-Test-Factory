import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# 1. CLOUD-AWARE CONFIGURATION
# Load local .env file if it exists (for VS Code)
# On GitHub, it will skip this and use the "Secrets" we set up
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo")

# CRITICAL CHECK: Ensure the key is present before starting
if not api_key or api_key == "***":
    print("❌ ERROR: OpenAI API Key is missing or invalid in the environment.")
    exit(1)

print(f"✅ Environment Check: Using model {model_name}")

# 2. INITIALIZE THE AI BRAIN
# We use the CrewAI LLM wrapper to prevent Pydantic Validation Errors
my_ai_brain = LLM(
    model=model_name,
    api_key=api_key
)

# 3. DEFINE THE AGENTS (The Personnel)

analyst = Agent(
    role='Business Requirement Analyst',
    goal='Identify all business rules and logical conditions from the requirement.',
    backstory='Expert in banking (BFSI) and telecom domains. You find core "If-Then" rules.',
    llm=my_ai_brain,
    verbose=True
)

developer = Agent(
    role='Lead SDET Architect',
    goal='Convert rules into Gherkin scenarios and high-quality Python Selenium code.',
    backstory='Expert in BDD (Behavior Driven Development). You write clean, executable scripts.',
    llm=my_ai_brain,
    verbose=True
)

healer = Agent(
    role='Self-Healing Engineer',
    goal='Audit the generated code for fragile locators and suggest robust fixes.',
    backstory='You prevent flaky tests by ensuring locators are resilient to UI changes.',
    llm=my_ai_brain,
    verbose=True
)

# 4. READ THE REQUIREMENT FILE
# This is the file that triggers the GitHub Action when changed
try:
    with open("input_requirement.txt", "r") as file:
        user_requirement = file.read()
except FileNotFoundError:
    user_requirement = "Default: User must be logged in to view balance."
    print("⚠️ Warning: input_requirement.txt not found. Using default.")

# 5. DEFINE THE TASKS

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

# 6. ASSEMBLE AND KICKOFF
qa_crew = Crew(
    agents=[analyst, developer, healer],
    tasks=[task_analysis, task_automation, task_healing],
    process=Process.sequential
)

print("### STARTING THE SELF-HEALING QA FACTORY ###")
result = qa_crew.kickoff()

# 7. SAVE THE OUTPUTS
# This saves the final report that GitHub Actions will "upload" as an artifact
with open("Final_AI_Test_Report.txt", "w") as f:
    f.write(str(result))

print("\n### SUCCESS: Final report saved to Final_AI_Test_Report.txt ###")