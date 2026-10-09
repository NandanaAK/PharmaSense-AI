import duckdb
import os

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database_path = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)

conn = duckdb.connect(database_path)

primary_keys = {
    "adverse_events": "event_id",
    "agent_interaction_logs": "log_id",
    "clinical_trials": "trial_id",
    "compounds": "compound_id",
    "lab_results": "result_id",
    "research_documents": "doc_id",
    "trial_sites": "site_id"
}

print("PharmaSense AI - Duplicate ID Check")
print("=" * 60)

for table_name, id_column in primary_keys.items():

    duplicates = conn.execute(
        f"""
        SELECT "{id_column}", COUNT(*) AS count
        FROM {table_name}
        GROUP BY "{id_column}"
        HAVING COUNT(*) > 1
        ORDER BY count DESC
        """
    ).fetchall()

    print(f"\nTable: {table_name}")
    print(f"ID column: {id_column}")

    if duplicates:
        print(f"⚠ Duplicate IDs found: {len(duplicates)}")

        for row in duplicates[:10]:
            print(f"  {row[0]} -> {row[1]} records")

    else:
        print("✓ No duplicate IDs found")

conn.close()

print("\nDuplicate ID check completed!")