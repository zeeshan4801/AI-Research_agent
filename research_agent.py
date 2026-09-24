import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS



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

    with DDGS() as ddgs:

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

    return results



# -----------------------------------
# Generate Research Report
# -----------------------------------

def generate_report(topic):


    sources = web_search(topic)



    research_data = ""

    for i, source in enumerate(sources, start=1):

        research_data += f"""

Source {i}

Title:
{source['title']}

Link:
{source['link']}

Information:
{source['snippet']}

--------------------

"""



    prompt = f"""

You are an expert AI research analyst.

Create a professional research report about:

{topic}


Use the following web research information:


{research_data}



Report structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Advantages

6. Challenges

7. Future Outlook

8. Conclusion


At the end add:

Sources Used:

List all URLs used in the research.


Write a detailed professional report.

"""



    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role":"system",
                "content":
                "You create professional research reports."
            },

            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content
