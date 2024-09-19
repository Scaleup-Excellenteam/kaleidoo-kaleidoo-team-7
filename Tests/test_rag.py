import pytest
from models import genai_model
from TextProcessorSingleton import TextProcessorSingleton
text_processor = TextProcessorSingleton.get_instance()

EVAL_PROMPT = """
Question: {actual_response}
Answer according to the following contents:
Contents: {best_match}

---

(Answer 'true' or 'false')
"""


def test_rag_llm_answer():
    assert query_and_validate(
        question="האם הפועל תל אביב אלופה?",
        expected_response="true",
    )


def query_and_validate(question: str, expected_response: str) -> bool:
    best_match = text_processor.find_best_match(question, top_k=1)
    best_match_str = "\n".join([f"{match[0]} (Score: {match[1]})" for match in best_match])

    prompt = EVAL_PROMPT.format(actual_response=question, expected_response=expected_response, best_match=best_match_str)

    # Log the prompt for debugging
    print(f"Prompt sent to model:\n{prompt}")

    # Call your LLM model to get the actual response
    actual_response = genai_model.generate_content(prompt)

    # Log or print the actual response for debugging
    print(f"Actual Response: {actual_response.text}")
    print(f"expected Response: {expected_response}")

    # Compare the model's response to the expected response
    return actual_response.text.lower().strip() == expected_response.lower().strip()