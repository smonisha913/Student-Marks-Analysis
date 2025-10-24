# filepath: student-analysis/src/Student_Analysis.py
import os
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', str(name)).strip()

def main():
    parser = argparse.ArgumentParser(description="Student Analysis")
    parser.add_argument("--file", "-f", default="data/students.xlsx", help="Input Excel file")
    parser.add_argument("--outdir", "-o", default="output", help="Output directory for charts and summary")
    args = parser.parse_args()

    file_path = args.file
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"File not found: {file_path} (cwd: {os.getcwd()})")
        raise
    except Exception as e:
        print("Error reading Excel:", repr(e))
        raise

    if 'Name' not in df.columns:
        raise KeyError(f"'Name' column not found. Available columns: {df.columns.tolist()}")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns found for score averaging.")

    df['Average'] = df[numeric_cols].mean(axis=1)
    subject_averages = df[numeric_cols].mean()

    for _, row in df.iterrows():
        student_name = row['Name']
        safe_name = sanitize_filename(student_name)
        subjects = numeric_cols
        scores = row[subjects].values

        plt.figure(figsize=(8, 5))
        plt.bar(subjects, scores, color='skyblue')
        plt.title(f"{student_name}'s Marks")
        plt.xlabel('Subjects')
        plt.ylabel('Marks')
        plt.ylim(0, 100)
        plt.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        save_path = os.path.join(outdir, f"{safe_name}_marks_bar_chart.png")
        plt.savefig(save_path, dpi=150)
        plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(subject_averages.index, subject_averages.values, marker='o', color='green')
    plt.title("Subject-wise Average Marks")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    trend_path = os.path.join(outdir, "subject_average_trend_line_chart.png")
    plt.savefig(trend_path, dpi=150)
    plt.close()

    summary_path = os.path.join(outdir, "student_summary.xlsx")
    df[['Name', 'Average']].to_excel(summary_path, index=False)

    print(f"Charts and summary saved to: {os.path.abspath(outdir)}")
    print(df[['Name', 'Average']])

if __name__ == "__main__":
    main()