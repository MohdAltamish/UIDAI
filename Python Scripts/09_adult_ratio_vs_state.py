import pandas as pd
import matplotlib.pyplot as plt

# ================================
# LOAD + CONCAT
# ================================
files = [
    "Datasets/api_data_aadhar_enrolment_0_500000.csv",
    "Datasets/api_data_aadhar_enrolment_500000_1000000.csv",
    "Datasets/api_data_aadhar_enrolment_1000000_1006029.csv"
]

df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# ================================
# STATE CLEANING
# ================================
df["state_clean"] = df["state"].astype(str).str.lower().str.strip()

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
# TOTAL
# ================================
df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
df = df[df["total_enrolment"] > 0]

# ================================
# STATE-WISE ADULT RATIO
# ================================
state_adult = (
    df.groupby("state_clean")
    .agg(total_adults=("age_18_greater", "sum"), total_all=("total_enrolment", "sum"))
    .reset_index()
)

state_adult["adult_ratio"] = state_adult["total_adults"] / state_adult["total_all"]
state_adult = state_adult.sort_values("adult_ratio", ascending=False)

state_adult.to_csv("Output Datasets/output_adult_ratio_statewise.csv", index=False)

# ================================
# VISUAL: Top 15 Adult Ratio States (Workforce Zones)
# ================================
top15 = state_adult.head(15)

plt.figure(figsize=(12, 6))
plt.barh(top15["state_clean"], top15["adult_ratio"])
plt.title("Adult Ratio vs State (Highest age_18_greater / total)")
plt.xlabel("Adult Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_adult_ratio_vs_state_top15.png", dpi=300)
plt.show()

# ================================
# VISUAL: Bottom 15 Adult Ratio States
# ================================
bottom15 = state_adult.tail(15)

plt.figure(figsize=(12, 6))
plt.barh(bottom15["state_clean"], bottom15["adult_ratio"])
plt.title("Adult Ratio vs State (Lowest age_18_greater / total)")
plt.xlabel("Adult Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_adult_ratio_vs_state_bottom15.png", dpi=300)
plt.show()

print("✅ Adult Ratio vs State generated successfully!")