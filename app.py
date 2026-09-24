import streamlit as st

from research_agent import generate_report

from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.pagesizes import letter

from reportlab.lib.enums import TA_CENTER

import io
import html
import re



# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="AI Research Agent",

    page_icon="🔎",

    layout="wide"

)



# -----------------------------------
# UI Styling
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
color:#666;

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

"<div class='subtitle'>Professional AI-powered research reports with live web research.</div>",

unsafe_allow_html=True

)



st.divider()



# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.header("⚙️ Settings")


    report_type = st.selectbox(

        "Report Style",

        [

            "Quick Report",

            "Detailed Report",

            "Academic Report"

        ]

    )



# -----------------------------------
# Input
# -----------------------------------

topic = st.text_input(

    "Enter Research Topic",

    placeholder="Example: Future of Artificial Intelligence"

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

            "Report Generated"

        )


    else:

        st.warning(

            "Enter a topic first."

        )



# -----------------------------------
# PDF Generator
# -----------------------------------

def add_page_number(canvas, doc):

    canvas.saveState()


    canvas.setFont(

        "Helvetica",

        9

    )


    canvas.drawCentredString(

        letter[0] / 2,

        25,

        f"AI Research Agent | Page {doc.page}"

    )


    canvas.restoreState()



def clean_text(text):

    text = html.escape(text)


    text = text.replace(

        "##",

        ""

    )


    text = text.replace(

        "**",

        ""

    )


    return text



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



    subtitle_style = ParagraphStyle(

        "subtitle",

        parent=styles["Normal"],

        alignment=TA_CENTER,

        fontSize=12

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



    story = []



    # Cover Page


    story.append(

        Spacer(

            1,

            120

        )

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

            subtitle_style

        )

    )


    story.append(

        Spacer(

            1,

            40

        )

    )


    story.append(

        Paragraph(

            f"Research Topic:<br/>{topic}",

            subtitle_style

        )

    )


    story.append(

        Spacer(

            1,

            20

        )

    )


    story.append(

        Paragraph(

            datetime.now().strftime("%d %B %Y"),

            subtitle_style

        )

    )


    story.append(

        PageBreak()

    )



    # Report Content


    for line in report.split("\n"):


        line = line.strip()


        if not line:

            continue



        line = clean_text(line)



        if re.match(

            r"^\d+\.",

            line

        ):


            story.append(

                Paragraph(

                    line,

                    heading_style

                )

            )


        else:


            story.append(

                Paragraph(

                    line,

                    body_style

                )

            )



        story.append(

            Spacer(

                1,

                8

            )

        )



    pdf.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )


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

        st.session_state.topic

    )


    st.markdown(

        st.session_state.report

    )


    st.divider()



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
