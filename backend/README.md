# Food Packaging Backend

Python backend replacing the previous Node/Express + separate ML-server architecture.

## Stack

- FastAPI
- scikit-learn
- pandas / NumPy
- MongoDB via PyMongo
- Random Forest regression
- joblib model persistence

## Architecture

React frontend -> FastAPI backend -> Random Forest -> recommendation logic -> MongoDB

The ML model is loaded once when the API starts.

## 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment

```bash
cp .env.example .env
```

Make sure MongoDB is running if you want database connectivity.

## 4. Train the prototype model

```bash
python training/train.py
```

This creates:

```text
trained_models/packaging_rf.joblib
```

The training data is synthetic and exists only to test the complete application pipeline.

## 5. Start the API

```bash
uvicorn app.main:app --reload --port 5000
```

API:
- http://localhost:5000
- Swagger UI: http://localhost:5000/docs
- Health: http://localhost:5000/api/health

## Existing frontend

The React frontend can keep using:

```text
VITE_API_URL=http://localhost:5000/api
```

The endpoint remains:

```text
POST /api/packaging/recommend
```

So the frontend does not need a major rewrite.

## Important prototype limitation

The model is trained from synthetic relationships created for software testing.

Its OTR/WVTR values are normalized demo requirement scores, and the thickness value is a demo estimate. They are NOT validated food-packaging engineering specifications.

Before this system is used for real packaging decisions, the synthetic dataset must be replaced with verified experimental/industrial data and the outputs must be validated by an appropriate food-packaging specialist.


## Trained model

The API loads `trained_models/packaging_rf.joblib` at startup. Train it with:

```bash
python training/train.py
```

Then run:

```bash
uvicorn app.main:app --reload --port 5000
```

Useful endpoints:
- `GET /api/packaging/model-status`
- `POST /api/packaging/predict`
- `POST /api/packaging/recommend`

The `/predict` endpoint returns the five model outputs directly. `/recommend` additionally maps them to the prototype material catalog.
