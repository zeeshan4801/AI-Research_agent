import os
import streamlit as st

from crewai import Agent, Task, Crew, LLM



# -----------------------------------
# Load Groq API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
    st.stop()



# -----------------------------------
# Environment Setup
# -----------------------------------

os.environ["GROQ_API_KEY"] = groq_api_key



# -----------------------------------
# Groq LLM
# -----------------------------------

llm = LLM(

    model="groq/llama-3.1-8b-instant",

    api_key=groq_api_key,

    temperature=0

)



# -----------------------------------
# Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Create accurate and structured research reports
on different topics.
""",

    backstory="""
You are an AI research analyst.
You analyze topics and write professional reports.
""",

    llm=llm,

    verbose=True,

    max_iter=3

)



# -----------------------------------
# Generate Report
# -----------------------------------

def generate_report(topic):


    research_task = Task(

        description=f"""

Create a detailed research report on:

{topic}


Use this structure:

1. Introduction

2. Background

3. Important Facts

4. Current Situation

5. Advantages

6. Challenges

7. Future Outlook

8. Conclusion


Write in a professional style.

""",

        expected_output="""

A complete research report with headings
and detailed explanations.

""",

        agent=researcher

    )


    crew = Crew(

        agents=[researcher],

        tasks=[research_task],

        verbose=True

    )


    result = crew.kickoff()


    return result
