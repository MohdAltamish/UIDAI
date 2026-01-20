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
# PART-3: Total + Student Ratio
# ================================
df["total_enrolment"] = df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
df = df[df["total_enrolment"] > 0]

df["student_ratio"] = df["age_5_17"] / df["total_enrolment"]

# ================================
# PART-4: District-wise Student Hotspots
# ================================
district_student = (
    df.groupby(["state_clean", "district"])
    .agg(
        total_students=("age_5_17", "sum"),
        total_all=("total_enrolment", "sum")
    )
    .reset_index()
)

district_student["student_ratio"] = district_student["total_students"] / district_student["total_all"]

# Top 15 by total_students
top15_students = district_student.sort_values("total_students", ascending=False).head(15)
top15_students.to_csv("Output Datasets/output_student_hotspots_top15.csv", index=False)

# ================================
# PART-5: Plot Top 15 Student Hotspots
# ================================
plt.figure(figsize=(12, 6))
plt.barh(
    top15_students["district"] + " (" + top15_students["state_clean"] + ")",
    top15_students["total_students"]
)

plt.title("Top Student Aadhaar Hotspots (Age 5-17)")
plt.xlabel("Total Age 5-17 Enrolments")
plt.ylabel("District (State)")
plt.tight_layout()
plt.savefig("plot_student_hotspots.png", dpi=300)
plt.show()

print("✅ File 03 done: Student Hotspots created.")