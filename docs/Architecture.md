# 🏛️ Technical Architecture: GBAG Framework
**Project Name:** Global Banking Automation Gateway  
**Architect:** Amit, Senior Principal Consultant  

## 1. Overview
The **GBAG Framework** is an AI-orchestrated middleware designed to automate the 'Requirement-to-Test' lifecycle. By leveraging multi-agent systems, the platform eliminates the manual bottleneck between Business Analysts and SDETs.

## 2. System Components


### A. Interface Layer (Streamlit)
* Acts as the **Audit & Control Portal**.
* Allows human-in-the-loop verification of AI-generated logic.

### B. Intelligence Layer (CrewAI)
* **Functional Analyst Agent:** Interprets complex BFSI domain logic (Loans, Deposits, Payments).
* **SDET Lead Agent:** Translates logic into Selenium 4.0 Page Object Models.
* **Healing Engineer Agent:** Performs static code analysis to replace hardcoded delays with **Fluent/Explicit Waits**, ensuring 99% test stability.

### C. Data & TDM Layer (SQL Simulation)
* **Dynamic Data Extraction:** Instead of static variables, the system generates context-aware SQL to fetch valid test records from Oracle/SQL Server UAT environments.
* **Database Assertions:** Enables E2E validation by comparing UI results with Back-end Ledger entries.

### D. DevOps & CI/CD (GitHub Actions)
* **Serverless Execution:** Pushes generated artifacts to GitHub for automated nightly regression runs.
* **Versioned Artifacts:** Every requirement change produces a versioned test script, ensuring full traceability.

## 3. Security & Compliance
* **Credential Vaulting:** Integration with GitHub Secrets for API protection.
* **Private LLM Ready:** Designed to swap OpenAI for **Azure OpenAI Private Link** or **On-Premise Llama 3**, ensuring banking data never leaves the internal firewall.