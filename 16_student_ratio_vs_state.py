import pandas as pd
import matplotlib.pyplot as plt

# ================================
# LOAD + CONCAT
# ================================
files = [
    "api_data_aadhar_enrolment_0_500000.csv",
    "api_data_aadhar_enrolment_500000_1000000.csv",
    "api_data_aadhar_enrolment_1000000_1006029.csv"
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
# STATE-WISE STUDENT RATIO
# ================================
state_student = (
    df.groupby("state_clean")
      .agg(total_students=("age_5_17", "sum"), total_all=("total_enrolment", "sum"))
      .reset_index()
)

state_student["student_ratio"] = state_student["total_students"] / state_student["total_all"]
state_student = state_student.sort_values("student_ratio", ascending=False)

state_student.to_csv("output_student_ratio_statewise.csv", index=False)

# ================================
# VISUAL: Top 15 Student Ratio States (Hotspots)
# ================================
top15 = state_student.head(15)

plt.figure(figsize=(12, 6))
plt.barh(top15["state_clean"], top15["student_ratio"])
plt.title("Student Ratio vs State (Highest age_5_17 / total)")
plt.xlabel("Student Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_student_ratio_vs_state_top15.png", dpi=300)
plt.show()

# ================================
# VISUAL: Bottom 15 Student Ratio States
# ================================
bottom15 = state_student.tail(15)

plt.figure(figsize=(12, 6))
plt.barh(bottom15["state_clean"], bottom15["student_ratio"])
plt.title("Student Ratio vs State (Lowest age_5_17 / total)")
plt.xlabel("Student Ratio")
plt.ylabel("State")
plt.tight_layout()
plt.savefig("plot_student_ratio_vs_state_bottom15.png", dpi=300)
plt.show()

print("✅ Student Ratio vs State generated successfully!")