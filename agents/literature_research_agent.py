from rag.vector_search import search_documents


def literature_research_agent(query, top_k=5):
    """
    Literature & Document Research Agent

    Searches the research document collection and returns
    relevant documents for the user's query.
    """

    results = search_documents(
        query,
        top_k=top_k
    )

    if results.empty:
        return {
            "query": query,
            "documents": []
        }

    documents = results[
        [
            "doc_id",
            "compound_id",
            "trial_id",
            "doc_type",
            "title",
            "chunk_id",
            "text",
            "similarity"
        ]
    ].to_dict(orient="records")

    return {
        "query": query,
        "documents": documents
    }


if __name__ == "__main__":

    query = "CMP-0055"

    result = literature_research_agent(
        query,
        top_k=5
    )

    print("\nPharmaSense AI - Literature Research Agent")
    print("=" * 60)

    print(f"\nQuery: {result['query']}")

    print("\nRelevant Documents:")

    for document in result["documents"]:
        print(
            f"\nDocument ID: {document['doc_id']}"
            f"\nTitle: {document['title']}"
            f"\nType: {document['doc_type']}"
            f"\nTrial ID: {document['trial_id']}"
            f"\nSimilarity: {document['similarity']:.4f}"
            f"\nText: {document['text']}"
        )