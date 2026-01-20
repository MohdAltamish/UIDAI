import pandas as pd
import matplotlib.pyplot as plt
import os

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
# PART-3: State-wise Age Aggregation
# ================================
state_age_summary = (
    df.groupby("state_clean")[["age_0_5", "age_5_17", "age_18_greater"]]
    .sum()
    .reset_index()
)

state_age_summary.to_csv(
    "Output Datasets/output_statewise_agegroup_distribution.csv",
    index=False
)

# ================================
# PART-4: Create Output Folder
# ================================
output_dir = "State Piecharts"
os.makedirs(output_dir, exist_ok=True)

# ================================
# PART-5: Generate Pie Chart for Each State
# ================================
for _, row in state_age_summary.iterrows():
    state = row["state_clean"]

    values = [
        row["age_0_5"],
        row["age_5_17"],
        row["age_18_greater"]
    ]

    if sum(values) == 0:
        continue

    labels = ["Age 0–5", "Age 5–17", "Age 18+"]

    plt.figure(figsize=(6, 6))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title(
        f"Aadhaar Enrolment Age Distribution\n{state.title()}",
        fontsize=12
    )

    plt.tight_layout()

    filename = f"{output_dir}/{state.replace(' ', '_')}_age_distribution_pie.png"
    plt.savefig(filename, dpi=300)
    plt.close()

print("✅ File 07 done: State-wise age group pie charts generated.")