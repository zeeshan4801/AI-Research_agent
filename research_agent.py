import streamlit as st

from crewai import Agent, Task, Crew

from groq import Groq



# -----------------------------------
# Load Groq API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY is missing in Streamlit Secrets.")
    st.stop()



# -----------------------------------
# Groq Client
# -----------------------------------

client = Groq(
    api_key=groq_api_key
)



# -----------------------------------
# Custom LLM Function
# -----------------------------------

class GroqLLM:

    def call(self, prompt):

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": "You are an expert research analyst."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2

        )


        return response.choices[0].message.content



llm = GroqLLM()



# -----------------------------------
# Research Agent
# -----------------------------------

researcher = Agent(

    role="AI Research Analyst",

    goal="""
Create detailed professional research reports
from given topics.
""",

    backstory="""
You are an expert research analyst.
You write accurate, structured reports.
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


Include:

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

A complete research report.

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
