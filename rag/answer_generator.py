import os
import sys

# Add project folder to Python path
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, project_folder)

from rag.vector_search import search_documents


def generate_answer(question):
    """
    Generate a simple evidence-based answer
    from the retrieved research documents.
    """

    results = search_documents(question, top_k=5)

    print("\nEvidence-based answer")
    print("=" * 60)

    # Use the highest-priority retrieved document
    first_result = results.iloc[0]

    print(f"Based on the available research evidence, "
          f"{first_result['text']}")

    print("\nSource:")
    print(f"{first_result['doc_id']} - {first_result['title']}")


if __name__ == "__main__":

    question = input("\nEnter your question: ")

    generate_answer(question)