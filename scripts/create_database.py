import pandas as pd
import duckdb
import os

# Get the main PharmaSense_AI project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database location
database_folder = os.path.join(project_folder, "database")
database_path = os.path.join(database_folder, "pharmasense.duckdb")

# Our 7 CSV files
files = [
    "adverse_events.csv",
    "agent_interaction_logs.csv",
    "clinical_trials.csv",
    "compounds.csv",
    "lab_results.csv",
    "research_documents.csv",
    "trial_sites.csv"
]

# Connect to DuckDB
conn = duckdb.connect(database_path)

print("Creating PharmaSense AI database")
print("=" * 50)

# Load each CSV into a DuckDB table
for file in files:

    # Table name = CSV filename without .csv
    table_name = os.path.splitext(file)[0]

    # Full CSV path
    file_path = os.path.join(project_folder, file)

    # Read CSV
    df = pd.read_csv(file_path)

    # Register dataframe temporarily
    conn.register("temp_df", df)

    # Create table in DuckDB
    conn.execute(
        f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM temp_df"
    )

    # Remove temporary dataframe registration
    conn.unregister("temp_df")

    print(f"✓ {table_name}: {len(df)} rows loaded")

# Close database connection
conn.close()

print("\nDatabase created successfully!")
print(f"Location: {database_path}")