import pandas as pd
import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from io import StringIO

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# PDF Function
def create_pdf(table, summary):
    doc = SimpleDocTemplate("trip_plan.pdf")
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Smart Trip Planner Report", styles["Title"]))
    story.append(Paragraph("<br/>Travel Plan Table:<br/>", styles["Heading2"]))

    table_text = table.to_string(index=False)
    story.append(Paragraph(f"<pre>{table_text}</pre>", styles["Normal"]))

    story.append(Paragraph("<br/>Summary:<br/>", styles["Heading2"]))
    story.append(Paragraph(summary.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)

# UI
st.title("🌍 AI Smart Trip Planner")

place = st.text_input("📍 Starting Place")
days = st.number_input("📅 Number of Days", 1, 10, 3)
budget = st.number_input("💰 Total Budget (₹)", 1000, value=5000)
people = st.number_input("👨‍👩‍👧 Number of People", 1, 10, 2)

travel_type = st.selectbox("🎯 Travel Type", ["Adventure", "Relax", "Family"])
budget_style = st.selectbox("💎 Budget Style", ["Cheap", "Standard", "Luxury"])

generate = st.button("✨ Generate Plan")

# Main Logic
if generate:
    st.info("✨ Generating your smart trip plan...")

    prompt = f"""
    Create a {days}-day travel itinerary starting from {place}.

    Constraints:
    - Total budget: ₹{budget}
    - Number of people: {people}
    - Travel type: {travel_type}
    - Budget style: {budget_style}

    IMPORTANT RULES:

    1. First give ONLY CSV table:
    Day,Destination,Location,Rating,Cost,Distance

    Example:
    1,Cherai Beach,Kochi,4.2,500,20km

    2. After table, write exactly:
    ###SUMMARY###

    3. Then give summary like:
    Total cost: ...
    Total distance: ...
    Best destination: ...
    Travel tips: ...

    DO NOT mix summary inside table.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response.choices[0].message.content

        # Split response
        if "###SUMMARY###" in result:
            parts = result.split("###SUMMARY###")
            table_data = parts[0].strip()
            summary = parts[1].strip()
        else:
            # fallback: try splitting by 'Total cost' or similar keywords
            lines = result.split("\n")
            table_lines = []
            summary_lines = []

            summary_started = False

            for line in lines:
                if "total cost" in line.lower() or "summary" in line.lower():
                    summary_started = True

                if summary_started:
                    summary_lines.append(line)
                else:
                    table_lines.append(line)

            table_data = "\n".join(table_lines)
            summary = "\n".join(summary_lines) if summary_lines else "No summary available"

        # Clean table data
        lines = table_data.split("\n")
        clean_lines = []

        for line in lines:
            if ("," in line and "Day" in line) or line.strip().startswith(tuple(str(i) for i in range(1, 10))):
                clean_lines.append(line)

        clean_data = "\n".join(clean_lines)

        # Validate data
        if clean_data.strip() == "":
            st.error("❌ AI did not return proper table data. Try again.")
            st.info("💡 Tip: Try different inputs (budget/days).")
        else:
            df = pd.read_csv(StringIO(clean_data))

            # Display
            st.subheader("🗺️ Travel Plan Table")
            st.dataframe(df, use_container_width=True)

            st.subheader("📊 Summary")
            st.write(summary)

            # PDF
            create_pdf(df, summary)

            with open("trip_plan.pdf", "rb") as f:
                st.download_button(
                    label="📄 Download Trip Plan",
                    data=f,
                    file_name="TripPlan.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error("⚠️ Something went wrong. Please try again.")
        st.text(str(e))

# Footer
st.markdown("---")
st.markdown("### 🌟 Plan Smart. Travel Better.")