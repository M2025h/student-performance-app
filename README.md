# Student Academic Performance Prediction System
**Gradient Boosting · UCI Student Performance Dataset · 90.77% Accuracy · AUC 0.957**

---

## ⚡ IMPORTANT — If you have student_model.pkl from Colab

Your Colab notebook already saved `student_model.pkl`.  
**Just drop it into the `model/` folder — no retraining needed.**

```
student_performance_app/
└── model/
    └── student_model.pkl   ← paste your downloaded file here
```

---

## Quick Start (Local)

```bash
pip install -r requirements.txt
python app.py        # → http://localhost:5000
```

The app loads `model/student_model.pkl` — the exact same file downloaded from Colab.

---

## Project Structure

```
student_performance_app/
├── app.py                  # Flask API
├── requirements.txt        # Dependencies
├── Procfile                # For Render/Railway/Heroku
├── README.md
├── model/
│   └── student_model.pkl   # ← Your Colab pkl goes here
└── templates/
    └── index.html          # Web UI
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Web UI |
| `/predict` | POST | Predict Pass/Fail |
| `/model-info` | GET | Model metadata + encoder values |
| `/health` | GET | Health check |

### POST /predict — Example
```json
{
  "school":"GP", "sex":"F", "age":17, "address":"U",
  "famsize":"GT3", "Pstatus":"T", "Medu":3, "Fedu":2,
  "Mjob":"services", "Fjob":"services", "reason":"reputation",
  "guardian":"mother", "traveltime":1, "studytime":2,
  "failures":0, "schoolsup":"no", "famsup":"yes", "paid":"no",
  "activities":"no", "nursery":"yes", "higher":"yes",
  "internet":"yes", "romantic":"no", "famrel":4, "freetime":3,
  "goout":3, "Walc":1, "health":3, "absences":3, "G1":13, "G2":14
}
```

---

## Cloud Deployment (Free)

### Render
1. Push folder to GitHub
2. render.com → New Web Service → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`

### Railway / Heroku
```bash
heroku create your-app-name
git push heroku main
```
