import streamlit as st
import os
import io
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# --- CONFIG ---
st.set_page_config(page_title="Enterprise QA Gateway | Excel Export", layout="wide")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- UI ---
st.title("🏦 Global QA Automation Gateway")
st.markdown("#### *Requirement-to-Excel Precision Engine*")
st.divider()

requirement_text = st.text_area("📝 Paste Requirement Text:", height=250)

if st.button("🚀 GENERATE EXCEL-READY TEST SUITE"):
    if not requirement_text:
        st.error("Requirement text is missing.")
    else:
        with st.spinner("Extracting logic into Excel format..."):
            
            my_llm = LLM(model="gpt-4-turbo", api_key=api_key, temperature=0.1)

            analyst = Agent(
                role='Principal QA Lead',
                goal='Generate structured CSV-compatible test cases',
                backstory='Expert in Test Management Tools (ALM, Jira Xray). Specialized in data-driven Excel exports.',
                llm=my_llm
            )

            # --- THE EXCEL-FORMAT TASK ---
            t1 = Task(
                description=f"""PROCESS REQUIREMENT: {requirement_text}
                
                Generate a DETAILED Test Matrix. 
                FORMATTING RULES FOR EXCEL:
                1. Output ONLY a table.
                2. Use the following columns: Scenario_Type, Step_ID, Action, Test_Data, Expected_Result.
                3. DO NOT use line breaks inside cells.
                4. Ensure 'Scenario_Type' identifies Positive, Negative, or Boundary cases.
                5. Escape any commas in the text to avoid CSV splitting errors.""",
                expected_output="A clean markdown table optimized for CSV conversion.",
                agent=analyst
            )

            crew = Crew(agents=[analyst], tasks=[t1], process=Process.sequential)
            result = crew.kickoff()

            # --- CONVERSION LOGIC FOR EXCEL ---
            # We take the raw markdown table and clean it for a real CSV download
            raw_output = str(result.tasks_output[0])
            
            st.divider()
            st.subheader("📊 Preview of Generated Test Cases")
            st.markdown(raw_output)

            # Creating a downloadable CSV that Excel actually likes
            # We strip the markdown pipes and convert to a clean string
            csv_data = raw_output.replace("|", ",").replace("-", "").strip()
            
            st.download_button(
                label="📥 DOWNLOAD FOR EXCEL (.csv)",
                data=csv_data,
                file_name=f"TestCases_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )

st.divider()
st.caption("© 2026 Amit | Senior Principal Consultant")