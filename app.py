from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Data setup
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
os.makedirs(DATA_DIR, exist_ok=True)
FILE_PATH = os.path.join(DATA_DIR, 'students.xlsx')

DEFAULT_SUBJECTS = ['Math', 'Science', 'English']

@app.route('/', methods=['GET'])
def index():
    # load subjects dynamically if file exists
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_excel(FILE_PATH)
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            subjects = numeric_cols if numeric_cols else DEFAULT_SUBJECTS
        except Exception:
            subjects = DEFAULT_SUBJECTS
    else:
        subjects = DEFAULT_SUBJECTS
    return render_template('base.html', subjects=subjects)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name', '').strip()
    if not name:
        return "Error: name is required.", 400

    subjects = request.form.getlist('subjects')
    if not subjects:
        return "Error: no subjects provided.", 400

    row = {'Name': name}
    for subj in subjects:
        raw = request.form.get(subj, '')
        val = pd.to_numeric(raw, errors='coerce')
        row[subj] = None if pd.isna(val) else float(val)

    # Read or create Excel file
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
    else:
        df = pd.DataFrame(columns=['Name'] + subjects)

    for subj in subjects:
        if subj not in df.columns:
            df[subj] = pd.NA

    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_excel(FILE_PATH, index=False)

    return redirect(url_for('report'))

@app.route('/report', methods=['GET'])
def report():
    if not os.path.exists(FILE_PATH):
        return render_template('report.html', data=[], averages={})

    df = pd.read_excel(FILE_PATH)
    if 'Name' not in df.columns:
        return render_template('report.html', data=[], averages={})

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        df['Average'] = df[numeric_cols].mean(axis=1)
        subject_averages = df[numeric_cols].mean()
    else:
        df['Average'] = 0
        subject_averages = pd.Series(dtype=float)

    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    averages = {k: float(v) for k, v in subject_averages.to_dict().items()}

    return render_template('report.html', data=records, averages=averages)

if __name__ == "__main__":
    app.run(debug=True)
