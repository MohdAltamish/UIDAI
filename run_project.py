import os
import subprocess
import sys

scripts = [
    "01_agewise_trend_dashboard.py",
    "02_child_priority_zones.py",
    "03_student_hotspots.py",
    "04_adult_demand_zones.py",
    "05_heatmap_state_vs_agegroup.py",
    "06_heatmap_state_vs_date_total.py",
    "07_child_ratio_priority_zones.py",
    "08_student_ratio_vs_state.py",
    "09_adult_ratio_vs_state.py",
    "analysis.py",
    "state_wise_piechart.py"
]

def main():
    while True:
        print("\nUIDAI Hackathon Project Runner")
        print("==============================")
        for i, script in enumerate(scripts):
            print(f"{i+1}. {script}")
        
        choice = input("\nEnter the number of the script to run (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(scripts):
                script_path = os.path.join("Python Scripts", scripts[idx])
                print(f"\nRunning {script_path}...")
                subprocess.run([sys.executable, script_path])
                print(f"\nFinished running {script_path}")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    main()
