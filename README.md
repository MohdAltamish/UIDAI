# UIDAI Hackathon — Aadhaar Enrolment Trends & Societal Insights 📊🇮🇳

## 📌 Problem Statement
**UIDAI Hackathon: Unlocking Societal Trends in Aadhaar Enrolment and Updates**

This project analyzes Aadhaar enrolment dataset to identify:
- meaningful patterns and trends
- demographic (age-wise) insights
- high-demand and low-demand zones
- ratio-based priority zones (child/student/adult)
- workload distribution across states/districts

The goal is to convert data into **actionable insights** for better decision-making and system improvements.

---

## 📂 Dataset Used
The dataset contains Aadhaar enrolment counts across age groups:

Columns used:
- `date`
- `state`
- `district`
- `pincode`
- `age_0_5`
- `age_5_17`
- `age_18_greater`

Age groups represent:
- **0–5 years** → Child enrolments  
- **5–17 years** → Student enrolments  
- **18+ years** → Adult/Workforce enrolments  

---

## ✅ Key Features / Analysis Done
### 🔹 1) State Name Cleaning & Standardization
Fixed spelling variants like:
- Orissa → Odisha  
- Pondicherry → Puducherry  
- West Bangal → West Bengal  
- Dadra & Nagar Haveli + Daman & Diu merged correctly  

---

### 🔹 2) State-wise Total Enrolment Intelligence
Generated:
- Total Aadhaar enrolments per state
- Top 10 states and Bottom 10 states ranking

📌 Output:
- ranking tables (CSV)
- bar charts (PNG)

---

### 🔹 3) Age-wise Aadhaar Trend Dashboard (Over Time)
Generated:
- Age group trends vs date
- Daily enrolment pulse
- Stacked area chart showing demographic contribution over time

---

### 🔹 4) Ratio / Priority Zone Analytics
State-wise ratio insights:
- **Child Ratio** = `age_0_5 / total_enrolment`
- **Student Ratio** = `age_5_17 / total_enrolment`
- **Adult Ratio** = `age_18_greater / total_enrolment`

These help identify:
✅ newborn enrolment gaps  
✅ school-driven enrolment hotspots  
✅ workforce-heavy regions  

---

### 🔹 5) Heatmaps
Generated heatmaps for:
- **State vs Age Group**
- **State vs Date (Total Enrolment intensity)**

---

## 📊 Visualizations Generated
This repo generates:
- ✅ Line charts (trends over time)
- ✅ Stacked area charts
- ✅ Bar charts (Top/Bottom rankings)
- ✅ Ratio-based bar charts (priority zones)
- ✅ Heatmaps (State vs Age / Date)

All plots are saved as `.png` files for easy hackathon submission.

---

## 🛠 Tech Stack
- Python 3
- Pandas
- Matplotlib

---

## 📁 Project Structure

UIDAI_Hackathon_Project/
│
├── api_data_aadhar_enrolment_0_500000.csv
├── api_data_aadhar_enrolment_500000_1000000.csv
├── api_data_aadhar_enrolment_1000000_1006029.csv
│
├── analysis.py
├── 01_agewise_trend_dashboard.py
├── 02_child_priority_zones.py
├── 03_student_hotspots.py
├── 04_adult_demand_zones.py
│
├── 05_heatmap_state_vs_agegroup.py
├── 06_heatmap_state_vs_date_total.py
│
├── 07_statewise_age_piecharts.py
│
├── 15_child_ratio_vs_state.py
├── 16_student_ratio_vs_state.py
├── 17_adult_ratio_vs_state.py
│
├── state_pie_charts/   (auto-generated pie charts)
├── outputs/            (generated CSV + PNG files)
└── README.md

---

## ▶️ How to Run
### ✅ Step 1: Install Dependencies
```bash
pip install pandas matplotlib


python3 analysis.py
python3 01_agewise_trend_dashboard.py
python3 05_heatmap_state_vs_agegroup.py
python3 07_statewise_age_piecharts.py
python3 15_child_ratio_vs_state.py



📦 Output Files Generated

After running scripts, you will get:
✅ .csv files containing ranked summaries
✅ .png plots for insights and dashboard visuals

Examples:
	•	output_child_ratio_statewise.csv
	•	plot_child_ratio_vs_state_top15.png
	•	plot_heatmap_state_vs_agegroup.png
	•	state_pie_charts/delhi_age_distribution_pie.png

⸻

🧠 Insights & Use Cases (Examples)
	•	States with low child ratio → need newborn enrolment awareness
	•	High student hotspots → likely school-driven Aadhaar camps
	•	High adult ratio zones → workforce migration & job onboarding demand
	•	Daily trends help forecast staffing needs & resource planning
	•	Pie charts summarize demographic focus per state clearly in one image

⸻

✨ Future Improvements
	•	Add interactive dashboard using Streamlit
	•	Add anomaly detection for spike/drop alerts
	•	Add district-level and pincode-level heatmaps
	•	Add forecasting models for future enrolment demand

⸻

👤 Author

Altamish | Ayush Raj Arun
Engineering Student | Data Analytics | UIDAI Hackathon Project
