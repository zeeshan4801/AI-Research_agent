import streamlit as st
from research_agent import generate_report

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

import io



# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="AI Research Agent",

    page_icon="🔎",

    layout="wide"

)



# -----------------------------------
# Custom CSS
# -----------------------------------

st.markdown(

"""
<style>

.main-title {

    font-size:45px;
    font-weight:700;
    color:#1f3c88;

}


.subtitle {

    font-size:18px;
    color:#555;

}


.report-box {

    padding:20px;
    border-radius:12px;
    background:#f8f9fa;

}


.stButton button {

    border-radius:10px;
    height:45px;
    font-weight:600;

}


</style>

""",

unsafe_allow_html=True

)



# -----------------------------------
# Header
# -----------------------------------

st.markdown(

"<div class='main-title'>🔎 AI Research Agent</div>",

unsafe_allow_html=True

)


st.markdown(

"<div class='subtitle'>Generate professional AI-powered research reports with live web research.</div>",

unsafe_allow_html=True

)



st.divider()



# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:


    st.header("⚙️ Research Settings")


    depth = st.selectbox(

        "Report Type",

        [

            "Quick Report",

            "Detailed Report",

            "Academic Report"

        ]

    )


    sources = st.slider(

        "Number of Sources",

        3,

        10,

        5

    )


    st.info(

        "AI Agent uses web search + Groq AI to create reports."

    )



# -----------------------------------
# Input
# -----------------------------------

topic = st.text_input(

    "Enter Research Topic",

    placeholder="Example: Future of Artificial Intelligence"

)



# -----------------------------------
# Generate
# -----------------------------------

if st.button(

    "🚀 Generate Research Report",

    use_container_width=True

):


    if topic.strip():


        with st.spinner(

            "AI agent is researching and writing..."

        ):


            report = generate_report(topic)



        st.session_state["report"] = report

        st.session_state["topic"] = topic



        st.success(

            "Report Generated Successfully"

        )


    else:


        st.warning(

            "Please enter a topic."

        )



# -----------------------------------
# Display Report
# -----------------------------------

if "report" in st.session_state:


    st.divider()


    st.subheader(

        "📄 Research Report"

    )


    st.caption(

        f"Topic: {st.session_state['topic']}"

    )


    st.caption(

        f"Generated: {datetime.now().strftime('%d %B %Y')}"

    )


    st.markdown("---")



    st.markdown(

        st.session_state["report"]

    )



    st.divider()



    # -------------------------------
    # Download Markdown
    # -------------------------------

    markdown_file = (

        "# AI Research Report\n\n"

        + st.session_state["report"]

    )


    st.download_button(

        label="⬇️ Download Markdown",

        data=markdown_file,

        file_name="research_report.md",

        mime="text/markdown"

    )



    # -------------------------------
    # Download PDF
    # -------------------------------

    def create_pdf(text):


        buffer = io.BytesIO()


        pdf = SimpleDocTemplate(

            buffer

        )


        styles = getSampleStyleSheet()


        story = []


        for line in text.split("\n"):


            story.append(

                Paragraph(

                    line,

                    styles["BodyText"]

                )

            )


            story.append(

                Spacer(1,12)

            )


        pdf.build(story)


        buffer.seek(0)


        return buffer



    pdf_file = create_pdf(

        st.session_state["report"]

    )


    st.download_button(

        label="📄 Download PDF",

        data=pdf_file,

        file_name="AI_Research_Report.pdf",

        mime="application/pdf"

    )
