import pandas as pd
import os


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Location of the research documents CSV
csv_file = os.path.join(
    project_folder,
    "research_documents.csv"
)


# Load the dataset
df = pd.read_csv(csv_file)

print("PharmaSense AI - Research Document Preparation")
print("=" * 60)

print(f"Total documents: {len(df)}")

print("\nColumns:")
for column in df.columns:
    print(f"  - {column}")

print("\nFirst document:")
print("-" * 60)
print(df["full_text"].iloc[0])

print("\nDocument preparation completed!")