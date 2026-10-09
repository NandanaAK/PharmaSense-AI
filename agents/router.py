
def route_question(question):
    """
    PharmaSense AI Router

    Determines which specialist agents are needed
    based on the user's question.
    """

    question_lower = question.lower()

    agents = []

    # Detect compound ID
    compound_question = (
        "cmp-" in question_lower
        or "compound" in question_lower
        or "compounds" in question_lower
    )

    # Detect trial ID
    trial_question = (
        "trl-" in question_lower
        or "trial" in question_lower
        or "clinical" in question_lower
        or "study" in question_lower
    )

    # Trial-related questions
    if any(word in question_lower for word in [
        "trial",
        "clinical",
        "enrollment",
        "phase",
        "study"
    ]):
        agents.append("trial_data")

    # Literature/document questions
    if any(word in question_lower for word in [
        "literature",
        "document",
        "research",
        "publication",
        "evidence"
    ]):
        agents.append("literature")

    # Adverse event / safety questions
    if any(word in question_lower for word in [
        "adverse",
        "event",
        "safety",
        "side effect",
        "serious",
        "severe"
    ]):
        agents.append("adverse_event")

    # Compound similarity questions
    if any(word in question_lower for word in [
        "similar",
        "similarity",
        "chemical"
    ]):
        agents.append("compound_similarity")

    # If the user asks for a report about a compound,
    # gather information from all relevant specialist agents.
    if compound_question and any(word in question_lower for word in [
        "report",
        "summary",
        "overview"
    ]):
        agents.extend([
            "trial_data",
            "literature",
            "adverse_event",
            "compound_similarity"
        ])

    # Report writer is needed when a final report is requested.
    if any(word in question_lower for word in [
        "report",
        "summary",
        "overview"
    ]):
        agents.append("report_writer")

    # Remove duplicates while preserving order.
    agents = list(dict.fromkeys(agents))

    return agents


if __name__ == "__main__":

    test_questions = [
        "Which clinical trials have low enrollment?",
        "What adverse events occurred in TRL-0037?",
        "Find compounds similar to CMP-0055.",
        "Give me a literature report for CMP-0055.",
        "Give me a report for CMP-0055."
    ]

    print("\nPharmaSense AI - Router Test")
    print("=" * 60)

    for question in test_questions:

        selected_agents = route_question(question)

        print(f"\nQuestion: {question}")
        print(f"Selected Agents: {selected_agents}")

