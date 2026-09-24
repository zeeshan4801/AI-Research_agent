import streamlit as st
from groq import Groq


# -----------------------------------
# Load Groq API Key
# -----------------------------------

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]

except Exception:
    st.error("GROQ_API_KEY is missing from Streamlit Secrets.")
    st.stop()



# -----------------------------------
# Groq Client
# -----------------------------------

client = Groq(
    api_key=groq_api_key
)



# -----------------------------------
# Generate Research Report
# -----------------------------------

def generate_report(topic):


    prompt = f"""

You are an expert AI research analyst.

Create a detailed professional research report about:

{topic}


Use this structure:

1. Introduction

2. Background

3. Current Information

4. Key Facts

5. Advantages

6. Challenges

7. Future Outlook

8. Conclusion


Write a complete, well-organized report.

"""


    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role": "system",
                "content": "You are a professional research analyst."
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        temperature=0.2

    )


    return response.choices[0].message.content
