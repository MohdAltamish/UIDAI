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
# PART-3: Date Cleaning + Total
# ================================
df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=True, errors="coerce")
df = df[df["date"].notna()]

df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]

# ================================
# PART-4: Pivot Table (State x Date)
# ================================
pivot = pd.pivot_table(
    df,
    index="state_clean",
    columns="date",
    values="total_enrolment",
    aggfunc="sum",
    fill_value=0
)

pivot = pivot.sort_index()
pivot.to_csv("output_heatmap_state_vs_date.csv")

# ================================
# PART-5: Heatmap Plot
# ================================
plt.figure(figsize=(14, 10))
heatmap = plt.imshow(pivot.values, aspect="auto")

plt.colorbar(heatmap, label="Total Enrolments")

plt.title("Heatmap: Total Aadhaar Enrolment (State vs Date)")
plt.xlabel("Date")
plt.ylabel("State")

# Show fewer date labels to avoid clutter
date_labels = [d.strftime("%d-%m-%Y") for d in pivot.columns]
step = max(1, len(date_labels) // 10)

plt.xticks(
    ticks=range(0, len(date_labels), step),
    labels=[date_labels[i] for i in range(0, len(date_labels), step)],
    rotation=45,
    ha="right"
)

plt.yticks(
    ticks=range(len(pivot.index)),
    labels=pivot.index
)

plt.tight_layout()
plt.savefig("plot_heatmap_state_vs_date_total.png", dpi=300)
plt.show()

print("✅ File 06 done: Heatmap (State vs Date) created.")