import streamlit as st

from groq import Groq
from ddgs import DDGS



# -----------------------------------
# Groq API
# -----------------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]


client = Groq(
    api_key=groq_api_key
)



# -----------------------------------
# DuckDuckGo Search
# -----------------------------------

def web_search(topic, max_results=5):

    results = []


    try:

        ddgs = DDGS()


        search_results = ddgs.text(
            topic,
            max_results=max_results
        )


        for item in search_results:

            results.append(
                {
                    "title": item.get("title"),
                    "link": item.get("href"),
                    "snippet": item.get("body")
                }
            )


    except Exception as e:

        results.append(
            {
                "title": "Search Error",
                "link": "",
                "snippet": str(e)
            }
        )


    return results



# -----------------------------------
# Generate Report
# -----------------------------------

def generate_report(topic):


    sources = web_search(topic)


    research_data = ""


    for index, source in enumerate(sources, start=1):

        research_data += f"""

Source {index}

Title:
{source['title']}

URL:
{source['link']}

Information:
{source['snippet']}

--------------------

"""



    prompt = f"""

You are an expert AI research analyst.

Prepare a professional research report about:

{topic}


Use this web research:


{research_data}



Report Structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Benefits and Opportunities

6. Challenges

7. Future Outlook

8. Conclusion


Add a final section:

Sources Used

Include URLs from the research.

Write a detailed professional report.

"""



    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",
                "content": "You write professional research reports."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content
