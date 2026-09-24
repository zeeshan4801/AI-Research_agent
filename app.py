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
import html



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


.stButton button {

height:45px;
border-radius:10px;
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

"<div class='subtitle'>AI-powered research with live web information.</div>",

unsafe_allow_html=True

)


st.divider()



# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:


    st.header("⚙️ Research Settings")


    report_type = st.selectbox(

        "Report Type",

        [

            "Quick Report",

            "Detailed Report",

            "Academic Report"

        ]

    )


    source_count = st.slider(

        "Sources",

        3,

        10,

        5

    )


    st.info(

        "Powered by Groq AI + DuckDuckGo Search"

    )



# -----------------------------------
# Topic Input
# -----------------------------------

topic = st.text_input(

    "Enter Research Topic",

    placeholder="Example: Future of Artificial Intelligence"

)



# -----------------------------------
# Generate Report
# -----------------------------------

if st.button(

    "🚀 Generate Research Report",

    use_container_width=True

):


    if topic.strip():


        with st.spinner(

            "Researching and generating report..."

        ):


            report = generate_report(topic)



        st.session_state.report = str(report)

        st.session_state.topic = topic



        st.success(

            "Report Generated Successfully"

        )


    else:


        st.warning(

            "Please enter a research topic."

        )



# -----------------------------------
# PDF Generator
# -----------------------------------

def create_pdf(text):


    buffer = io.BytesIO()


    pdf = SimpleDocTemplate(

        buffer

    )


    styles = getSampleStyleSheet()


    story = []


    clean_text = html.escape(text)



    for line in clean_text.split("\n"):


        if line.strip():


            story.append(

                Paragraph(

                    line,

                    styles["BodyText"]

                )

            )


            story.append(

                Spacer(

                    1,

                    12

                )

            )



    pdf.build(story)


    buffer.seek(0)


    return buffer



# -----------------------------------
# Display Report
# -----------------------------------

if "report" in st.session_state:


    st.divider()


    st.subheader(

        "📄 Research Report"

    )


    st.caption(

        f"Topic: {st.session_state.topic}"

    )


    st.caption(

        f"Generated: {datetime.now().strftime('%d %B %Y')}"

    )


    st.divider()



    st.markdown(

        st.session_state.report

    )



    st.divider()



    # Markdown Download


    markdown_data = (

        "# AI Research Report\n\n"

        + st.session_state.report

    )


    st.download_button(

        label="⬇️ Download Markdown",

        data=markdown_data,

        file_name="AI_Research_Report.md",

        mime="text/markdown"

    )



    # PDF Download


    pdf = create_pdf(

        st.session_state.report

    )


    st.download_button(

        label="📄 Download PDF",

        data=pdf,

        file_name="AI_Research_Report.pdf",

        mime="application/pdf"

    )
