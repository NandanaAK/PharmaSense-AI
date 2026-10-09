
def report_writer_agent(
    question,
    trial_data=None,
    literature_data=None,
    adverse_event_data=None,
    compound_similarity_data=None,
    evidence_fusion_data=None
):
    """
    Combines specialist agent results and evidence
    fusion findings into a structured final report.
    """

    report = []

    # HEADER
    report.append("PHARMASENSE AI - FINAL REPORT")
    report.append("=" * 60)
    report.append(f"\nUser Question:\n{question}")

    # 1. TRIAL DATA
    if trial_data:
        report.append("\n\n1. TRIAL DATA")
        report.append("-" * 40)

        if isinstance(trial_data, dict):
            status = trial_data.get("status")

            if status == "failed":
                report.append(
                    "Trial Data Agent could not complete the analysis."
                )
                report.append(
                    "The structured trial data analysis is temporarily unavailable."
                )
            elif status == "skipped":
                report.append("Trial Data Agent was skipped.")
            else:
                report.append(str(trial_data))
        else:
            report.append(str(trial_data))

    # 2. LITERATURE & DOCUMENT EVIDENCE
    if literature_data:
        report.append("\n\n2. LITERATURE & DOCUMENT EVIDENCE")
        report.append("-" * 40)

        if isinstance(literature_data, dict):
            status = literature_data.get("status")

            if status == "failed":
                report.append(
                    "Literature Research Agent could not complete the search."
                )
            elif status == "skipped":
                report.append("Literature Research Agent was skipped.")
            else:
                documents = literature_data.get("documents", [])

                if documents:
                    for document in documents:
                        report.append(
                            f"\nDocument: {document.get('doc_id', 'N/A')}"
                        )
                        report.append(
                            f"Title: {document.get('title', 'N/A')}"
                        )
                        report.append(
                            f"Trial ID: {document.get('trial_id', 'N/A')}"
                        )
                        report.append(
                            f"Evidence: {document.get('text', 'N/A')}"
                        )
                else:
                    report.append("No relevant documents were found.")
        else:
            report.append(str(literature_data))

    # 3. ADVERSE EVENT ANALYSIS
    if adverse_event_data:
        report.append("\n\n3. ADVERSE EVENT ANALYSIS")
        report.append("-" * 40)

        if isinstance(adverse_event_data, dict):
            status = adverse_event_data.get("status")

            if status == "failed":
                report.append(
                    "Adverse Event Agent could not complete the analysis."
                )
            elif status == "skipped":
                report.append(
                    "Adverse Event Agent was skipped because "
                    "no trial ID was available."
                )
            else:
                report.append(
                    f"Trial ID: {adverse_event_data.get('trial_id', 'N/A')}"
                )
                report.append(
                    f"Total Events: {adverse_event_data.get('total_events', 0)}"
                )
                report.append(
                    f"Serious Events: {adverse_event_data.get('serious_events', 0)}"
                )
                report.append(
                    f"Severe Events: {adverse_event_data.get('severe_events', 0)}"
                )
        else:
            report.append(str(adverse_event_data))

    
    
    # 4. COMPOUND SIMILARITY
    if compound_similarity_data:
        report.append("\n\n4. COMPOUND SIMILARITY")
        report.append("-" * 40)

        if isinstance(compound_similarity_data, dict):
            status = compound_similarity_data.get("status")

            if status == "failed":
                report.append(
                    "Compound Similarity Agent could not complete the analysis."
                )
            elif status == "skipped":
                report.append(
                    "Compound Similarity Agent was skipped because "
                    "no compound ID was detected."
                )
            else:
                similar_compounds = compound_similarity_data.get(
                    "similar_compounds", []
                )

                if similar_compounds:
                    for compound in similar_compounds:
                        report.append(
                            f"\nCompound ID: "
                            f"{compound.get('compound_id', 'N/A')}"
                        )
                        report.append(
                            f"Compound Name: "
                            f"{compound.get('compound_name', 'N/A')}"
                        )
                        report.append(
                            f"Matching Attributes: "
                            f"{compound.get('matching_attributes', 'N/A')}"
                        )
                        report.append(
                            f"Similarity Score: "
                            f"{compound.get('similarity_score', 'N/A')}%"
                        )

                    report.append(
                        "\nNote: Scores represent exact metadata matches "
                        "across three attributes, not chemical similarity."
                    )
                else:
                    report.append("No similar compounds were found.")
        else:
            report.append(str(compound_similarity_data))

    # 5. EVIDENCE CONSISTENCY CHECK
    if evidence_fusion_data:
        report.append("\n\n5. EVIDENCE CONSISTENCY CHECK")
        report.append("-" * 40)

        if isinstance(evidence_fusion_data, dict):
            conflicts = evidence_fusion_data.get("conflicts", [])

            if conflicts:
                report.append(
                    "Potential discrepancies were detected "
                    "between structured data and research documents."
                )

                for conflict in conflicts:
                    report.append("\n⚠ POTENTIAL EVIDENCE DISCREPANCY")
                    report.append(
                        f"Document: {conflict.get('document_id', 'N/A')}"
                    )
                    report.append(
                        f"Title: {conflict.get('document_title', 'N/A')}"
                    )
                    report.append(
                        f"Trial ID: {conflict.get('trial_id', 'N/A')}"
                    )
                    report.append(
                        f"Database enrollment: "
                        f"{conflict.get('database_value', 'N/A')}%"
                    )
                    report.append(
                        f"Document enrollment: "
                        f"{conflict.get('document_value', 'N/A')}%"
                    )
                    report.append(
                        f"Difference: "
                        f"{conflict.get('difference', 'N/A')} "
                        "percentage points"
                    )
                    report.append("Action: Flag for human review.")
            else:
                report.append(
                    "No discrepancies were detected in the "
                    "available evidence checked."
                )
        else:
            report.append(str(evidence_fusion_data))
    else:
        report.append("\n\n5. EVIDENCE CONSISTENCY CHECK")
        report.append("-" * 40)
        report.append(
            "Evidence fusion was not run or no results were provided. "
            "Consistency has not been assessed."
        )

    # 6. SUMMARY
    report.append("\n\n6. SUMMARY")
    report.append("-" * 40)
    report.append(
        "The report combines structured trial data, "
        "research documents, adverse event information, "
        "compound similarity results, and evidence "
        "consistency findings when available."
    )
    report.append(
        "Potential evidence discrepancies should be reviewed "
        "by a human before decisions are made."
    )

    return "\n".join(report)


if __name__ == "__main__":
    print("\nPharmaSense AI - Report Writer Agent")
    print("=" * 60)

    test_report = report_writer_agent(
        question="Give me a report for CMP-0055.",
        trial_data={
            "status": "failed",
            "error": "Temporary service unavailable"
        },
        literature_data={
            "documents": []
        },
        adverse_event_data={
            "trial_id": "TRL-0037",
            "total_events": 3,
            "serious_events": 0,
            "severe_events": 0
        },
        compound_similarity_data={
            "similar_compounds": []
        },
        evidence_fusion_data={
            "conflicts": [
                {
                    "document_id": "DOC-00050",
                    "document_title": "Internal Memo",
                    "trial_id": "TRL-0037",
                    "database_value": 40.46,
                    "document_value": 57.0,
                    "difference": 16.54
                }
            ]
        }
    )

    print("\n")
    print(test_report)