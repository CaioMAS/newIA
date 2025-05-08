import pandas as pd
import joblib
from datetime import datetime
import os

from app.database import engine
from app.services.treinamento import treinar_modelo

def simular_operacao():
    try:
        # Treina o modelo caso não exista ainda
        if not os.path.exists("modelo_trading.joblib"):
            print("⚠️ Modelo não encontrado. Treinando automaticamente...")
            treinar_modelo()

        modelo = joblib.load("modelo_trading.joblib")
        df = pd.read_csv("dados_trading.csv")

        if len(df) < 6:
            print("⚠️ Dados insuficientes para simular operação.")
            return

        entrada = df.iloc[-6].copy()
        ultima = df.iloc[-1]

        X = pd.DataFrame([entrada[["rsi", "ema20", "ema100", "macd"]]])
        pred = modelo.predict(X)[0]

        if pred == 1:
            preco_entrada = entrada.get("ema20")
            preco_saida = ultima.get("ema20")

            # Verificação robusta de preços inválidos
            if not preco_entrada or not preco_saida or preco_entrada == 0.0 or preco_saida == 0.0 or pd.isna(preco_entrada) or pd.isna(preco_saida):
                print("⚠️ Preços inválidos detectados. Operação descartada.")
                return

            preco_entrada = float(preco_entrada)
            preco_saida = float(preco_saida)
            lucro = (preco_saida / preco_entrada - 1) * 100
            resultado = "lucro" if lucro > 0 else "prejuízo" if lucro < 0 else "neutro"

            operacao = {
                "par": "BTCUSDT",
                "preco_entrada": round(preco_entrada, 4),
                "preco_saida": round(preco_saida, 4),
                "lucro_percentual": round(lucro, 2),
                "resultado": resultado,
                "data": datetime.now().isoformat()
            }

            df_operacao = pd.DataFrame([operacao])
            df_operacao.to_sql("operacoes", con=engine, if_exists="append", index=False)

            print("✅ Operação simulada e salva no banco:", operacao)
        else:
            print("🟡 IA sugeriu aguardar. Nenhuma operação realizada.")

    except Exception as e:
        print("❌ Erro ao simular operação:", e)


def consultar_operacoes(limit=10):
    try:
        query = f"SELECT * FROM operacoes ORDER BY data DESC LIMIT {limit}"
        df = pd.read_sql(query, con=engine)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"erro": str(e)}
