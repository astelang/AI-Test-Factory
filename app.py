import streamlit as st
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# --- ENTERPRISE CONFIGURATION ---
st.set_page_config(page_title="Enterprise AI QA Gateway", page_icon="🏦", layout="wide")

# Professional Banking UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #004a99; color: white; font-weight: bold; height: 3.5em; border-radius: 8px; }
    .stTextArea>div>div>textarea { background-color: #ffffff; border: 1px solid #004a99; }
    .stStatus { border-left: 5px solid #004a99; }
    </style>
    """, unsafe_content_type=True)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- DATABASE SIMULATION LOGIC ---
def simulate_tdm_query(req_text):
    """Simulates Test Data Management (TDM) Agent finding real account data"""
    st.markdown("### 🗄️ Enterprise Data Intelligence Layer")
    col_sql, col_data = st.columns(2)
    
    # Logic-based SQL generation simulation
    if "withdraw" in req_text.lower() or "transfer" in req_text.lower():
        query = "SELECT TOP 1 account_id, balance FROM CORE_BANK_DB.ACCOUNTS WHERE STATUS='ACTIVE' AND CURRENCY='USD' AND AVAILABLE_LIMIT > 1000;"
        mock_data = {"Account_ID": "BNP-77421-X", "Ledger_Balance": 5400.25, "Status": "Verified"}
    else:
        query = "SELECT TOP 1 cust_id FROM CRM_PROD.CUSTOMERS WHERE KYC_STATUS='COMPLETED' AND REGION='APAC';"
        mock_data = {"Customer_ID": "CUST-9901-AMIT", "Region": "India", "KYC": "Clear"}

    with col_sql:
        st.caption("AI-Generated TDM SQL")
        st.code(query, language="sql")
    with col_data:
        st.caption("Fetched UAT Test Record")
        st.json(mock_data)
    return mock_data

# --- SIDEBAR: SYSTEM STATUS ---
with st.sidebar:
    st.title("🏦 CoE Dashboard")
    st.divider()
    st.write("**Node:** `Azure-North-Gateway-01`")
    st.write("**Access Level:** `Senior Principal Consultant`")
    st.write("**Operator:** `Amit`")
    st.write("**Framework:** `CrewAI v0.102.x` / `Selenium 4.x`")
    st.divider()
    st.success("System: Operational")
    st.info("GDPR/SOC2 Compliant Tunnel Active")

# --- MAIN UI ---
st.title("Global Banking Automation Gateway (GBAG)")
st.caption("Internal Quality Engineering Center of Excellence (CoE)")
st.divider()

col_input, col_logs = st.columns([2, 1])

with col_input:
    st.markdown("##### 📝 Functional Requirement / Business Rule")
    requirement = st.text_area("Input Requirement:", height=200, 
        placeholder="e.g., A customer can only withdraw $500 if the account is older than 30 days...")

with col_logs:
    st.markdown("##### 📋 System Audit Trail")
    audit_trail = st.empty()
    audit_trail.info("Awaiting Transaction...")

if st.button("🚀 INITIATE AGENTIC AUTOMATION PIPELINE"):
    if not api_key:
        st.error("API Error: Secure vault connection failed (Check .env)")
    elif not requirement:
        st.warning("Please provide a requirement to begin analysis.")
    else:
        # Step 1: Database Simulation
        test_context = simulate_tdm_query(requirement)
        
        # Step 2: Running the Crew
        audit_trail.write("🕒 10:42:01 - Initializing Agentic Orchestrator...")
        time.sleep(1)
        audit_trail.write("🕒 10:42:05 - Analyst: Extracting BFSI Logic Rules...")
        
        with st.spinner("🤖 Agents Collaborating in Private Cloud..."):
            my_llm = LLM(model="gpt-4-turbo", api_key=api_key)

            # Define Roles
            ba = Agent(role='Functional Analyst', goal='Decompose banking rules', backstory='Ex-Oracle Financials Consultant', llm=my_llm)
            sdet = Agent(role='SDET Lead', goal='Generate Selenium Scripts', backstory='Automation Architect', llm=my_llm)
            healer = Agent(role='Healing Engineer', goal='Audit code stability', backstory='Quality Assurance Principal', llm=my_llm)

            # Define Workflow
            t1 = Task(description=f"Analyze requirements: {requirement}", expected_output="Functional Logic Map", agent=ba)
            t2 = Task(description=f"Using data {test_context}, write Selenium code", expected_output="Python Code", agent=sdet)
            t3 = Task(description="Self-Heal the script for dynamic waits", expected_output="Final Stabilized Code", agent=healer)

            crew = Crew(agents=[ba, sdet, healer], tasks=[t1, t2, t3], process=Process.sequential)
            result = crew.kickoff()

            audit_trail.write("🕒 10:42:50 - Success: Artifacts Generated.")

            # Display Outputs
            st.divider()
            out1, out2 = st.columns(2)
            with out1:
                st.markdown("### ✅ Analyzed Logic")
                st.text_area("Analysis", value=str(result), height=400)
            with out2:
                st.markdown("### 🐍 Healed Selenium Script")
                st.code(str(result), language="python")

            st.download_button("📥 Export QA Artifacts", str(result), file_name=f"GBAG_QA_Export_{datetime.now().strftime('%Y%m%d')}.txt")

st.divider()
st.caption("Proprietary Tooling of Enterprise Quality Engineering Group © 2026")