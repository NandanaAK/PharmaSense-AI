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

# Business question:
# Which Phase II oncology trials are below 60% enrollment?

query = """
SELECT
    trial_id,
    compound_id,
    trial_phase,
    therapeutic_area,
    target_enrollment,
    actual_enrollment,
    ROUND(
        actual_enrollment * 100.0 / NULLIF(target_enrollment, 0),
        2
    ) AS enrollment_percentage
FROM clinical_trials
WHERE trial_phase = 'Phase II'
  AND therapeutic_area = 'Oncology'
  AND actual_enrollment < target_enrollment * 0.60
ORDER BY enrollment_percentage;
"""

# Run the SQL query
result = conn.execute(query).fetchdf()

print("\nPhase II Oncology Trials Below 60% Enrollment")
print("=" * 70)

if result.empty:
    print("No matching trials found.")
else:
    print(result.to_string(index=False))

# Close connection
conn.close()