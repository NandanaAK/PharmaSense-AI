import duckdb
import os

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database_path = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)

conn = duckdb.connect(database_path)

tables = conn.execute("SHOW TABLES").fetchall()

print("PharmaSense AI - Data Inspection")
print("=" * 70)

for table in tables:
    table_name = table[0]

    print(f"\nTable: {table_name}")
    print("-" * 70)

    print("\nColumns and Data Types:")
    columns = conn.execute(f"DESCRIBE {table_name}").fetchall()

    for column in columns:
        print(f"  {column[0]} → {column[1]}")

    print("\nFirst 3 Records:")
    sample = conn.execute(
        f"SELECT * FROM {table_name} LIMIT 3"
    ).fetchdf()

    print(sample.to_string(index=False))

conn.close()

print("\nData inspection completed!")