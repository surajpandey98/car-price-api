from pathlib import Path
import pandas as pd
import joblib

CAR_PRICE_API_DIR = Path(__file__).resolve().parent

MODEL_PATH = CAR_PRICE_API_DIR / "random_forest_model.pkl"
COLS_PATH = CAR_PRICE_API_DIR / "feature_columns.pkl"

_model = None
_feature_columns = None


def load_artifacts():
    global _model, _feature_columns

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    if _feature_columns is None:
        _feature_columns = joblib.load(COLS_PATH)


def preprocess(payload: dict) -> pd.DataFrame:
    """
    Convert input into the same encoded feature structure used in training.
    """
    df = pd.DataFrame([payload])

    categorical_cols = [
        "Fuel_Type",
        "Seller_Type",
        "TransmissionType",
        "Owner",
        "Car_Name"
    ]

    df_encoded = pd.get_dummies(
        df,
        columns=categorical_cols,
        drop_first=True
    )

    # Add missing columns, remove unexpected columns,
    # and arrange columns in the correct order.
    df_encoded = df_encoded.reindex(
        columns=_feature_columns,
        fill_value=0
    )

    return df_encoded

def predict_price(payload: dict) -> float:
    load_artifacts()

    X = preprocess(payload)
    pred = _model.predict(X)[0]

    return float(pred)