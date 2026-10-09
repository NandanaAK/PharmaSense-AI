import pandas as pd
import os
from sentence_transformers import SentenceTransformer


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Input file containing document chunks
input_file = os.path.join(
    project_folder,
    "research_document_chunks.csv"
)

# Output file for embeddings
output_file = os.path.join(
    project_folder,
    "document_embeddings.csv"
)


print("PharmaSense AI - Creating Document Embeddings")
print("=" * 60)

# Load chunks
df = pd.read_csv(input_file)

print(f"Total chunks: {len(df)}")

# Load embedding model
print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")

# Create embeddings
print("\nCreating embeddings...")

embeddings = model.encode(
    df["text"].tolist(),
    show_progress_bar=True
)

# Convert embeddings to strings so they can be saved in CSV
df["embedding"] = [
    ",".join(map(str, embedding))
    for embedding in embeddings
]

# Save embeddings
df.to_csv(
    output_file,
    index=False
)

print("\nEmbeddings created successfully!")
print(f"Total embeddings: {len(embeddings)}")
print(f"Embedding size: {len(embeddings[0])}")

print("\nSaved to:")
print(output_file)