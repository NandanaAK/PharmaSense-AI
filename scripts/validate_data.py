import duckdb
import os

# Get the main PharmaSense_AI project folder
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database path
database_path = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)

# Connect to database
conn = duckdb.connect(database_path)

print("PharmaSense AI - Data Validation")
print("=" * 60)

# Get all tables
tables = conn.execute("SHOW TABLES").fetchall()

# Check missing values in every table
for table in tables:

    table_name = table[0]

    print(f"\nTable: {table_name}")
    print("-" * 60)

    # Get column names
    columns = conn.execute(
        f"DESCRIBE {table_name}"
    ).fetchall()

    for column in columns:

        column_name = column[0]

        # Count missing values
        missing_count = conn.execute(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            WHERE "{column_name}" IS NULL
            """
        ).fetchone()[0]

        print(f"{column_name}: {missing_count} missing")

# Close connection
conn.close()

print("\nData validation completed!")