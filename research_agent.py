import streamlit as st

from crewai import Agent, Task, Crew, LLM

from tools import DuckDuckGoSearchTool



# -----------------------------------
# Get Groq API Key from Streamlit
# -----------------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]



# -----------------------------------
# CrewAI LLM using Groq
# -----------------------------------

llm = LLM(

    model="groq/openai/gpt-oss-120b",

    api_key=groq_api_key,

    temperature=0.2

)



# -----------------------------------
# Web Search Tool
# -----------------------------------

search_tool = DuckDuckGoSearchTool()



# -----------------------------------
# Single Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Research any given topic using web search
and create an accurate professional report.
""",

    backstory="""
You are an expert AI research analyst.
You search for relevant information,
analyze facts, and write structured reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True

)



# -----------------------------------
# Generate Report Function
# -----------------------------------

def generate_report(topic):


    research_task = Task(

        description=f"""
Research the following topic:

{topic}


Create a detailed research report.

Follow this structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Benefits and Opportunities

6. Challenges and Limitations

7. Future Outlook

8. Conclusion


Use information collected from web search.
Include important sources where available.

""",

        expected_output="""
A complete professional research report
with clear headings and detailed explanations.
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
