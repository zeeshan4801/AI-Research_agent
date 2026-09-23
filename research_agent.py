import os

from dotenv import load_dotenv

from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

from tools import DuckDuckGoSearchTool


load_dotenv()


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0.2
)


search_tool = DuckDuckGoSearchTool()



researcher = Agent(
    role="AI Research Analyst",

    goal="""
Research any given topic from reliable sources
and create a detailed professional report.
""",

    backstory="""
You are an expert research analyst.
You collect information,
verify important points,
and write clear reports.
""",

    tools=[search_tool],

    llm=llm,

    verbose=True
)



def generate_report(topic):

    task = Task(

        description=f"""
Research this topic:

{topic}

Create a detailed report including:

1. Introduction
2. Background
3. Current information
4. Important facts
5. Advantages and disadvantages
6. Future outlook
7. Conclusion

Use information collected from web search.
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
