import os
import sys
import re
import duckdb


# =========================================================
# PROJECT SETUP
# =========================================================

project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, project_folder)

from rag.vector_search import search_documents


# =========================================================
# DATABASE PATH
# =========================================================

DATABASE_PATH = os.path.join(
    project_folder,
    "database",
    "pharmasense.duckdb"
)


# =========================================================
# SQL SEARCH - CLINICAL TRIAL DATA
# =========================================================

def search_sql(compound_id):
    """
    Search structured clinical trial data
    associated with the given compound.
    """

    con = duckdb.connect(
        DATABASE_PATH,
        read_only=True
    )

    query = """
        SELECT
            trial_id,
            compound_id,
            trial_phase,
            therapeutic_area,
            sponsor,
            start_date,
            planned_end_date,
            actual_end_date,
            status,
            target_enrollment,
            actual_enrollment,
            primary_endpoint
        FROM clinical_trials
        WHERE UPPER(compound_id) = UPPER(?)
        ORDER BY trial_id
    """

    result = con.execute(
        query,
        [compound_id]
    ).fetchdf()

    con.close()

    return result


# =========================================================
# EXTRACT ENROLLMENT FROM RESEARCH DOCUMENTS
# =========================================================

def extract_document_enrollment(text):
    """
    Extract an enrollment percentage from research
    document text.

    Example:
        'enrollment is at 57% of target'

    Returns:
        57.0
        or None if no enrollment percentage is found.
    """

    if not text:
        return None

    patterns = [
        r"enrollment\s+(?:is\s+)?(?:at\s+)?(\d+(?:\.\d+)?)\s*%",
        r"enrolled\s+(\d+(?:\.\d+)?)\s*%",
        r"enrollment\s+completion\s+(?:rate\s+)?(?:is\s+)?(\d+(?:\.\d+)?)\s*%"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return float(
                match.group(1)
            )

    return None


# =========================================================
# CALCULATE DATABASE ENROLLMENT
# =========================================================

def calculate_database_enrollment(sql_results):
    """
    Calculate enrollment percentage from the
    clinical_trials table.

    Formula:

        actual enrollment / target enrollment * 100
    """

    if sql_results is None:
        return None

    if len(sql_results) == 0:
        return None

    required_columns = [
        "target_enrollment",
        "actual_enrollment"
    ]

    for column in required_columns:

        if column not in sql_results.columns:
            return None

    enrollment_values = []

    for _, row in sql_results.iterrows():

        target = row["target_enrollment"]
        actual = row["actual_enrollment"]

        if target is None or actual is None:
            continue

        if target == 0:
            continue

        percentage = (
            float(actual)
            / float(target)
            * 100
        )

        enrollment_values.append(
            {
                "trial_id": row["trial_id"],
                "target_enrollment": target,
                "actual_enrollment": actual,
                "percentage": round(
                    percentage,
                    2
                )
            }
        )

    return enrollment_values


# =========================================================
# DETECT EVIDENCE CONFLICTS
# =========================================================

def detect_conflicts(
    rag_results,
    sql_results
):
    """
    Compare structured clinical trial evidence
    with research-document evidence.

    Currently checks enrollment percentages.
    """

    conflicts = []

    database_enrollment = (
        calculate_database_enrollment(
            sql_results
        )
    )

    if not database_enrollment:

        return conflicts

    for _, row in rag_results.iterrows():

        document_text = str(
            row.get(
                "text",
                ""
            )
        )

        document_enrollment = (
            extract_document_enrollment(
                document_text
            )
        )

        if document_enrollment is None:

            continue

        # Compare the document percentage
        # against each relevant clinical trial.
        for trial in database_enrollment:

            difference = round(
                abs(
                    trial["percentage"]
                    - document_enrollment
                ),
                2
            )

            # Differences greater than
            # 1 percentage point are flagged.
            if difference > 1:

                conflicts.append(
                    {
                        "type": (
                            "enrollment_discrepancy"
                        ),
                        "document_id": row.get(
                            "doc_id",
                            "N/A"
                        ),
                        "document_title": row.get(
                            "title",
                            "N/A"
                        ),
                        "trial_id": trial[
                            "trial_id"
                        ],
                        "database_value": trial[
                            "percentage"
                        ],
                        "document_value": (
                            document_enrollment
                        ),
                        "difference": difference
                    }
                )

    return conflicts


# =========================================================
# EVIDENCE FUSION
# =========================================================

def fuse_evidence(
    question,
    compound_id=None
):
    """
    Combine RAG evidence with structured
    clinical trial evidence and detect
    potential discrepancies.
    """

    print("\n" + "=" * 60)
    print("PHARMASENSE AI - EVIDENCE FUSION")
    print("=" * 60)

    # -----------------------------------------------------
    # 1. RETRIEVE RESEARCH DOCUMENTS
    # -----------------------------------------------------

    print(
        "\n[1] Retrieving research documents..."
    )

    rag_query = question

    if compound_id:

        rag_query = (
            f"{question} {compound_id}"
        )

    rag_results = search_documents(
        rag_query,
        top_k=5
    )

    print(
        f"Retrieved {len(rag_results)} "
        f"research documents."
    )

    # -----------------------------------------------------
    # 2. SEARCH STRUCTURED CLINICAL TRIAL DATABASE
    # -----------------------------------------------------

    print(
        "\n[2] Searching structured "
        "clinical trial database..."
    )

    sql_results = None

    if compound_id:

        sql_results = search_sql(
            compound_id
        )

        if len(sql_results) > 0:

            print(
                f"Found {len(sql_results)} "
                f"clinical trial(s) for "
                f"{compound_id}."
            )

        else:

            print(
                f"No clinical trials found "
                f"for {compound_id}."
            )

    else:

        print(
            "No compound ID provided."
        )

    # -----------------------------------------------------
    # 3. DETECT CONFLICTS
    # -----------------------------------------------------

    print(
        "\n[3] Checking for evidence discrepancies..."
    )

    conflicts = detect_conflicts(
        rag_results,
        sql_results
    )

    if conflicts:

        print(
            f"Detected {len(conflicts)} "
            f"potential evidence discrepancy."
        )

    else:

        print(
            "No evidence discrepancies detected."
        )

    # -----------------------------------------------------
    # 4. DISPLAY COMBINED EVIDENCE
    # -----------------------------------------------------

    print(
        "\n[4] Combined Evidence"
    )

    print("=" * 60)

    # -----------------------------------------------------
    # RESEARCH EVIDENCE
    # -----------------------------------------------------

    print(
        "\n--- Research Evidence ---"
    )

    if len(rag_results) > 0:

        for _, row in rag_results.iterrows():

            print(
                f"\nDocument: "
                f"{row['doc_id']}"
            )

            print(
                f"Title: "
                f"{row['title']}"
            )

            print(
                f"Trial ID: "
                f"{row.get('trial_id', 'N/A')}"
            )

            print(
                f"Evidence: "
                f"{row['text']}"
            )

    else:

        print(
            "No research evidence available."
        )

    # -----------------------------------------------------
    # STRUCTURED CLINICAL TRIAL EVIDENCE
    # -----------------------------------------------------

    print(
        "\n--- Structured Clinical Trial Evidence ---"
    )

    if (
        sql_results is not None
        and len(sql_results) > 0
    ):

        print(
            sql_results.to_string(
                index=False
            )
        )

    else:

        print(
            "No structured clinical trial "
            "evidence available."
        )

    # -----------------------------------------------------
    # ENROLLMENT CALCULATION
    # -----------------------------------------------------

    database_enrollment = (
        calculate_database_enrollment(
            sql_results
        )
    )

    if database_enrollment:

        print(
            "\n--- Database Enrollment Analysis ---"
        )

        for trial in database_enrollment:

            print(
                f"Trial ID: "
                f"{trial['trial_id']}"
            )

            print(
                f"Target Enrollment: "
                f"{trial['target_enrollment']}"
            )

            print(
                f"Actual Enrollment: "
                f"{trial['actual_enrollment']}"
            )

            print(
                f"Enrollment Progress: "
                f"{trial['percentage']}%"
            )

    # -----------------------------------------------------
    # CONFLICT REPORT
    # -----------------------------------------------------

    print(
        "\n--- Evidence Consistency Check ---"
    )

    if conflicts:

        for conflict in conflicts:

            print(
                "\n⚠ POTENTIAL EVIDENCE DISCREPANCY"
            )

            print(
                f"Document: "
                f"{conflict['document_id']}"
            )

            print(
                f"Title: "
                f"{conflict['document_title']}"
            )

            print(
                f"Trial ID: "
                f"{conflict['trial_id']}"
            )

            print(
                "Database enrollment: "
                f"{conflict['database_value']}%"
            )

            print(
                "Document enrollment: "
                f"{conflict['document_value']}%"
            )

            print(
                "Difference: "
                f"{conflict['difference']} "
                "percentage points"
            )

            print(
                "Action: "
                "Flag for human review."
            )

    else:

        print(
            "No conflicts detected between "
            "the available evidence sources."
        )

    # -----------------------------------------------------
    # RETURN ALL EVIDENCE
    # -----------------------------------------------------

    return {
        "question": question,
        "compound_id": compound_id,
        "rag_results": rag_results,
        "sql_results": sql_results,
        "database_enrollment": (
            database_enrollment
        ),
        "conflicts": conflicts
    }


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    question = input(
        "\nEnter your question: "
    )

    compound_id = input(
        "Enter compound ID "
        "(example CMP-0055), "
        "or press Enter to skip: "
    ).strip()

    if compound_id == "":
        compound_id = None

    fuse_evidence(
        question,
        compound_id
    )