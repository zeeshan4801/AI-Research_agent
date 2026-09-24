import streamlit as st

from crewai import Agent, Task, Crew, LLM

from tools import DuckDuckGoSearchTool



# -----------------------------------
# Load Groq API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
    st.stop()



# -----------------------------------
# Groq LLM Configuration
# -----------------------------------

llm = LLM(

    model="groq/gpt-oss-120b",

    api_key=groq_api_key,

    temperature=0.2

)



# -----------------------------------
# DuckDuckGo Search Tool
# -----------------------------------

search_tool = DuckDuckGoSearchTool()



# -----------------------------------
# Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Research any given topic using web search
and create a detailed, accurate, professional report.
""",

    backstory="""
You are an expert AI research analyst.
You search the internet, collect useful information,
analyze facts, and prepare structured research reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True

)



# -----------------------------------
# Generate Report
# -----------------------------------

def generate_report(topic):


    research_task = Task(

        description=f"""

Research the following topic:

{topic}


Create a detailed research report with these sections:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Benefits and Opportunities

6. Challenges and Limitations

7. Future Outlook

8. Conclusion


Use web search information.
Write the report in a professional format.

""",

        expected_output="""

A complete professional research report
with headings, explanations, and important facts.

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
