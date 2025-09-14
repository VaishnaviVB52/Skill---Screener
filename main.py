import streamlit as st
import openai
import pandas as pd
from io import StringIO
from PyPDF2 import PdfReader
from openai import AzureOpenAI
import os
from PIL import Image
from docx import Document
from zipfile import BadZipFile
from tabulate import tabulate

jadeimage = Image.open("assets/jadelogo.png")
st.set_page_config(page_title="JadeScreener",page_icon=jadeimage,layout="wide")

client = AzureOpenAI(
    api_version=st.secrets["AZURE_OPENAI_API_VERSION"],
    api_key=st.secrets["AZURE_OPENAI_API_KEY"],
    azure_endpoint=st.secrets["AZURE_OPENAI_API_BASE"],

)
deployment_name = "hackathon-group4"  
st.set_page_config(page_title="Jade Skill Screener", layout="wide")

# ---- HEADER ----
st.title("🤖 AI-Powered Skill Screener")
st.markdown("**Accelerating hiring decisions with AI-driven intelligence.**")

# ---- FILE UPLOAD ----
with st.sidebar:
	image = Image.open("assets/skillimage.png")
	image = st.image('assets/skillimage.png',width=280)
	resume_files = st.file_uploader("📂 Upload Resumes (pdf)", type=["pdf","docx"], accept_multiple_files=True)
jd_text = st.chat_input("Enter your job description here:")

if jd_text is not None and jd_text.strip() != "":
	def extract_text_from_file(uploaded_file):
	    file_name = uploaded_file.name.lower()
	    
	    try:
	        if file_name.endswith(".pdf"):
	            reader = PdfReader(uploaded_file)
	            text = "\n".join(page.extract_text() or "" for page in reader.pages)
	
	        elif file_name.endswith(".docx"):
	            try:
	                doc = Document(uploaded_file)
	                text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
	            except KeyError as e:
	                # Corrupted DOCX with missing media
	                text = "(Could not fully read DOCX - some media missing)"
	            except BadZipFile:
	                text = "(Invalid DOCX file format)"
	                
	        else:  # assume .txt
	            text = uploaded_file.read().decode("utf-8")
	
	    except Exception as e:
	        text = f"(Error reading file: {str(e)})"
	    
	    return text
	
	if resume_files:
	    resumes = [(file.name, extract_text_from_file(file)) for file in resume_files]
	
	    with st.spinner("Analyzing resumes with AI..."):
	        results = []
	        for name, resume_text in resumes:
	            prompt = f"""
	            You are an AI assistant helping a Talent Aquation Team. Match the following candidate resume with the job description which is given as input by user.
	            Provide a match score (0-100) and highlight key missing skills if any.
	
	            Job Description:
	            {jd_text}
	
	            Candidate Resume:
	            {resume_text}
	
	            Return your output as JSON with fields: match_score, missing_skills (comma separated), summary (1-2 sentences).
	            """
	
	            response = client.chat.completions.create(
	                model=deployment_name,
	                max_completion_tokens=16384,
	                messages=[{"role": "system", "content": "You are a helpful AI recruiter assistant."},
	                         {"role": "user", "content": prompt}]
	            )
	            try:
	                content = response.choices[0].message.content
	                # st.write(content)
	                data = eval(content) if content.strip().startswith('{') else {}
	                results.append({
	                    "Candidate": name,
	                    "Match Score": data.get("match_score", 0),
	                    "Missing Skills": data.get("missing_skills", ""),
	                    "Summary": data.get("summary", "")
	                })
	            except Exception as e:
	                results.append({
	                    "Candidate": name,
	                    "Match Score": "Error",
	                    "Missing Skills": "Error parsing",
	                    "Summary": str(e)
	                })
	
	        df = pd.DataFrame(results)
	        df = df.sort_values(by="Match Score", ascending=False)
	        st.subheader("📊 Ranked Candidates")
	        st.dataframe(df, use_container_width=True)
			# table = tabulate(df, headers="keys", tablefmt="pretty", showindex=False)
			# st.text(table)
	        best_candidate = df.iloc[0]
	        st.success(f"Top Candidate: **{best_candidate['Candidate']}** with Match Score **{best_candidate['Match Score']}%**")
	
	else:
	    st.info("Please upload a Job Description and at least one Resume to begin analysis.")
else:
    st.write("Kindly provide the job description before proceeding.")
