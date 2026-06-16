import telebot
import requests

TOKEN = "8103469853:AAHN9z-hcXg9ObcxHOzi3QO0vkwBhResrDc"

bot = telebot.TeleBot(TOKEN)

# -------------------------
# اسم‌ها (فارسی → کریپتو)
# -------------------------
SYMBOLS = {
    "بیتکوین": "bitcoin",
    "btc": "bitcoin",
    "اتریوم": "ethereum",
    "eth": "ethereum",
    "تتر": "tether",
    "usdt": "tether",
}

# -------------------------
# کریپتو از CoinGecko
# -------------------------
def get_crypto_price(coin):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r.get(coin, {}).get("usd")
    except:
        return None

# -------------------------
# دلار/تومان از نوبیتکس
# -------------------------
def get_usdt_irr():
    try:
        url = "https://api.nobitex.ir/market/stats"
        r = requests.get(url, timeout=10).json()
        return r["stats"]["usdt-rls"]["latest"]
    except:
        return None

# -------------------------
# فارکس (Exchangerate API)
# -------------------------
def get_forex(pair):
    try:
        base = pair[:3].upper()
        symbol = pair[3:].upper()

        url = f"https://api.exchangerate.host/latest?base={base}&symbols={symbol}"
        r = requests.get(url, timeout=10).json()

        return r["rates"][symbol]
    except:
        return None

# -------------------------
# فارکس لیست
# -------------------------
FOREX = {
    "eurusd": "EURUSD",
    "gbpusd": "GBPUSD",
    "usdjpy": "USDJPY",
    "usdtry": "USDTRY",
}

# -------------------------
# هندل پیام
# -------------------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.lower().strip()

    # ---------------- دلار / تتر ----------------
    if text in ["دلار", "usd", "تتر", "usdt"]:
        price = get_usdt_irr()
        if price:
            bot.send_message(message.chat.id, f"💵 دلار/تتر: {price} تومان")
        else:
            bot.send_message(message.chat.id, "❌ خطا در گرفتن قیمت دلار")
        return

    # ---------------- فارکس ----------------
    if text in FOREX:
        pair = FOREX[text]
        price = get_forex(pair)
        if price:
            bot.send_message(message.chat.id, f"📊 {pair}: {price}")
        else:
            bot.send_message(message.chat.id, "❌ خطا در فارکس")
        return

    # ---------------- کریپتو ----------------
    if text in SYMBOLS:
        coin = SYMBOLS[text]
        price = get_crypto_price(coin)

        if price:
            bot.send_message(message.chat.id, f"💰 {coin.upper()} : ${price}")
        else:
            bot.send_message(message.chat.id, "❌ قیمت کریپتو پیدا نشد")
        return

    # ---------------- پیام پیشفرض ----------------
    bot.send_message(
        message.chat.id,
        "📌 بنویس:\n"
        "- BTC یا بیتکوین\n"
        "- دلار یا تتر\n"
        "- EURUSD یا USDJPY"
    )

print("bot started")
bot.polling()
