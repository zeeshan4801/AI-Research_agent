import os
import streamlit as st

from crewai import Agent, Task, Crew

from langchain_groq import ChatGroq



# -----------------------------------
# Load API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY missing from Streamlit Secrets.")
    st.stop()



os.environ["GROQ_API_KEY"] = groq_api_key



# -----------------------------------
# Groq LLM
# -----------------------------------

llm = ChatGroq(

    model="llama-3.1-8b-instant",

    api_key=groq_api_key,

    temperature=0.2

)



# -----------------------------------
# Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Create detailed and professional research reports
on any given topic.
""",

    backstory="""
You are an expert AI research analyst.
You analyze topics and create structured reports.
""",

    llm=llm,

    verbose=True

)



# -----------------------------------
# Generate Report
# -----------------------------------

def generate_report(topic):


    task = Task(

        description=f"""

Create a detailed research report on:

{topic}


Follow this structure:

1. Introduction

2. Background

3. Important Facts

4. Current Information

5. Advantages

6. Challenges

7. Future Outlook

8. Conclusion


Write a professional report.

""",

        expected_output="""

A complete professional research report.

""",

        agent=researcher

    )



    crew = Crew(

        agents=[researcher],

        tasks=[task],

        verbose=True

    )


    result = crew.kickoff()


    return result
