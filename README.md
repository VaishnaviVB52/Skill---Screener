# Jade Global AI-Powered - Skill Screener

Skill Screener is an AI-driven Talent Acquisition solution built to transform the traditional recruitment process.
It automates resume screening by matching candidate profiles with job descriptions using Azure OpenAI GPT models and presents ranked candidates based on their match score.

📌 Problem Statement
Recruiters often face:
a) Manual and time-consuming resume screening
b) Inconsistent candidate shortlisting
c) Delayed hiring decisions
d) Recruiter fatigue from processing large volumes

🚀 Solution Overview
a) JadeScreen streamlines this process by:
b) Uploading Job Descriptions (JD)
c) Uploading Candidate Resumes (PDF/DOCX)
d) Extracting text from documents
e) Comparing resumes with JD using Azure OpenAI
f) Generating a Match Score for each candidate
g) Displaying a ranked list of candidates using tabulate

⚙️ Architecture
Frontend: Streamlit web app
AI Engine: Azure OpenAI GPT model 
Document Parser: PyPDF2 for PDFs and python-docx for DOCX
Output Display: Tabulated ranked candidates using tabulate
Deployment: Easily deployable on Streamlit Cloud 

📊 Output
Ranked candidates displayed with columns:
a) Candidate Name
b) Match Score
c) Key Matching Keywords
d) Interactive UI to view and download results
