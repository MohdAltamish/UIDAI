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
# PART-3: State-wise Age Totals
# ================================
state_age = (
    df.groupby("state_clean")[["age_0_5", "age_5_17", "age_18_greater"]]
      .sum()
      .sort_values(by="age_18_greater", ascending=False)
)

state_age.to_csv("output_state_vs_agegroup_heatmap_data.csv")

# ================================
# PART-4: Heatmap Plot (imshow)
# ================================
plt.figure(figsize=(10, 12))
heatmap = plt.imshow(state_age.values, aspect="auto")

plt.colorbar(heatmap, label="Total Enrolments")

plt.xticks(
    ticks=[0, 1, 2],
    labels=["Age 0-5", "Age 5-17", "Age 18+"],
    rotation=0
)
plt.yticks(
    ticks=range(len(state_age.index)),
    labels=state_age.index
)

plt.title("Heatmap: State vs Age-Group Enrolments")
plt.xlabel("Age Group")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_heatmap_state_vs_agegroup.png", dpi=300)
plt.show()

print("✅ File 05 done: Heatmap (State vs Age Group) created.")