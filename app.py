import streamlit as st
from research_agent import generate_report

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER

import io
import re
import html



# -----------------------------
# Page Setup
# -----------------------------

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)



# -----------------------------
# UI Design
# -----------------------------

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

</style>
""",
unsafe_allow_html=True
)


st.markdown(
"<div class='main-title'>🔎 AI Research Agent</div>",
unsafe_allow_html=True
)


st.markdown(
"<div class='subtitle'>Generate professional AI research reports.</div>",
unsafe_allow_html=True
)


st.divider()



# -----------------------------
# Input
# -----------------------------

topic = st.text_input(
    "Enter Research Topic"
)



if st.button(
    "🚀 Generate Report",
    use_container_width=True
):

    if topic.strip():

        with st.spinner(
            "Researching..."
        ):

            report = generate_report(topic)


        st.session_state.report = str(report)

        st.session_state.topic = topic


        st.success(
            "Report Generated Successfully"
        )

    else:

        st.warning(
            "Enter a topic first"
        )



# -----------------------------
# Text Cleaning
# -----------------------------

def clean_text(text):


    # remove html

    text = re.sub(
        r"<[^>]+>",
        "",
        text
    )


    # remove markdown

    text = text.replace(
        "**",
        ""
    )


    text = text.replace(
        "__",
        ""
    )


    text = text.replace(
        "---",
        ""
    )


    # remove markdown table lines

    text = re.sub(
        r"\|[-:\s|]+\|",
        "",
        text
    )


    # replace table separators

    text = text.replace(
        "|",
        " "
    )


    # remove invisible characters

    text = re.sub(
        r"[\u0000-\u001F\u007F-\u009F\u200B-\u200F\u202A-\u202E]",
        "",
        text
    )


    # replace strange symbols

    replacements = {

        "■":"",
        "•":"-",
        "–":"-",
        "—":"-",
        "“":'"',
        "”":'"',
        "’":"'"

    }


    for old,new in replacements.items():

        text = text.replace(
            old,
            new
        )


    return html.escape(
        text.strip()
    )



# -----------------------------
# PDF Footer
# -----------------------------

def footer(canvas,doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9
    )


    canvas.drawCentredString(

        letter[0]/2,

        25,

        f"AI Research Agent | Page {doc.page}"

    )


    canvas.restoreState()



# -----------------------------
# Create PDF
# -----------------------------

def create_pdf(report,topic):


    buffer = io.BytesIO()


    pdf = SimpleDocTemplate(

        buffer,

        pagesize=letter,

        leftMargin=60,

        rightMargin=60,

        topMargin=60,

        bottomMargin=60

    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "title",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=22

    )



    heading_style = ParagraphStyle(

        "heading",

        parent=styles["Heading2"],

        fontSize=15,

        spaceBefore=15

    )



    body_style = ParagraphStyle(

        "body",

        parent=styles["BodyText"],

        fontSize=11,

        leading=16

    )



    story=[]



    # Cover Page


    story.append(
        Spacer(1,120)
    )


    story.append(

        Paragraph(

            "AI RESEARCH AGENT",

            title_style

        )

    )


    story.append(
        Spacer(1,20)
    )


    story.append(

        Paragraph(

            "Powered by Groq AI",

            body_style

        )

    )


    story.append(
        Spacer(1,30)
    )


    story.append(

        Paragraph(

            f"Research Topic: {html.escape(topic)}",

            body_style

        )

    )


    story.append(

        Paragraph(

            datetime.now().strftime("%d %B %Y"),

            body_style

        )

    )


    story.append(
        PageBreak()
    )



    # Report Body


    for line in report.split("\n"):


        line=line.strip()


        if not line:

            continue



        cleaned = clean_text(line)



        if re.match(

            r"^(#|\d+\.)",

            line

        ):


            story.append(

                Paragraph(

                    cleaned.replace("#",""),

                    heading_style

                )

            )


        elif line.startswith("-"):


            story.append(

                Paragraph(

                    "• " + cleaned[1:],

                    body_style

                )

            )


        else:


            story.append(

                Paragraph(

                    cleaned,

                    body_style

                )

            )


        story.append(
            Spacer(1,8)
        )



    pdf.build(

        story,

        onFirstPage=footer,

        onLaterPages=footer

    )


    buffer.seek(0)


    return buffer



# -----------------------------
# Display
# -----------------------------

if "report" in st.session_state:


    st.divider()


    st.subheader(
        "📄 Research Report"
    )


    st.markdown(
        st.session_state.report
    )


    pdf_file = create_pdf(

        st.session_state.report,

        st.session_state.topic

    )


    st.download_button(

        "📄 Download Professional PDF",

        pdf_file,

        file_name="AI_Research_Report.pdf",

        mime="application/pdf"

    )
