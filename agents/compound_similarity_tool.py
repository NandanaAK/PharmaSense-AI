
import pandas as pd
import os

# Find the project folder
project_folder = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

# Compounds dataset
data_file = os.path.join(
    project_folder,
    "compounds.csv"
)


def find_similar_compounds(compound_id, top_n=5):
    """
    Compare compounds using:
    - Chemical class
    - Therapeutic area
    - Target protein

    Score is the percentage of exact matches
    across these three attributes.
    """

    df = pd.read_csv(data_file)

    # Find the reference compound
    reference_rows = df[
        df["compound_id"].astype(str).str.upper()
        == compound_id.upper()
    ]

    if reference_rows.empty:
        return pd.DataFrame()

    reference = reference_rows.iloc[0]

    # Exclude the reference compound
    candidates = df[
        df["compound_id"].astype(str).str.upper()
        != compound_id.upper()
    ].copy()

    # Attributes to compare
    attributes = [
        "chemical_class",
        "therapeutic_area",
        "target_protein"
    ]

    # Count exact matches and record reasons
    candidates["matching_attributes"] = ""

    for attribute in attributes:
        matches = (
            candidates[attribute].fillna("").astype(str).str.strip().str.lower()
            == str(reference[attribute]).strip().lower()
        )

        candidates.loc[matches, "matching_attributes"] += (
            attribute + ", "
        )

    candidates["match_count"] = (
        candidates["matching_attributes"]
        .str.count(",")
    )

    # Percentage of matching attributes
    candidates["similarity_score"] = (
        candidates["match_count"] / len(attributes) * 100
    ).round(2)

    # Remove trailing comma and space
    candidates["matching_attributes"] = (
        candidates["matching_attributes"].str.rstrip(", ")
    )

    # Sort by score, then compound ID for stable output
    candidates = candidates.sort_values(
        by=["similarity_score", "compound_id"],
        ascending=[False, True]
    )

    return candidates.head(top_n)


if __name__ == "__main__":

    compound_id = "CMP-0055"

    result = find_similar_compounds(
        compound_id,
        top_n=5
    )

    print("\nPharmaSense AI - Compound Similarity Tool")
    print("=" * 70)

    if result.empty:
        print(f"\nCompound {compound_id} was not found.")

    else:
        print(f"\nReference Compound: {compound_id}")
        print("\nSimilar Compounds:")

        print(
            result[
                [
                    "compound_id",
                    "compound_name",
                    "matching_attributes",
                    "similarity_score"
                ]
            ].to_string(index=False)
        )

        print("\nNote: Scores represent exact matches across")
        print("three metadata attributes, not chemical similarity.")