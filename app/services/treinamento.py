import pandas as pd # type: ignore
import joblib # type: ignore
from xgboost import XGBClassifier # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.metrics import accuracy_score # type: ignore

def treinar_modelo():
    df = pd.read_csv("dados_trading.csv")
    X = df[["rsi", "ema20", "ema100", "macd"]]
    y = df["resultado"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = XGBClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    joblib.dump(model, "modelo_trading.joblib")
    return round(acc, 4)

def prever_com_modelo():
    try:
        modelo = joblib.load("modelo_trading.joblib")
        df = pd.read_csv("dados_trading.csv").tail(1)
        X = df[["rsi", "ema20", "ema100", "macd"]]
        pred = modelo.predict(X)[0]
        return "COMPRA" if pred == 1 else "AGUARDAR"
    except Exception as e:
        return f"Erro: {e}"
