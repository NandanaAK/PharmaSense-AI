
from agents.compound_similarity_tool import find_similar_compounds


def compound_similarity_agent(compound_id, top_n=5):
    """
    Compound Similarity Agent

    Finds compounds with matching metadata attributes
    and returns their similarity scores and match reasons.
    """

    results = find_similar_compounds(
        compound_id,
        top_n=top_n
    )

    if results.empty:
        return {
            "compound_id": compound_id,
            "similar_compounds": []
        }

    similar_compounds = results[
        [
            "compound_id",
            "compound_name",
            "chemical_class",
            "therapeutic_area",
            "target_protein",
            "matching_attributes",
            "similarity_score"
        ]
    ].to_dict(orient="records")

    return {
        "compound_id": compound_id,
        "similar_compounds": similar_compounds
    }


if __name__ == "__main__":

    result = compound_similarity_agent(
        "CMP-0055",
        top_n=5
    )

    print("\nPharmaSense AI - Compound Similarity Agent")
    print("=" * 70)

    print(f"\nReference Compound: {result['compound_id']}")
    print("\nSimilar Compounds:")

    for compound in result["similar_compounds"]:
        print(
            f"\nCompound ID: {compound['compound_id']}\n"
            f"Name: {compound['compound_name']}\n"
            f"Class: {compound['chemical_class']}\n"
            f"Area: {compound['therapeutic_area']}\n"
            f"Target: {compound['target_protein']}\n"
            f"Matching Attributes: {compound['matching_attributes']}\n"
            f"Similarity Score: {compound['similarity_score']}%"
        )