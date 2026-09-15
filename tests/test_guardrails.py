import unittest
import logging
import re
from core.prompts import get_system_prompt
from client.llm_client import stream_openai_response

# ==========================================
# 1. Logging Configuration for Tests
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [TEST] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class TestCunyBotGuardrails(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """This runs once before any tests start. It loads the system prompt."""
        logger.info("Initializing Test Suite...")
        cls.system_prompt = get_system_prompt()
        logger.info("System prompt loaded successfully.")

    def ask_bot(self, user_question: str) -> str:
        """Helper function to simulate the chat history, call the stream, and compile the result."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_question}
        ]
        
        logger.info(f"Question: '{user_question}'")
        
        # Collect the streamed chunks into a single final string
        stream = stream_openai_response(messages)
        final_answer = "".join([chunk for chunk in stream])
        
        logger.info(f"Answer: {final_answer}\n")
        return final_answer.lower() # Lowercase for easier assertion checking

    # ==========================================
    # 2. The Test Cases
    # ==========================================
    
    def test_in_domain_factual(self):
        """Test if the bot correctly retrieves strict numerical facts."""
        logger.info("Running Test: In-Domain Factual Retrieval")
        answer = self.ask_bot("How many quality points is an A- worth?")
        
        # We don't check the whole sentence, just the critical data point
        self.assertIn("3.7", answer, "Bot failed to retrieve the correct quality points for A-.")

    def test_out_of_domain_hallucination(self):
        """Test if the bot refuses to answer questions outside the provided document."""
        logger.info("Running Test: Out-of-Domain Hallucination Check")
        answer = self.ask_bot("What is the cost of tuition for an out-of-state student at Hunter College?")
        
        # The bot should refuse gracefully with the scope phrase from prompts.py (Rule 3)
        expected_refusal = "outside the scope of the cuny uniform grade glossary"
        self.assertIn(expected_refusal, answer, "Bot hallucinated an answer instead of refusing.")

    def test_temporal_policy_change(self):
        """Test if the bot recognizes date-specific policy changes (Fall 2021)."""
        logger.info("Running Test: Temporal Policy Change (Fall 2021 WU grade)")
        answer = self.ask_bot("What happens to my GPA if I get a WU grade after Fall 2021?")
        
        # The document states it will not have a punitive impact
        self.assertTrue(
            "not have" in answer and "punitive" in answer or "no impact" in answer,
            "Bot failed to recognize the Fall 2021 WU grade policy change."
        )

    def test_temporary_vs_earned_grades(self):
        """Test if the bot successfully distinguishes between grade types."""
        logger.info("Running Test: Distinguishing Grade Types (INC)")
        answer = self.ask_bot("Is INC an earned grade or a temporary grade? What happens if I don't finish it?")
        
        self.assertIn("temporary", answer, "Bot failed to classify INC as a temporary grade.")
        self.assertIn("fin", answer, "Bot failed to mention the lapse to an FIN grade.")

    # ==========================================
    # 3. Partial-answer and graceful-refusal cases
    # ==========================================

    def test_partial_answer_never_attended(self):
        """Q2: 'never attended' is in the document (WN); death is not. The bot must
        still surface WN and not refuse the whole question."""
        logger.info("Running Test: Partial Answer (died + never attended -> WN)")
        answer = self.ask_bot("What grade should a student receive if they died and never attended?")

        # WN as a standalone token, so 'known'/'shown' etc. don't falsely match
        self.assertTrue(
            re.search(r"\bwn\b", answer),
            "Bot failed to surface the WN grade for a student who never participated."
        )

    def test_partial_answer_cheating(self):
        """Q3: cheating is governed by the Academic Integrity Policy. The document's
        relevant mechanism is the PEN grade / academic review process, not a direct F."""
        logger.info("Running Test: Partial Answer (cheating -> academic review / PEN)")
        answer = self.ask_bot("Can I give a student an F if he cheated on one test?")

        self.assertTrue(
            "integrity" in answer or "review" in answer or "pending" in answer,
            "Bot failed to reference the academic review process / PEN grade for a cheating case."
        )

    def test_out_of_scope_redirect(self):
        """Q1 (correct behavior): advance notice of a withdrawal grade is not in the
        document. The bot should refuse gracefully using the scope phrase."""
        logger.info("Running Test: Graceful Out-of-Scope Redirect (withdrawal-grade notice)")
        answer = self.ask_bot("Do I need to tell the student ahead of time which withdrawal grade I am giving?")

        self.assertIn(
            "outside the scope of the cuny uniform grade glossary",
            answer,
            "Bot failed to give the graceful out-of-scope response."
        )


if __name__ == "__main__":
    # Run the tests with high verbosity
    unittest.main(verbosity=2)