"""
Student Academic Performance Prediction — Flask API
Loads student_model.pkl with the EXACT same structure saved in Colab Cell 50:
  {model, scaler, encoders, features, cat_cols, model_name, accuracy, auc}
"""
import pickle, os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

PKL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'student_model.pkl')
with open(PKL_PATH, 'rb') as f:
    pkg = pickle.load(f)

model      = pkg['model']
scaler     = pkg['scaler']
encoders   = pkg['encoders']
features   = pkg['features']
cat_cols   = pkg['cat_cols']
model_name = pkg['model_name']
acc        = pkg['accuracy']
auc        = pkg['auc']

@app.route('/')
def index():
    return render_template('index.html', accuracy=round(acc*100,2), auc=round(auc,4))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        row = {}
        for col in features:
            val = data.get(col)
            if val is None:
                return jsonify({'error': f'Missing field: {col}'}), 400
            if col in cat_cols:
                enc = encoders[col]
                if val not in enc:
                    return jsonify({'error': f'Unknown value "{val}" for {col}. Valid: {list(enc.keys())}'}), 400
                row[col] = enc[val]
            else:
                row[col] = float(val)

        X = pd.DataFrame([[row[c] for c in features]], columns=features)
        prob     = model.predict_proba(X)[0]
        pred     = int(model.predict(X)[0])
        pass_pct = round(float(prob[1]) * 100, 1)
        fail_pct = round(float(prob[0]) * 100, 1)
        risk = 'High Risk' if fail_pct >= 70 else 'Moderate Risk' if fail_pct >= 40 else 'Low Risk'

        return jsonify({
            'prediction':       'Pass' if pred == 1 else 'Fail',
            'pass_probability': pass_pct,
            'fail_probability': fail_pct,
            'risk_level':       risk,
            'key_factors':      _key_factors(row)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _key_factors(row):
    factors = []
    if row.get('G2', 20) < 10:
        factors.append({'factor': 'Low Period 2 Grade (G2)', 'impact': 'High'})
    if row.get('G1', 20) < 10:
        factors.append({'factor': 'Low Period 1 Grade (G1)', 'impact': 'High'})
    if row.get('failures', 0) >= 1:
        factors.append({'factor': 'Prior Academic Failures', 'impact': 'High'})
    if row.get('absences', 0) >= 10:
        factors.append({'factor': 'High Absences (10+)', 'impact': 'Moderate'})
    if row.get('studytime', 4) <= 1:
        factors.append({'factor': 'Low Study Time', 'impact': 'Moderate'})
    if not factors:
        factors.append({'factor': 'Strong Academic Profile', 'impact': 'Positive'})
    return factors[:3]

@app.route('/model-info')
def model_info():
    return jsonify({
        'model': model_name, 'accuracy': round(acc*100,2), 'roc_auc': round(auc,4),
        'features': len(features), 'feature_list': features,
        'encoders': {col: list(enc.keys()) for col, enc in encoders.items()}
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'model': model_name, 'features': len(features)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
