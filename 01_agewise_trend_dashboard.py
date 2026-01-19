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
# PART-3: Date + Total Enrolment
# ================================
df["date"] = pd.to_datetime(df["date"], format="mixed", dayfirst=True, errors="coerce")
df = df[df["date"].notna()]

df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]

# ================================
# PART-4: Daily Age-wise Trends
# ================================
daily_age = (
    df.groupby("date")[["age_0_5", "age_5_17", "age_18_greater", "total_enrolment"]]
      .sum()
      .reset_index()
      .sort_values("date")
)

daily_age.to_csv("output_daily_agewise_trend.csv", index=False)

# ================================
# PART-5: Line Chart (3 Age Groups)
# ================================
plt.figure(figsize=(12, 5))
plt.plot(daily_age["date"], daily_age["age_0_5"], marker="o", label="Age 0-5")
plt.plot(daily_age["date"], daily_age["age_5_17"], marker="o", label="Age 5-17")
plt.plot(daily_age["date"], daily_age["age_18_greater"], marker="o", label="Age 18+")

plt.title("Age-wise Aadhaar Enrolment Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Enrolments")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("plot_agewise_line_trend.png", dpi=300)
plt.show()

# ================================
# PART-6: Stacked Area Chart
# ================================
plt.figure(figsize=(12, 5))
plt.stackplot(
    daily_age["date"],
    daily_age["age_0_5"],
    daily_age["age_5_17"],
    daily_age["age_18_greater"],
    labels=["Age 0-5", "Age 5-17", "Age 18+"]
)

plt.title("Stacked Area Chart: Aadhaar Enrolments by Age Group")
plt.xlabel("Date")
plt.ylabel("Enrolments")
plt.xticks(rotation=45)
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("plot_agewise_stacked_area.png", dpi=300)
plt.show()

print("✅ File 01 done: Age-wise Trend Dashboard created.")