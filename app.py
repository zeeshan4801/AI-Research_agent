import streamlit as st

from research_agent import generate_report



st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)



st.title("🔎 AI Research Agent")

st.write(
    "Enter any research topic and generate a complete AI research report."
)



topic = st.text_input(
    "Enter Research Topic"
)



if st.button("Generate Report"):


    if topic:

        with st.spinner(
            "Researching and writing report..."
        ):

            report = generate_report(topic)


        st.success(
            "Report Generated"
        )


        st.markdown(report)


    else:

        st.warning(
            "Please enter a topic"
        )
