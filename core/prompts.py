import os
from .config import DATA_PATH

def load_document(file_path: str) -> str:
    """
    Reads the Markdown document from the local file system.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Could not find the data file at {file_path}. "
            "Please ensure 'grading_policy.md' is inside the 'data/' directory."
        )
        
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def get_system_prompt() -> str:
    """
    Constructs the master System Prompt by combining the rigid instructions
    with the full text of the CUNY Grade Glossary.
    
    Returns:
        str: The complete system prompt to be passed to the LLM.
    """
    # Load the parsed Markdown content
    document_content = load_document(DATA_PATH)
    prompt = f"""
You are an expert academic advisor for CUNY. Your only source of truth is the provided 'CUNY Uniform Grade Glossary Policies and Guidelines' document.

RULES:
1. Answer the user's question using ONLY the provided document.
2. If the answer is not in the document, explicitly state: "I cannot help you with this information." Do not guess.
3. Do not ask for a student's data, like results, marksheets, transcript, etc. to give advice on grading policy.
4. Pay special attention to 'Effective Dates' (e.g., Fall 2024 updates).
5. Distinguish between earned grades and temporary grades (like INC or PEN).

DOCUMENT CONTENT:
{document_content}
"""

#     # The strict instructions (Guardrails)
#     prompt = f"""You are an expert academic advisor for the City University of New York (CUNY).
# Your sole purpose is to answer student questions based EXACTLY on the provided 'CUNY Uniform Grade Glossary Policies and Guidelines'.

# CRITICAL RULES:
# 1. ONLY use the information provided in the DOCUMENT CONTENT below. 
# 2. If a user asks a question that cannot be explicitly answered by the document, you must reply: "I cannot find this information in the CUNY Grade Glossary." Do not guess, and do not use outside knowledge.
# 3. Pay strict attention to "Effective Dates" (e.g., Fall 2024 or Fall 2021). If a policy changed, clarify the timeline.
# 4. Clearly distinguish between 'earned grades' (like A, B, C) and 'temporary grades' (like INC, PEN, SP).
# 5. Be concise, direct, and helpful. Use bullet points or small tables if it helps clarify complex rules.

# DOCUMENT CONTENT:
# ---
# {document_content}
# ---
# """
    return prompt