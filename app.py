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

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

import io
import html
import re
import os



# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(

    page_title="AI Research Agent",

    page_icon="🔎",

    layout="wide"

)



# -----------------------------------
# Register Unicode Font
# -----------------------------------

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


pdfmetrics.registerFont(

    TTFont(

        "DejaVu",

        font_path

    )

)



# -----------------------------------
# UI CSS
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

"<div class='subtitle'>Professional AI powered research reports with live web research.</div>",

unsafe_allow_html=True

)


st.divider()



# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:


    st.header("⚙️ Research Settings")


    report_style = st.selectbox(

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

            "AI agent is researching..."

        ):


            report = generate_report(topic)



        st.session_state.report = str(report)

        st.session_state.topic = topic


        st.success(

            "Report Generated Successfully"

        )


    else:


        st.warning(

            "Please enter a topic."

        )



# -----------------------------------
# Clean PDF Text
# -----------------------------------

def clean_text(text):


    replacements = {

        "\u2013": "-",

        "\u2014": "-",

        "\u2018": "'",

        "\u2019": "'",

        "\u201c": '"',

        "\u201d": '"',

        "\u00a0": " ",

        "\u2022": "-",

        "\u200b": ""

    }


    for old, new in replacements.items():

        text = text.replace(

            old,

            new

        )


    text = re.sub(

        r"[^\x00-\x7F]+",

        "",

        text

    )


    text = html.escape(text)


    return text



# -----------------------------------
# Page Number Footer
# -----------------------------------

def add_footer(canvas, doc):


    canvas.saveState()


    canvas.setFont(

        "DejaVu",

        9

    )


    canvas.drawCentredString(

        letter[0] / 2,

        25,

        f"AI Research Agent | Page {doc.page}"

    )


    canvas.restoreState()



# -----------------------------------
# PDF Generator
# -----------------------------------

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

        "TitleCustom",

        parent=styles["Title"],

        fontName="DejaVu",

        alignment=TA_CENTER,

        fontSize=24

    )



    subtitle_style = ParagraphStyle(

        "SubtitleCustom",

        parent=styles["Normal"],

        fontName="DejaVu",

        alignment=TA_CENTER,

        fontSize=12

    )



    heading_style = ParagraphStyle(

        "HeadingCustom",

        parent=styles["Heading2"],

        fontName="DejaVu",

        fontSize=15,

        spaceBefore=15

    )



    body_style = ParagraphStyle(

        "BodyCustom",

        parent=styles["BodyText"],

        fontName="DejaVu",

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

        Spacer(

            1,

            20

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

            f"Research Topic:<br/>{html.escape(topic)}",

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

            r"^(\d+\.|#)",

            line

        ):


            story.append(

                Paragraph(

                    line.replace("#",""),

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

        onFirstPage=add_footer,

        onLaterPages=add_footer

    )


    buffer.seek(0)


    return buffer



# -----------------------------------
# Show Report
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

        label="📄 Download Professional PDF",

        data=pdf_file,

        file_name="AI_Research_Report.pdf",

        mime="application/pdf"

    )
