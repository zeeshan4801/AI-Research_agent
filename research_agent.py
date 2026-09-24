import streamlit as st

from crewai import Agent, Task, Crew, LLM

from tools import DuckDuckGoSearchTool



# Get Groq API Key

groq_api_key = st.secrets["GROQ_API_KEY"]



# CrewAI native LLM

llm = LLM(

    model="groq/openai/gpt-oss-120b",

    api_key=groq_api_key,

    temperature=0.2

)



# Search Tool

search_tool = DuckDuckGoSearchTool()



# Agent

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Research topics using web search and create
accurate professional research reports.
""",

    backstory="""
You are an expert AI research analyst.
You collect information, analyze sources,
and write structured reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True

)



def generate_report(topic):


    task = Task(

        description=f"""

Research the following topic:

{topic}


Create a detailed report with:

1. Introduction
2. Background
3. Current Information
4. Key Facts
5. Advantages
6. Challenges
7. Future Trends
8. Conclusion


Use web search information.

""",

        expected_output="""

A professional research report with clear sections.

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
