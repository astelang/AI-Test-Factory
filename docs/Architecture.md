# 🏛️ Enterprise System Architecture: GBAG

## 1. High-Level Design
The **Global Banking Automation Gateway (GBAG)** is an AI-native middleware designed to bridge the gap between Business Requirements and Automated Regression Suites.

## 2. Core Components
* **Interface Layer:** Streamlit-based Enterprise Portal for manual overrides and auditing.
* **Intelligence Layer:** Multi-Agent Orchestration using **CrewAI**.
    * *Analyst Node:* Business Logic extraction.
    * *SDET Node:* Automation code generation.
    * *Healer Node:* Predictive stability auditing.
* **DevOps Layer:** GitHub Actions for serverless execution and artifact versioning.

## 3. Data Privacy & Security
To comply with banking regulations (GDPR/SOC2):
* **LLM Agnostic:** Supports Azure OpenAI (Private Link) or On-Premise Llama 3 via Ollama.
* **Credential Masking:** All API keys and environment variables are managed via GitHub Secrets and local `.env` encryption.