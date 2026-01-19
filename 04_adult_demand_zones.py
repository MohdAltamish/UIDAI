import pandas as pd
import matplotlib.pyplot as plt

# ================================
# PART-1: Load & Combine Data
# ================================
files = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
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
# PART-3: Total + Adult Ratio
# ================================
df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
df = df[df["total_enrolment"] > 0]

df["adult_ratio"] = df["age_18_greater"] / df["total_enrolment"]

# ================================
# PART-4: District-wise Adult Demand
# ================================
district_adult = (
    df.groupby(["state_clean", "district"])
    .agg(
        total_adults=("age_18_greater", "sum"),
        total_all=("total_enrolment", "sum")
    )
    .reset_index()
)

district_adult["adult_ratio"] = district_adult["total_adults"] / district_adult["total_all"]

# Top 15 adult demand districts
top15_adults = district_adult.sort_values("total_adults", ascending=False).head(15)
top15_adults.to_csv("output_adult_demand_top15.csv", index=False)

# ================================
# PART-5: Plot Adult Demand Zones
# ================================
plt.figure(figsize=(12, 6))
plt.barh(
    top15_adults["district"] + " (" + top15_adults["state_clean"] + ")",
    top15_adults["total_adults"]
)

plt.title("Top Adult Aadhaar Demand Zones (Age 18+)")
plt.xlabel("Total Age 18+ Enrolments")
plt.ylabel("District (State)")
plt.tight_layout()
plt.savefig("plot_adult_demand_zones.png", dpi=300)
plt.show()

print("✅ File 04 done: Adult Demand Zones created.")