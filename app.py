import streamlit as st

from research_agent import generate_report

from datetime import datetime

import io
import re
import html

import markdown

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

from reportlab.lib import colors



# ---------------------------------
# Page Config
# ---------------------------------

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎",
    layout="wide"
)



# ---------------------------------
# UI
# ---------------------------------

st.markdown(
"""
<style>

.main-title{
font-size:45px;
font-weight:700;
color:#1f3c88;
}

.subtitle{
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
"<div class='subtitle'>Professional AI-powered research reports.</div>",
unsafe_allow_html=True
)


st.divider()



# ---------------------------------
# Sidebar
# ---------------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    report_style = st.selectbox(
        "Report Style",
        [
            "Quick Report",
            "Detailed Report",
            "Academic Report"
        ]
    )



# ---------------------------------
# Input
# ---------------------------------

topic = st.text_input(
    "Enter Research Topic",
    placeholder="Example: Artificial Intelligence in Healthcare"
)



if st.button(
    "🚀 Generate Report",
    use_container_width=True
):

    if topic.strip():

        with st.spinner(
            "Generating report..."
        ):

            report = generate_report(topic)


        st.session_state.report = str(report)

        st.session_state.topic = topic


        st.success(
            "Report Generated Successfully"
        )


    else:

        st.warning(
            "Please enter topic"
        )



# ---------------------------------
# Markdown Cleaner
# ---------------------------------

def clean_markdown(text):


    text = text.replace(
        "---",
        ""
    )


    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text
    )


    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
        text
    )


    text = text.replace(
        "`",
        ""
    )


    return text.strip()



# ---------------------------------
# PDF Footer
# ---------------------------------

def footer(canvas, doc):

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



# ---------------------------------
# PDF Generator
# ---------------------------------

def create_pdf(report, topic):


    buffer = io.BytesIO()


    pdf = SimpleDocTemplate(

        buffer,

        pagesize=letter,

        rightMargin=60,

        leftMargin=60,

        topMargin=60,

        bottomMargin=60

    )



    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "title",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=22,

        spaceAfter=20

    )



    heading_style = ParagraphStyle(

        "heading",

        parent=styles["Heading2"],

        fontSize=15,

        spaceBefore=15,

        spaceAfter=10

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
        Paragraph(
            "Powered by Groq AI",
            body_style
        )
    )


    story.append(
        Spacer(1,40)
    )


    story.append(
        Paragraph(
            f"Research Topic:<br/>{html.escape(topic)}",
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



    # Clean Markdown

    report = clean_markdown(report)



    lines = report.split("\n")



    for line in lines:


        line=line.strip()


        if not line:

            continue



        safe_line = html.escape(line)



        # headings


        if re.match(
            r"^(#|\d+\.)",
            line
        ):


            story.append(

                Paragraph(

                    safe_line.replace("#",""),

                    heading_style

                )

            )


        # bullets


        elif line.startswith("-"):


            story.append(

                Paragraph(

                    "• " + safe_line[1:].strip(),

                    body_style

                )

            )


        else:


            story.append(

                Paragraph(

                    safe_line,

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



# ---------------------------------
# Display
# ---------------------------------

if "report" in st.session_state:


    st.divider()


    st.subheader(
        "📄 Research Report"
    )


    st.markdown(
        st.session_state.report
    )


    st.divider()



    pdf_file=create_pdf(

        st.session_state.report,

        st.session_state.topic

    )



    st.download_button(

        "📄 Download Professional PDF",

        pdf_file,

        file_name="AI_Research_Report.pdf",

        mime="application/pdf"

    )
