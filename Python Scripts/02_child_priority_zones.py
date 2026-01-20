import pandas as pd
import matplotlib.pyplot as plt

# ================================
# PART-1: Load & Combine Data
# ================================
files = [
    "Datasets/api_data_aadhar_enrolment_0_500000.csv",
    "Datasets/api_data_aadhar_enrolment_500000_1000000.csv",
    "Datasets/api_data_aadhar_enrolment_1000000_1006029.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# ================================
# PART-2: Clean State Names
# ================================
df["state_clean"] = df["state"].str.lower().str.strip()

fix_map = {
    "orissa": "odisha",
    "pondicherry": "puducherry",
    "west bangal": "west bengal",
    "westbengal": "west bengal",
    "west  bengal": "west bengal",
    "jammu & kashmir": "jammu and kashmir",
    "andaman & nicobar islands": "andaman and nicobar islands",
    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "100000": None
}

df["state_clean"] = df["state_clean"].replace(fix_map)
df = df[df["state_clean"].notna()]

# ================================
# PART-3: Total + Child Ratio
# ================================
df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
df = df[df["total_enrolment"] > 0]

# Child Ratio (0-5)
df["child_ratio"] = df["age_0_5"] / df["total_enrolment"]

# ================================
# PART-4: District-wise Child Ratio
# ================================
district_child = (
    df.groupby(["state_clean", "district"])
    .agg(
        total_child=("age_0_5", "sum"),
        total_all=("total_enrolment", "sum")
    )
    .reset_index()
)

district_child["child_ratio"] = district_child["total_child"] / district_child["total_all"]

district_child = district_child.sort_values("child_ratio", ascending=True)

district_child.to_csv("Output Datasets/output_child_priority_districts.csv", index=False)

# ================================
# PART-5: Bottom 15 Child Ratio Districts (Priority Zones)
# ================================
bottom15 = district_child.head(15)

plt.figure(figsize=(12, 6))
plt.barh(
    bottom15["district"] + " (" + bottom15["state_clean"] + ")",
    bottom15["child_ratio"]
)

plt.title("Child Enrolment Priority Zones (Lowest 0-5 Ratio Districts)")
plt.xlabel("Child Ratio (age_0_5 / total)")
plt.ylabel("District (State)")
plt.tight_layout()
plt.savefig("plot_child_priority_zones.png", dpi=300)
plt.show()

print("✅ File 02 done: Child Priority Zones created.")