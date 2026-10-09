import os
import sys

# Add project folder to Python path
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, project_folder)

from rag.vector_search import search_documents


def build_context(results):
    """
    Prepare retrieved documents as evidence.
    """

    context_parts = []

    for _, row in results.iterrows():
        context_parts.append(
            f"Document: {row['doc_id']}\n"
            f"Title: {row['title']}\n"
            f"Evidence: {row['text']}"
        )

    return "\n\n".join(context_parts)


def run_rag(question):
    """
    Retrieve relevant evidence for a question.
    """

    print("\nRetrieving relevant evidence...")

    results = search_documents(question, top_k=5)

    context = build_context(results)

    print("\nRetrieved Evidence")
    print("=" * 60)
    print(context)

    return context


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    run_rag(question)