import pandas as pd
import os


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Research documents CSV
csv_file = os.path.join(
    project_folder,
    "research_documents.csv"
)

# Load documents
df = pd.read_csv(csv_file)


def create_chunks(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    """

    if pd.isna(text):
        return []

    text = str(text)

    chunks = []
    start = 0

    while start < len(text):

        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


print("PharmaSense AI - Document Chunking")
print("=" * 60)

all_chunks = []

for _, row in df.iterrows():

    chunks = create_chunks(row["full_text"])

    for i, chunk in enumerate(chunks):

        all_chunks.append({
            "doc_id": row["doc_id"],
            "compound_id": row["compound_id"],
            "trial_id": row["trial_id"],
            "doc_type": row["doc_type"],
            "title": row["title"],
            "chunk_id": i,
            "text": chunk
        })


chunks_df = pd.DataFrame(all_chunks)

print(f"Total documents: {len(df)}")
print(f"Total chunks created: {len(chunks_df)}")

print("\nFirst chunk:")
print("-" * 60)
print(chunks_df.iloc[0]["text"])

# Save chunks
output_file = os.path.join(
    project_folder,
    "research_document_chunks.csv"
)

chunks_df.to_csv(
    output_file,
    index=False
)

print("\nChunks saved to:")
print(output_file)

print("\nDocument chunking completed!")