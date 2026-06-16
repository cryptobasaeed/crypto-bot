import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔐 توکن از Environment Variable گرفته میشه
TOKEN = os.getenv("BOT_TOKEN")


# 📊 گرفتن قیمت از Binance
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        return float(requests.get(url, timeout=5).json()["price"])
    except:
        return None


# 🤖 دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن شد 🚀")


# 🔁 لوپ قیمت
async def price_loop():
    print("PRICE LOOP STARTED")

    while True:
        btc = get_price("BTCUSDT")

        if btc:
            print("BTC:", btc)

        await asyncio.sleep(10)


# 🚀 این تابع بعد از بالا آمدن ربات اجرا میشه
async def run(app):
    asyncio.create_task(price_loop())


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    # 🔥 اتصال صحیح loop
    app.post_init = run

    app.run_polling()


if __name__ == "__main__":
    main()
