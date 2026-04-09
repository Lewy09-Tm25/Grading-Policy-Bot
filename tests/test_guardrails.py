import unittest
import logging
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
        
        # Check if the exact refusal string we programmed in prompts.py is triggered
        expected_refusal = "i cannot find this information in the cuny grade glossary"
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


if __name__ == "__main__":
    # Run the tests with high verbosity
    unittest.main(verbosity=2)