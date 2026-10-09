import pandas as pd
import os

# Get the main PharmaSense_AI project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Names of our 7 datasets
files = [
    "adverse_events.csv",
    "agent_interaction_logs.csv",
    "clinical_trials.csv",
    "compounds.csv",
    "lab_results.csv",
    "research_documents.csv",
    "trial_sites.csv"
]

print("PharmaSense AI - Data Loading")
print("=" * 50)

for file in files:

    # Create the complete path to the CSV file
    file_path = os.path.join(project_folder, file)

    # Read the CSV file
    df = pd.read_csv(file_path)

    # Display basic information
    print(f"\nTable: {file}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")