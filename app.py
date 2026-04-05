import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI QA Factory", page_icon="🤖", layout="wide")

# --- LOAD API KEY ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- UI HEADER ---
st.title("🚀 Autonomous QA Test Factory")
st.markdown("### From Requirement to Selenium Code in Seconds")
st.info("Enter your business requirement below to trigger the AI Agent Crew.")

# --- INPUT AREA ---
user_input = st.text_area("Business Requirement:", 
    placeholder="e.g., A user should only be able to transfer funds if their account balance is above $1000.")

if st.button("Generate Automation Suite"):
    if not api_key:
        st.error("API Key missing! Please check your .env file.")
    elif not user_input:
        st.warning("Please enter a requirement first.")
    else:
        with st.spinner("🤖 The Crew is working... (Analyst, SDET, and Healer are collaborating)"):
            
            # 1. Setup Brain
            my_llm = LLM(model="gpt-4-turbo", api_key=api_key)

            # 2. Define Agents (Simplified for UI speed)
            analyst = Agent(role='Analyst', goal='Extract logic', backstory='Expert BA', llm=my_llm)
            developer = Agent(role='SDET', goal='Write Selenium', backstory='Expert Coder', llm=my_llm)
            healer = Agent(role='Healer', goal='Fix code', backstory='QA Lead', llm=my_llm)

            # 3. Define Tasks
            t1 = Task(description=f"Analyze: {user_input}", expected_output="Business rules list", agent=analyst)
            t2 = Task(description="Write Selenium Python code", expected_output="Python script", agent=developer)
            t3 = Task(description="Heal the code for stability", expected_output="Final stabilized Python code", agent=healer)

            # 4. Run Crew
            crew = Crew(agents=[analyst, developer, healer], tasks=[t1, t2, t3], process=Process.sequential)
            result = crew.kickoff()

            # --- DISPLAY RESULTS ---
            st.success("✅ Generation Complete!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 AI Analysis & Test Cases")
                st.text_area("Report Output", value=str(result), height=400)
            
            with col2:
                st.subheader("🐍 Generated Selenium Code")
                # We tell Streamlit this is Python code for nice coloring
                st.code(str(result), language="python")

            st.download_button("Download Full Report", str(result), file_name="AI_QA_Report.txt")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Project Info")
    st.write("Built by: Amit")
    st.write("Role: Senior Principal Consultant")
    st.write("Tech: CrewAI + Streamlit + Selenium")