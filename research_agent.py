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


os.environ["GROQ_API_KEY"] = groq_api_key


# -----------------------------------
# Groq LLM
# -----------------------------------

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=groq_api_key,
    temperature=0.2
)


# -----------------------------------
# Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Create accurate and professional research reports
on any given topic.
""",

    backstory="""
You are an expert research analyst.
You analyze topics and write structured reports.
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
Prepare a detailed research report about:

{topic}


Use this structure:

1. Introduction

2. Background

3. Key Facts

4. Current Information

5. Advantages

6. Challenges

7. Future Outlook

8. Conclusion


Write in a professional research style.
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
