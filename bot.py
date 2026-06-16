import os
import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# -----------------------
# Binance Price Fetch
# -----------------------
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return None


# -----------------------
# Start Command
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ربات حرفه‌ای فعال شد 🚀")


# -----------------------
# Price Monitor Loop
# -----------------------
async def price_monitor(app):
    btc_last = None

    while True:
        btc = get_price("BTCUSDT")

        if btc:
            print("BTC:", btc)

            # مثال ساده آلارم
            if btc_last:
                if abs(btc - btc_last) >= 1000:
                    await app.bot.send_message(
                        chat_id="@your_channel_or_user_id",
                        text=f"BTC تغییر شدید: {btc}$ 🚨"
                    )

            btc_last = btc

        await asyncio.sleep(10)


# -----------------------
# Main
# -----------------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")

    # background task
    app.job_queue.run_once(lambda ctx: asyncio.create_task(price_monitor(app)), 1)

    app.run_polling()


if __name__ == "__main__":
    main()
