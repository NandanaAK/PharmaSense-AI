import duckdb
import os


def get_trial_for_compound(compound_id):
    """
    Find the clinical trial associated with a compound.
    """

    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    database_file = os.path.join(
        project_folder,
        "database",
        "pharmasense.duckdb"
    )

    connection = duckdb.connect(database_file)

    query = """
        SELECT
            trial_id,
            compound_id,
            trial_phase,
            therapeutic_area,
            status
        FROM clinical_trials
        WHERE UPPER(compound_id) = UPPER(?)
        ORDER BY trial_id
        LIMIT 1
    """

    result = connection.execute(
        query,
        [compound_id]
    ).fetchone()

    connection.close()

    if result is None:
        return None

    return {
        "trial_id": result[0],
        "compound_id": result[1],
        "trial_phase": result[2],
        "therapeutic_area": result[3],
        "status": result[4]
    }


if __name__ == "__main__":

    compound_id = "CMP-0055"

    result = get_trial_for_compound(compound_id)

    print("\nPharmaSense AI - Compound Trial Lookup")
    print("=" * 60)

    print(f"\nCompound ID: {compound_id}")

    if result:
        print(f"Trial ID: {result['trial_id']}")
        print(f"Trial Phase: {result['trial_phase']}")
        print(f"Therapeutic Area: {result['therapeutic_area']}")
        print(f"Status: {result['status']}")
    else:
        print("No trial found.")