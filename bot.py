import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        return float(requests.get(url).json()["price"])
    except:
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن شد 🚀")


# 🔥 این تابع هر 10 ثانیه اجرا میشه
async def price_job(context: ContextTypes.DEFAULT_TYPE):
    btc = get_price("BTCUSDT")

    if btc:
        print("BTC:", btc)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 🔥 درست‌ترین روش در این لایبرری
    app.job_queue.run_repeating(price_job, interval=10, first=5)

    print("Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
