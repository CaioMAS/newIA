import pandas as pd # type: ignore
from ta.momentum import RSIIndicator # type: ignore
from ta.trend import EMAIndicator, MACD # type: ignore
from binance.client import Client # type: ignore
import asyncio
from app.services.simulador import simular_operacao  # Importa a IA de simulação

# Criptos monitoradas
symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "PEPEUSDT"]
interval = Client.KLINE_INTERVAL_15MINUTE
limit = 200

# Cliente da Binance
client = Client()

# Função para processar candles e gerar indicadores + target
def get_data(symbol):
    candles = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(candles, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])

    df["close"] = pd.to_numeric(df["close"])
    df["rsi"] = RSIIndicator(df["close"]).rsi()
    df["ema20"] = EMAIndicator(df["close"], window=20).ema_indicator()
    df["ema100"] = EMAIndicator(df["close"], window=100).ema_indicator()
    df["macd"] = MACD(df["close"]).macd_diff()
    df["future_return"] = df["close"].shift(-5) / df["close"] - 1
    df["resultado"] = (df["future_return"] > 0.01).astype(int)
    df = df.dropna()
    return df[["rsi", "ema20", "ema100", "macd", "resultado"]]

# Função principal de coleta contínua
async def iniciar_coleta():
    while True:
        print("🔄 Coletando dados...")
        frames = []

        for symbol in symbols:
            try:
                df = get_data(symbol)
                frames.append(df)
            except Exception as e:
                print(f"Erro ao coletar {symbol}: {e}")

        df_final = pd.concat(frames, ignore_index=True)
        df_final.to_csv("dados_trading.csv", index=False)
        print("✅ Dados salvos com sucesso.")

        # 🔁 Simula operação com base na IA treinada
        simular_operacao()

        # Aguarda 1 hora para a próxima coleta
        await asyncio.sleep(60)
