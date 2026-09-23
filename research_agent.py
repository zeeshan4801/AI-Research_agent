import streamlit as st

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

from tools import DuckDuckGoSearchTool



# -----------------------------
# Groq API Key from Streamlit Secrets
# -----------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]



# -----------------------------
# Groq LLM
# -----------------------------

llm = ChatGroq(

    api_key=groq_api_key,

    model="openai/gpt-oss-120b",

    temperature=0.2

)



# -----------------------------
# Search Tool
# -----------------------------

search_tool = DuckDuckGoSearchTool()



# -----------------------------
# Single Research Agent
# -----------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Research any given topic using web search
and create a detailed, accurate professional report.
""",

    backstory="""
You are an expert AI research analyst.
You collect information from online sources,
analyze important points, and write structured reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True

)



# -----------------------------
# Generate Research Report
# -----------------------------

def generate_report(topic):


    research_task = Task(

        description=f"""

Research the following topic:

{topic}


Create a complete research report.

Follow this structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Benefits

6. Challenges

7. Future Trends

8. Conclusion


Use information collected from web search.
Mention important sources when possible.

""",

        expected_output="""

A detailed professional research report
with clear headings and paragraphs.

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
