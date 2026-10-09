
import os
import sys
import duckdb

PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_FOLDER)

from agents.router import route_question
from agents.id_extractor import extract_compound_id, extract_trial_id
from agents.compound_trial_lookup import get_trial_for_compound

from agents.trial_data_agent import trial_data_agent
from agents.literature_research_agent import literature_research_agent
from agents.adverse_event_agent import adverse_event_agent
from agents.compound_similarity_agent import compound_similarity_agent
from agents.evidence_fusion import fuse_evidence
from agents.report_writer_agent import report_writer_agent


def validate_compound_id(compound_id):
    """Check whether a compound ID exists in the DuckDB database."""

    database_path = os.path.join(
        PROJECT_FOLDER, "database", "pharmasense.duckdb"
    )

    connection = duckdb.connect(database_path, read_only=True)

    try:
        result = connection.execute(
            "SELECT 1 FROM compounds WHERE compound_id = ? LIMIT 1",
            [compound_id]
        ).fetchone()

        return result is not None
    finally:
        connection.close()


def orchestrate(question):
    """
    PharmaSense AI Orchestrator

    Validates compound IDs, routes the question, runs specialist
    agents and evidence fusion, then creates a final report.
    """

    print("\nPharmaSense AI - Orchestrator")
    print("=" * 60)

    compound_id = extract_compound_id(question)
    trial_id = extract_trial_id(question)

    print("\nDetected IDs:")
    print(f"- Compound ID: {compound_id or 'Not detected'}")
    print(f"- Trial ID: {trial_id or 'Not detected'}")

    # Validate the compound before running any agents
    if compound_id:
        print("\nValidating compound ID...")

        try:
            is_valid = validate_compound_id(compound_id)
        except Exception as error:
            print(f"Compound validation failed: {error}")

            return {
                "status": "validation_failed",
                "message": (
                    "Unable to validate the compound ID because "
                    "the database could not be checked."
                ),
                "compound_id": compound_id,
                "selected_agents": [],
                "trial_data": None,
                "literature_data": None,
                "adverse_event_data": None,
                "compound_similarity_data": None,
                "evidence_fusion_data": None
            }

        if not is_valid:
            message = (
                f"Compound {compound_id} was not found in the database. "
                "Please check the compound ID and try again."
            )
            print(f"\n{message}")

            return {
                "status": "invalid_compound",
                "message": message,
                "compound_id": compound_id,
                "selected_agents": [],
                "trial_data": None,
                "literature_data": None,
                "adverse_event_data": None,
                "compound_similarity_data": None,
                "evidence_fusion_data": None
            }

        print(f"Compound {compound_id} found.")

    # Route only after compound validation
    selected_agents = route_question(question)

    print("\nUser Question:")
    print(question)

    print("\nSelected Agents:")
    for agent in selected_agents:
        print(f"- {agent}")

    # Find trial associated with compound if needed
    if not trial_id and compound_id:
        print("\nLooking up trial associated with compound...")

        try:
            trial_info = get_trial_for_compound(compound_id)

            if trial_info:
                trial_id = trial_info["trial_id"]
                print(f"Trial ID found from compound: {trial_id}")
            else:
                print("No clinical trial found for this compound.")

        except Exception as error:
            print(f"Trial lookup failed: {error}")

    trial_data = None
    literature_data = None
    adverse_event_data = None
    compound_similarity_data = None
    evidence_fusion_data = None

    # Trial Data Agent
    if "trial_data" in selected_agents:
        print("\nRunning Trial Data Agent...")

        try:
            trial_data = trial_data_agent(question)
        except Exception as error:
            print(f"\nTrial Data Agent failed: {error}")
            trial_data = {
                "status": "failed",
                "error": str(error)
            }

    # Literature Research Agent
    if "literature" in selected_agents:
        print("\nRunning Literature Research Agent...")

        try:
            literature_data = literature_research_agent(
                question,
                top_k=5
            )
        except Exception as error:
            print(f"\nLiterature Research Agent failed: {error}")
            literature_data = {
                "status": "failed",
                "error": str(error),
                "documents": []
            }

    # Adverse Event Agent
    if "adverse_event" in selected_agents:
        print("\nRunning Adverse Event Agent...")

        try:
            if trial_id:
                adverse_event_data = adverse_event_agent(trial_id)
            else:
                adverse_event_data = {
                    "status": "skipped",
                    "reason": "No trial ID could be determined.",
                    "trial_id": None
                }
        except Exception as error:
            print(f"\nAdverse Event Agent failed: {error}")
            adverse_event_data = {
                "status": "failed",
                "error": str(error),
                "trial_id": trial_id
            }

    # Compound Similarity Agent
    if "compound_similarity" in selected_agents:
        print("\nRunning Compound Similarity Agent...")

        try:
            if compound_id:
                compound_similarity_data = compound_similarity_agent(
                    compound_id,
                    top_n=5
                )
            else:
                compound_similarity_data = {
                    "status": "skipped",
                    "reason": "No compound ID detected.",
                    "similar_compounds": []
                }
        except Exception as error:
            print(f"\nCompound Similarity Agent failed: {error}")
            compound_similarity_data = {
                "status": "failed",
                "error": str(error),
                "similar_compounds": []
            }

    # Evidence Fusion
    if compound_id:
        print("\nRunning Evidence Fusion...")

        try:
            evidence_fusion_data = fuse_evidence(
                question=question,
                compound_id=compound_id
            )
        except Exception as error:
            print(f"\nEvidence Fusion failed: {error}")
            evidence_fusion_data = None
    else:
        print("\nEvidence Fusion skipped: No compound ID detected.")

    # Report Writer Agent
    if "report_writer" in selected_agents:
        print("\nRunning Report Writer Agent...")

        try:
            final_report = report_writer_agent(
                question=question,
                trial_data=trial_data,
                literature_data=literature_data,
                adverse_event_data=adverse_event_data,
                compound_similarity_data=compound_similarity_data,
                evidence_fusion_data=evidence_fusion_data
            )

            return final_report

        except Exception as error:
            print(f"\nReport Writer Agent failed: {error}")

            return {
                "status": "failed",
                "error": str(error),
                "trial_data": trial_data,
                "literature_data": literature_data,
                "adverse_event_data": adverse_event_data,
                "compound_similarity_data": compound_similarity_data,
                "evidence_fusion_data": evidence_fusion_data
            }

    return {
        "selected_agents": selected_agents,
        "trial_data": trial_data,
        "literature_data": literature_data,
        "adverse_event_data": adverse_event_data,
        "compound_similarity_data": compound_similarity_data,
        "evidence_fusion_data": evidence_fusion_data
    }



if __name__ == "__main__":
    question = "Give me a report for CMP-0055."

    result = orchestrate(question)

    print("\nFINAL RESULT")
    print("=" * 60)
    print(result)