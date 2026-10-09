import duckdb
import os


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# Database path
database_file = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)


def run_sql_query(query):
    """
    Execute a SQL query on the PharmaSense AI database
    and return the result.
    """

    connection = duckdb.connect(
        database_file,
        read_only=True
    )

    try:
        result = connection.execute(query).fetchdf()
        return result

    finally:
        connection.close()


if __name__ == "__main__":

    query = """
    SELECT
        trial_id,
        compound_id,
        trial_phase,
        therapeutic_area,
        target_enrollment,
        actual_enrollment,
        ROUND(
            actual_enrollment * 100.0
            / target_enrollment,
            2
        ) AS enrollment_percentage
    FROM clinical_trials
    WHERE actual_enrollment < target_enrollment * 0.60
    ORDER BY enrollment_percentage;
    """

    result = run_sql_query(query)

    print("\nSQL Tool Result:")
    print("=" * 60)
    print(result)