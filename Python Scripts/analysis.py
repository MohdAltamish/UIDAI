import pandas as pd

# PART-1: Data Loading
# ================================

files=["Datasets/api_data_aadhar_enrolment_0_500000.csv",
"Datasets/api_data_aadhar_enrolment_500000_1000000.csv",
"Datasets/api_data_aadhar_enrolment_1000000_1006029.csv"]

# STEP-1.1 — Load & Concatenate
# --------------------------------  

df=pd.concat([pd.read_csv(f)
for f in files], ignore_index=True)
print("Total Records:", len(df))
print("Unique Raw States:", df['state'].nunique())
print(df["state"].unique())

# PART-2: State Name Cleaning
# ================================

# STEP-2.1 — Lowercase + Trim
# --------------------------------
df["state_clean"] = df["state"].str.lower().str.strip()

print("\nSTEP-2.1 Output (Lowercase + Trim):")
print(df["state_clean"].unique())

# --------------------------------
# STEP-2.2 — Sorted State List
# (Problem Identification)
# --------------------------------
print("\nSTEP-2.2 Output (Sorted State List):")
print(sorted(df["state_clean"].unique()))

# --------------------------------
# STEP-2.3 — Fix Mapping Dictionary
# --------------------------------
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

# --------------------------------
# STEP-2.4 — Final Clean Output
# --------------------------------
print("\nSTEP-2.4 Final Clean Result:")
print("Final Clean States & UTs:", df["state_clean"].nunique())
print(sorted(df["state_clean"].unique()))


# ======================================================
# PART-3 : STATE-WISE INTELLIGENCE & RANKING
# ======================================================

# ------------------------------------------------------
# STEP 3.1 — Total Enrolment Column Banana
# (3 age groups ko jod kar real Aadhaar count banana)
# ------------------------------------------------------
df["total_enrolment"] = (
    df["age_0_5"] +
    df["age_5_17"] +
    df["age_18_greater"]
)

# ------------------------------------------------------
# STEP 3.2 — State-wise Total Aadhaar Enrolment
# (Bivariate Analysis: State vs Enrolment Count)
# ------------------------------------------------------
state_summary = (
    df.groupby("state_clean")["total_enrolment"]
      .sum()
      .reset_index()
      .sort_values(by="total_enrolment", ascending=False)
)

print(state_summary)

# ------------------------------------------------------
# STEP 3.3 — Top 10 & Bottom 10 States (Raw View)
# ------------------------------------------------------
print("\nTop 10 States by Aadhaar Enrolment:")
print(state_summary.head(10))

print("\nBottom 10 States by Aadhaar Enrolment:")
print(state_summary.tail(10))

# ------------------------------------------------------
# STEP 3.4 — Overall Human-Readable Ranking
# (Index 0 se nahi, Rank 1 se start hoga)
# ------------------------------------------------------
state_summary = state_summary.reset_index(drop=True)
state_summary["Overall_Rank"] = range(1, len(state_summary) + 1)

# ------------------------------------------------------
# STEP 3.5 — Top-10 States (Clean Ranking 1–10)
# ------------------------------------------------------
top10 = state_summary.head(10).copy()
top10 = top10.reset_index(drop=True)
top10["Top10_Rank"] = range(1, len(top10) + 1)

print("\n🏆 Top-10 States (Clean Ranking 1–10):")
print(
    top10[["Top10_Rank", "state_clean", "total_enrolment"]]
    .to_string(index=False)
)

# ------------------------------------------------------
# STEP 3.6 — Bottom-10 States (Clean Ranking 1–10)
# ------------------------------------------------------
bottom10 = state_summary.tail(10).copy()
bottom10 = bottom10.reset_index(drop=True)
bottom10["Bottom10_Rank"] = range(1, len(bottom10) + 1)

print("\n🔻 Bottom-10 States (Clean Ranking 1–10):")
print(
    bottom10[["Bottom10_Rank", "state_clean", "total_enrolment"]]
    .to_string(index=False)
)


# 🔹 STEP-4.1 — Top-10 States

import matplotlib.pyplot as plt
colors = ["#2c249f", "#000407", "#7bdf72"]

plt.figure(figsize=(10,5))
bars = plt.bar(
    top10["state_clean"],
    top10["total_enrolment"],
    color=colors * 4   # repeat colors automatically
)

plt.xticks(rotation=45, ha="right")
plt.title("Top 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, h, f"{int(h):,}",
            ha="center", va="bottom", fontsize=9)

plt.tight_layout()

### 🔹 STEP-4.2 — Bottom-10 States

plt.figure(figsize=(10,5))
bars = plt.bar(
    bottom10["state_clean"],
    bottom10["total_enrolment"],
    color=colors * 4
)

plt.xticks(rotation=45, ha="right")
plt.title("Bottom 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, h, f"{int(h):,}",
    ha="center", va="bottom", fontsize=9)

plt.tight_layout()


#Step 4.3
# ===== REQUIRED: create daily_pulse BEFORE plotting =====

df["date"] = pd.to_datetime(
    df["date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

df = df[df["date"].notna()]

daily_pulse = (
    df.groupby("date")["total_enrolment"]
    .sum()
    .reset_index()
)

# 🔹 STEP-4.4 — Pie Chart
# ===== NOW PLOT =====
plt.figure(figsize=(12,5))
plt.plot(
    daily_pulse["date"],
    daily_pulse["total_enrolment"],
    color=colors[1],   # pick any one
    marker="o",
    linewidth=2
)

plt.title("Aadhaar Enrolment Pulse Over Time")
plt.xlabel("Date")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()

# ------------------------------------------------------
# END OF analysis.py    