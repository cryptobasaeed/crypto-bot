import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")


def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات روشن شد 🚀")


async def price_loop(app):
    print("PRICE LOOP STARTED")

    btc_last = None

    while True:
        btc = get_price("BTCUSDT")

        if btc:
            print("BTC:", btc)

            if btc_last and abs(btc - btc_last) >= 1000:
                await app.bot.send_message(
                    chat_id=update_chat_id(app),
                    text=f"BTC تغییر شدید: {btc}$ 🚨"
                )

            btc_last = btc

        await asyncio.sleep(10)


def update_chat_id(app):
    # فعلاً ساده (بعداً multi-user می‌کنیم)
    return list(app.bot.get_updates())[-1].message.chat_id


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    async def run_loop():
        await price_loop(app)

    app.create_task(run_loop())

    app.run_polling()


if __name__ == "__main__":
    main()
