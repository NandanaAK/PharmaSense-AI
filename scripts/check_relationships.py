import duckdb
import os

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database_path = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)

conn = duckdb.connect(database_path)

print("PharmaSense AI - Referential Integrity Check")
print("=" * 70)

relationships = [
    ("clinical_trials", "compound_id", "compounds", "compound_id"),
    ("lab_results", "compound_id", "compounds", "compound_id"),
    ("adverse_events", "trial_id", "clinical_trials", "trial_id"),
    ("adverse_events", "site_id", "trial_sites", "site_id"),
    ("trial_sites", "trial_id", "clinical_trials", "trial_id"),
    ("research_documents", "compound_id", "compounds", "compound_id"),
    ("research_documents", "trial_id", "clinical_trials", "trial_id")
]

for child_table, child_column, parent_table, parent_column in relationships:

    query = f"""
    SELECT COUNT(*)
    FROM {child_table} AS child
    LEFT JOIN {parent_table} AS parent
        ON child."{child_column}" = parent."{parent_column}"
    WHERE child."{child_column}" IS NOT NULL
      AND parent."{parent_column}" IS NULL
    """

    missing_count = conn.execute(query).fetchone()[0]

    print(f"\n{child_table}.{child_column}")
    print(f"  → {parent_table}.{parent_column}")

    if missing_count == 0:
        print("  ✓ All references are valid")
    else:
        print(f"  ⚠ Missing references: {missing_count}")

conn.close()

print("\nReferential integrity check completed!")