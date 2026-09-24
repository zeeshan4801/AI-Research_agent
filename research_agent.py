import os
import streamlit as st

from crewai import Agent, Task, Crew, LLM



# -----------------------------------
# Load Groq API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY is missing in Streamlit Secrets.")
    st.stop()



# -----------------------------------
# Environment
# -----------------------------------

os.environ["GROQ_API_KEY"] = groq_api_key



# -----------------------------------
# Groq LLM
# -----------------------------------

llm = LLM(

    model="groq/openai/gpt-oss-120b",

    api_key=groq_api_key,

    temperature=0.2,

    drop_params=True

)



# -----------------------------------
# Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Create detailed, accurate, and professional
research reports on any given topic.
""",

    backstory="""
You are an expert AI research analyst.
You analyze topics, organize information,
and write high-quality research reports.
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

Prepare a detailed research report on:

{topic}


Use this structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Advantages and Opportunities

6. Challenges and Limitations

7. Future Outlook

8. Conclusion


Write in a professional research style.

""",

        expected_output="""

A complete professional research report
with clear headings and explanations.

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
