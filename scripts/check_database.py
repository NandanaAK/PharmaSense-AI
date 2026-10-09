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

# Connect to the database
conn = duckdb.connect(database_path)

print("Tables in PharmaSense AI database")
print("=" * 50)

# Get all tables
tables = conn.execute("SHOW TABLES").fetchall()

# Check each table
for table in tables:

    table_name = table[0]

    # Count rows
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"✓ {table_name}: {count} rows")

# Close connection
conn.close()

print("\nDatabase check completed successfully!")