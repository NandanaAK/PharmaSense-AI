import re
import streamlit as st
from agents.orchestrator import orchestrate


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PharmaSense AI",
    page_icon="🧬",
    layout="wide"
)


# =========================================================
# REPORT DISPLAY HELPER
# =========================================================

def display_report(report):
    """
    Display the text report using readable headings,
    sections, bullet points, and highlighted findings.
    """

    lines = report.splitlines()
    current_section = None
    section_content = []

    def render_section(section, content):
        if not section:
            return

        text_content = "\n".join(content).strip()

        if "ADVERSE EVENT" in section.upper():
            with st.container(border=True):
                st.subheader(f"⚠️ {section.title()}")
                if text_content:
                    st.markdown(text_content)

        elif "LITERATURE" in section.upper():
            with st.container(border=True):
                st.subheader(f"📚 {section.title()}")
                if text_content:
                    st.markdown(text_content)

        elif "TRIAL DATA" in section.upper():
            with st.container(border=True):
                st.subheader(f"🧪 {section.title()}")
                if text_content:
                    st.markdown(text_content)

        elif "COMPOUND SIMILARITY" in section.upper():
            with st.container(border=True):
                st.subheader(f"🧬 {section.title()}")
                if text_content:
                    st.markdown(text_content)

        elif "SUMMARY" in section.upper():
            with st.container(border=True):
                st.subheader(f"📋 {section.title()}")
                if text_content:
                    st.markdown(text_content)

        else:
            with st.container(border=True):
                st.subheader(section.title())
                if text_content:
                    st.markdown(text_content)

    for line in lines:
        clean_line = line.strip()

        # Detect numbered report sections, e.g. 1. TRIAL DATA
        match = re.match(r"^\d+\.\s+(.+)$", clean_line)

        if match:
            render_section(current_section, section_content)
            current_section = match.group(1).strip()
            section_content = []
            continue

        # Skip decorative divider lines
        if clean_line and set(clean_line) == {"="}:
            continue

        if clean_line and set(clean_line) == {"-"}:
            continue

        # Skip the report title because it is shown separately
        if clean_line.upper() == "PHARMASENSE AI - FINAL REPORT":
            continue

        section_content.append(line)

    render_section(current_section, section_content)


# =========================================================
# HEADER
# =========================================================

st.title("🧬 PharmaSense AI")

st.subheader(
    "Agentic AI Assistant for Pharmaceutical Research & Clinical Analysis"
)

st.write(
    "An AI-powered assistant for exploring compounds, "
    "clinical trials, research literature, adverse events, "
    "and compound similarity."
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("🧬 PharmaSense AI")

    st.subheader("Available Capabilities")

    st.markdown(
        """
        - 🔬 Compound Analysis
        - 🧪 Clinical Trial Analysis
        - 📚 Literature Research
        - ⚠️ Adverse Event Analysis
        - 🧬 Compound Similarity
        - 📊 Integrated Reports
        """
    )

    st.divider()

    st.subheader("Example Questions")

    examples = [
        "Give me a report for CMP-0055.",
        "What adverse events occurred in TRL-0037?",
        "Find compounds similar to CMP-0055.",
        "Which clinical trials have low enrollment?"
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state["question"] = example


# =========================================================
# QUESTION INPUT
# =========================================================

st.header("💬 Ask PharmaSense AI")

question = st.text_area(
    "Enter your question:",
    key="question",
    placeholder="Example: Give me a report for CMP-0055.",
    height=120
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🚀 Analyze",
    type="primary",
    use_container_width=True
):

    if not question.strip():
        st.warning("Please enter a question before clicking Analyze.")

    else:
        with st.spinner(
            "PharmaSense AI is analyzing your question..."
        ):
            try:
                result = orchestrate(question.strip())

                if isinstance(result, str):
                    st.success("Analysis completed.")
                    st.divider()
                    st.header("📋 PharmaSense AI Report")
                    display_report(result)

                    st.download_button(
                        label="📥 Download Report",
                        data=result,
                        file_name="PharmaSense_AI_Report.txt",
                        mime="text/plain"
                    )

                elif isinstance(result, dict):
                    if result.get("status") == "failed":
                        st.error("The report could not be generated.")
                        st.write(result.get("error", "Unknown error"))
                    else:
                        st.success("Analysis completed.")
                        st.header("📋 PharmaSense AI Results")
                        st.json(result)

                else:
                    st.success("Analysis completed.")
                    st.write(result)

            except Exception as error:
                st.error(
                    "An unexpected error occurred while "
                    "processing the question."
                )
                st.exception(error)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "PharmaSense AI | Agentic AI Pharmaceutical Research Assistant"
)
