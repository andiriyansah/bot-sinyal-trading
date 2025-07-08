import os
import yfinance as yf
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ambil token dari variabel environment
TOKEN = os.getenv("TOKEN")

# Hitung RSI manual
def hitung_rsi(df, periode=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periode).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periode).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Fungsi analisis RSI dan hasilkan sinyal
def get_rsi_signal(symbol="AAPL"):
    df = yf.download(symbol, period="30d", interval="1d")
    df["RSI"] = hitung_rsi(df)
    rsi = df["RSI"].iloc[-1]
    
    if rsi < 30:
        return f"📉 BUY – RSI: {rsi:.2f} (Oversold)"
    elif rsi > 70:
        return f"📈 SELL – RSI: {rsi:.2f} (Overbought)"
    else:
        return f"⏸️ WAIT – RSI: {rsi:.2f} (Normal)"

# Command Handler: /cek AAPL
async def cek(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].upper()
    else:
        symbol = "AAPL"
    result = get_rsi_signal(symbol)
    await update.message.reply_text(f"Sinyal {symbol}:\n{result}")

# Setup bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("cek", cek))
print("Bot aktif...")
app.run_polling()
