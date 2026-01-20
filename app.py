import streamlit as st
from pdf_extracter import text_extractor #  importing a function from different file
from langchain_google_genai import ChatGoogleGenerativeAI
import os


# First Let's configure the model

gemini_api_key = os.getenv("project-testing")
model = ChatGoogleGenerativeAI(model = 'gemini-2.5-flash-lite',api_key = gemini_api_key,temperature=0.9)

# Let's create the sidebar to upload the resume

st.sidebar.title(':red[Upload your Resume here(ONLY PDF format)]')
file = st.sidebar.file_uploader('Resume',type = ['pdf']) # for uploading a resume in this file
if file:
    file_text = text_extractor(file) # calling the function from pdf_extracter.py file
    st.sidebar.success("File uploaded Successfully!")


# Create the Main page of the application

st.title(":blue[SKILL MATCH :-] :rainbow[Your AI-Powered Resume Analyzer TOOL]")
st.markdown("##### :red[This application will help you to analyze your resume and job description and give you the feedback based on the job description you provide.]",width='content')
tips = '''
Follow these steps:
1. Upload your resume in the pdf format using sidebar.
2. Copy and paste the job Description below.
3. Click on submit to run the application.'''

st.markdown(tips)

job_desc = st.text_area(":green[Copy and  Paste your Job Description here :-]",max_chars=50000)

if st.button("Submit"):
    with st.spinner("processing..."):
        prompt = f'''
        <Role> You are an expert in analyzing resume and matching it with job description.
        <Goal> Match the resume with the job description provided by the the applicant and create a report.
        <Context> The following content has been provided by the applicant.
        *Resume ={file_text}
        * Job Description = {job_desc}
        <Format>  The report should contain the following sections:
        * Give a brief description of the applicant in 3 to 5 lines
        * Describe in percentage what are the chances of this resume of getting selected for the job.
        * Need not to be the exact percentage , you can give interval of percentage.
        * Give the expected ATS score along with matching and non-matching keywords.
        * Perform SWOT analysis and explain each parameter is strength, weakness,opportunity and threat .
        * Give what all sections in the current resume that are required to be changed in order to improve the ATS score and selection percentage.
        * Show both current version and improved version of the section in resume.
        * Create two sample resume which can maximize the ATS score and selection percentage.

        <Instructions>
        * Use bullet points for explaination whenever possible.
        * Create tables for descriptio where ever required.
        * Strictly do not add any new skill in sample resume.
        * The format of sample resume should be in such a way that they can be copied and pasted directly in word. 
        '''

        # Now we create a submit button to run the application


        response = model.invoke(prompt)
        st.write(response.content)

