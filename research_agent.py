import os
import streamlit as st

from crewai import Agent, Task, Crew, LLM

from tools import DuckDuckGoSearchTool


# -----------------------------
# Groq API Key
# -----------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]


# LiteLLM Groq configuration
os.environ["GROQ_API_KEY"] = groq_api_key


# -----------------------------
# LLM
# -----------------------------

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=groq_api_key,
    temperature=0.2
)


# -----------------------------
# Search Tool
# -----------------------------

search_tool = DuckDuckGoSearchTool()


# -----------------------------
# Agent
# -----------------------------

researcher = Agent(
    role="AI Research Analyst",

    goal="""
Research topics using web search and create
accurate professional research reports.
""",

    backstory="""
You are an expert research analyst.
You collect information from online sources,
analyze it, and prepare structured reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True
)


# -----------------------------
# Generate Report
# -----------------------------

def generate_report(topic):

    task = Task(
        description=f"""
Research this topic:

{topic}

Create a detailed report containing:

1. Introduction
2. Background
3. Current Information
4. Key Facts
5. Advantages
6. Challenges
7. Future Outlook
8. Conclusion

Use web search information.
""",

        expected_output="""
A professional research report with headings
and detailed explanations.
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
