
import pandas as pd
import numpy as np
import os
import re
from sentence_transformers import SentenceTransformer


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Embeddings file
embeddings_file = os.path.join(
    project_folder,
    "document_embeddings.csv"
)

print("PharmaSense AI - Vector Search")
print("=" * 60)

# Load embedding data
df = pd.read_csv(embeddings_file)

# Convert stored embeddings into vectors
df["embedding_vector"] = df["embedding"].apply(
    lambda x: np.array(
        [float(value) for value in x.split(",")],
        dtype=float
    )
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(query_embedding, document_embeddings):
    """Calculate cosine similarity between query and documents."""

    similarities = []

    query_norm = np.linalg.norm(query_embedding)

    for document_embedding in document_embeddings:
        document_norm = np.linalg.norm(document_embedding)

        if query_norm == 0 or document_norm == 0:
            similarity = 0.0
        else:
            similarity = np.dot(
                query_embedding,
                document_embedding
            ) / (query_norm * document_norm)

        similarities.append(float(similarity))

    return similarities


def search_documents(query, top_k=5):
    """Search exact compound documents or perform semantic search."""

    # Detect compound-like IDs, excluding trial IDs
    identifiers = re.findall(
        r"\b[A-Z]{2,4}-\d{3,5}\b",
        query.upper()
    )

    compound_ids = [
        identifier for identifier in identifiers
        if not identifier.startswith("TRL-")
    ]

    # Compound-specific search
    if compound_ids:
        compound_id = compound_ids[0]

        print(f"\nDetected compound ID: {compound_id}")

        # Exact metadata match only
        if "compound_id" not in df.columns:
            print(
                "Cannot perform exact compound search: "
                "compound_id column is missing."
            )
            return df.iloc[0:0].copy()

        compound_match = (
            df["compound_id"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.upper()
            .eq(compound_id)
        )

        exact_match = df[compound_match].copy()

        if exact_match.empty:
            print(f"No documents found for {compound_id}.")
            return exact_match.assign(similarity=pd.Series(dtype=float))

        print(
            f"Found {len(exact_match)} "
            f"documents for {compound_id}."
        )

        # Embed query and rank only exact compound matches
        query_embedding = model.encode(query)

        exact_match["similarity"] = calculate_similarity(
            query_embedding,
            exact_match["embedding_vector"]
        )

        exact_match = exact_match.sort_values(
            by="similarity",
            ascending=False
        )

        return exact_match.head(top_k)

    # Normal semantic search when no compound ID is present
    query_embedding = model.encode(query)

    results = df.copy()

    results["similarity"] = calculate_similarity(
        query_embedding,
        results["embedding_vector"]
    )

    results = results.sort_values(
        by="similarity",
        ascending=False
    )

    return results.head(top_k)


# Test the vector search
if __name__ == "__main__":
    query = input("\nEnter your question: ")

    results = search_documents(query)

    print("\nTop relevant documents:")
    print("=" * 60)

    if results.empty:
        print("No matching documents found.")
    else:
        for _, row in results.iterrows():
            print(f"\nDocument: {row['doc_id']}")
            print(f"Title: {row['title']}")
            print(f"Similarity: {row['similarity']:.4f}")
            print("\nText:")
            print(row["text"])
            print("-" * 60)