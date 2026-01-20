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
# STATE-WISE CHILD RATIO
# ================================
state_child = (
    df.groupby("state_clean")
    .agg(total_child=("age_0_5", "sum"), total_all=("total_enrolment", "sum"))
    .reset_index()
)

state_child["child_ratio"] = state_child["total_child"] / state_child["total_all"]
state_child = state_child.sort_values("child_ratio", ascending=True)

state_child.to_csv("Output Datasets/output_child_ratio_statewise.csv", index=False)

# ================================
# VISUAL: Bottom 15 Child Ratio States
# ================================
bottom15 = state_child.head(15)

plt.figure(figsize=(12, 6))
plt.barh(bottom15["state_clean"], bottom15["child_ratio"])
plt.title("Child Ratio vs State (Lowest age_0_5 / total)")
plt.xlabel("Child Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_child_ratio_vs_state_bottom15.png", dpi=300)
plt.show()

# ================================
# VISUAL: Top 15 Child Ratio States
# ================================
top15 = state_child.tail(15)

plt.figure(figsize=(12, 6))
plt.barh(top15["state_clean"], top15["child_ratio"])
plt.title("Child Ratio vs State (Highest age_0_5 / total)")
plt.xlabel("Child Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_child_ratio_vs_state_top15.png", dpi=300)
plt.show()

print("✅ Child Ratio vs State generated successfully!")