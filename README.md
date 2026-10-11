An AI-powered media analysis tool built to evaluate German public broadcasting (ÖRR) content. Instead of manually parsing complex transcripts for political bias, this tool allows media researchers to paste any news article or video transcript to instantly trigger an automated framing analysis that outputs an ideological density score and inline visual highlights.

Features
Dynamic Content Parsing: Accepts raw news text or long-form video transcripts directly via a responsive web layer.
Automated Bias Detection: Uses OpenAI (gpt-4o-mini) with strict deterministic parameters to evaluate left-liberal or "woke" framing, moralizing language, and identity politics narratives.
Strict Schema Enforcement: Leverages Pydantic v2 validation to guarantee a standardized JSON payload, isolating precise text coordinates and mapping a reliable global density percentage score.
Inline Target Auditing: Dynamically injects highly visible HTML/CSS styling onto the front-end to isolate and highlight flagged text segments in real-time.
Production-Ready Security: Supports isolated environment-based credential loading (.env) to keep sensitive OpenAI API keys secure and separate from source code.

Tech Stack
Language: Python 3.10+
Framework: Streamlit (Agile Web UI Layer)
AI Processing: OpenAI API (gpt-4o-mini via Structured Outputs)
Validation: Pydantic v2 (Strict Data Formatting)
