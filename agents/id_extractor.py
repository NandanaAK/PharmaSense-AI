import re


def extract_compound_id(question):
    """
    Extract a compound ID such as CMP-0055 from a question.
    """

    match = re.search(
        r"\bCMP-\d+\b",
        question.upper()
    )

    if match:
        return match.group(0)

    return None


def extract_trial_id(question):
    """
    Extract a trial ID such as TRL-0037 from a question.
    """

    match = re.search(
        r"\bTRL-\d+\b",
        question.upper()
    )

    if match:
        return match.group(0)

    return None


if __name__ == "__main__":

    test_question = "Give me a report for CMP-0055 and TRL-0037."

    compound_id = extract_compound_id(test_question)
    trial_id = extract_trial_id(test_question)

    print("Question:")
    print(test_question)

    print("\nExtracted Compound ID:")
    print(compound_id)

    print("\nExtracted Trial ID:")
    print(trial_id)