
import pandas as pd

df = pd.read_csv("compounds.csv")

ids = [
    "CMP-0055",
    "CMP-0001",
    "CMP-0003",
    "CMP-0004",
    "CMP-0007",
    "CMP-0006"
]

cols = [
    "compound_id",
    "chemical_class",
    "therapeutic_area",
    "target_protein",
    "mechanism_of_action",
    "discovery_phase",
    "molecular_weight_da",
    "solubility_mg_ml",
    "toxicity_score"
]

result = df[df["compound_id"].isin(ids)][cols]

print("\nCompound Attribute Comparison")
print("=" * 70)
print(result.to_string(index=False))