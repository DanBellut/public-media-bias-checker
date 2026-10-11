import os
import json
import streamlit as st
from openai import OpenAI

# 1. Initialize OpenAI Client (Uses the OPENAI_API_KEY environment variable)
client = OpenAI()

# Define the system prompt guiding the LLM's classification logic
SYSTEM_PROMPT = """
You are a precise text analysis assistant. Your task is to analyze news articles or video transcripts to detect "left-liberal" or "woke" ideological framing, narratives, and interpretations (e.g., heavily moralizing language, identity politics framing, specific terminology/buzzwords).

You must return your response STRICTLY as a valid JSON object in the following format:
{
  "percentage": <integer between 0 and 100>,
  "analysis": [
    {"text": "exact text snippet from the input", "ideological": true/false},
    ...
  ]
}

Instructions:
1. Break down the entire input text into sequential snippets without skipping any words, so that concatenating them reconstructs the original text perfectly.
2. Set "ideological": true only for snippets containing the described framing or bias. Otherwise, set it to false.
"""

def analyze_text(user_text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Cost-effective and highly capable model
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            temperature=0.1,  # Low temperature ensures more consistent classifications
        )
        # Parse the JSON response
        return json.loads(response.choices.message.content)
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# 2. Streamlit Web UI Setup
st.set_page_config(page_title="Media Bias Analyzer", layout="wide")
st.title("🔍 Media Content Bias Analyzer")
st.write(
    "Paste a news article or transcript below to analyze it for specific ideological framing."
)

# Text area for user input
user_input = st.text_area("Paste text / transcript here:", height=250)

if st.button("Analyze Text", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Analyzing text layout and bias..."):
            result = analyze_text(user_input)

        if result:
            # Display percentage score
            percentage = result.get("percentage", 0)
            st.subheader(f"Identified Ideological Framing: {percentage}%")
            st.progress(percentage / 100)

            # Build and render the highlighted HTML text
            st.write("### Analyzed Text Output:")
            html_output = ""

            for snippet in result.get("analysis", []):
                text_content = snippet.get("text", "")
                if snippet.get("ideological", False):
                    # Red highlight styling for flagged text
                    html_output += (
                        f'<span style="background-color: #ffcccc; color: #cc0000; '
                        f'padding: 2px 4px; border-radius: 4px; font-weight: bold;" '
                        f'title="Flagged Framing">{text_content}</span>'
                    )
                else:
                    html_output += text_content

            # Render HTML safely inside Streamlit
            st.markdown(html_output, unsafe_allow_html=True)
