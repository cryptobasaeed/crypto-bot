import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


def get_price(symbol):
    try:
        return float(
            requests.get(
                f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
            ).json()["price"]
        )
    except:
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن شد 🚀")


async def price_loop(app):
    print("PRICE LOOP STARTED")

    while True:
        btc = get_price("BTCUSDT")

        if btc:
            print("BTC:", btc)

        await asyncio.sleep(10)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    async def runner():
        await price_loop(app)

    # 🔥 مهم: بعد از start_polling اجرا میشه
    app.post_init = lambda app: asyncio.create_task(runner())

    app.run_polling()


if __name__ == "__main__":
    main()
