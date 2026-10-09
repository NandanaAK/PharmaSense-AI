import pandas as pd
import os


# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


# Adverse events dataset
data_file = os.path.join(
    project_folder,
    "adverse_events.csv"
)


def get_adverse_events(
    trial_id=None,
    severity=None,
    seriousness=None
):
    """
    Retrieve adverse events using optional filters.
    """

    df = pd.read_csv(data_file)

    # Filter by trial
    if trial_id:
        df = df[
            df["trial_id"].astype(str).str.upper()
            == trial_id.upper()
        ]

    # Filter by severity
    if severity:
        df = df[
            df["severity"].astype(str).str.lower()
            == severity.lower()
        ]

    # Filter by seriousness
    if seriousness:
        df = df[
            df["seriousness"].astype(str).str.lower()
            == seriousness.lower()
        ]

    return df


if __name__ == "__main__":

    print("\nPharmaSense AI - Adverse Event Tool")
    print("=" * 60)

    result = get_adverse_events(
        trial_id="TRL-0056"
    )

    print(
        f"\nFound {len(result)} adverse events."
    )

    print("\nResults:")
    print(result.to_string(index=False))