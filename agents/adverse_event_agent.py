from agents.adverse_event_tool import get_adverse_events


def adverse_event_agent(trial_id):
    """
    Adverse Event Triage Agent

    Retrieves adverse events for a clinical trial
    and identifies serious or severe events.
    """

    events = get_adverse_events(trial_id=trial_id)

    if events.empty:
        return {
            "trial_id": trial_id,
            "total_events": 0,
            "serious_events": 0,
            "severe_events": 0,
            "events": []
        }

    serious_events = events[
        events["seriousness"].astype(str).str.lower() == "serious"
    ]

    severe_events = events[
        events["severity"].astype(str).str.lower() == "severe"
    ]

    return {
        "trial_id": trial_id,
        "total_events": len(events),
        "serious_events": len(serious_events),
        "severe_events": len(severe_events),
        "events": events.to_dict(orient="records")
    }


if __name__ == "__main__":

    result = adverse_event_agent("TRL-0037")

    print("\nPharmaSense AI - Adverse Event Triage Agent")
    print("=" * 60)

    print(f"Trial ID: {result['trial_id']}")
    print(f"Total adverse events: {result['total_events']}")
    print(f"Serious events: {result['serious_events']}")
    print(f"Severe events: {result['severe_events']}")

    print("\nAdverse Events:")

    for event in result["events"]:
        print(
            f"{event['event_id']} | "
            f"{event['adverse_event_term']} | "
            f"Severity: {event['severity']} | "
            f"Seriousness: {event['seriousness']}"
        )