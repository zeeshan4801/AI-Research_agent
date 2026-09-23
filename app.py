import streamlit as st

from research_agent import generate_report



# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(

    page_title="AI Research Agent",

    page_icon="🔎",

    layout="wide"

)



# -----------------------------
# UI
# -----------------------------

st.title("🔎 AI Research Agent")

st.write(
    "Enter a research topic and generate an AI-powered research report."
)



topic = st.text_input(

    "Enter Research Topic"

)



if st.button("Generate Report"):


    if topic.strip():


        with st.spinner(

            "AI agent is researching and writing report..."

        ):


            report = generate_report(topic)



        st.success(

            "Report Generated Successfully"

        )


        st.markdown(

            str(report)

        )


    else:


        st.warning(

            "Please enter a research topic."

        )
