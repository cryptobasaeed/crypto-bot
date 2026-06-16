import telebot
import requests

TOKEN = "توکن_ربات_تو_اینجا"

bot = telebot.TeleBot(TOKEN)

# -------------------------
# اسم‌ها (فارسی → انگلیسی کریپتو)
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
# گرفتن قیمت کریپتو (CoinGecko)
# -------------------------
def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    r = requests.get(url).json()
    return r[coin]["usd"]

# -------------------------
# دلار/تومان از نوبیتکس
# -------------------------
def get_usdt_irr():
    url = "https://api.nobitex.ir/market/stats"
    r = requests.get(url).json()
    return r["stats"]["usdt-rls"]["latest"]

# -------------------------
# فارکس (Forex)
# -------------------------
def get_forex(pair):
    url = f"https://api.exchangerate.host/latest?base={pair[:3]}&symbols={pair[3:]}"
    r = requests.get(url).json()
    return r["rates"][pair[3:]]

# -------------------------
# تشخیص فارکس
# -------------------------
FOREX_PAIRS = {
    "eurusd": "EURUSD",
    "eurgbp": "EURGBP",
    "usdtry": "USDTRY",
    "gbpusd": "GBPUSD",
    "usdjpy": "USDJPY",
}

# -------------------------
# پیام‌ها
# -------------------------
@bot.message_handler(func=lambda message: True)
def handle(message):
    text = message.text.lower().strip()

    # -------------------------
    # دلار / تتر ایران
    # -------------------------
    if text in ["دلار", "usd", "تتر", "usdt"]:
        price = get_usdt_irr()
        bot.send_message(message.chat.id, f"💵 دلار (تتر): {price} تومان")
        return

    # -------------------------
    # فارکس
    # -------------------------
    if text in FOREX_PAIRS:
        pair = FOREX_PAIRS[text]
        try:
            price = get_forex(pair)
            bot.send_message(message.chat.id, f"📊 {pair}: {price}")
        except:
            bot.send_message(message.chat.id, "❌ خطا در دریافت فارکس")
        return

    # -------------------------
    # کریپتو
    # -------------------------
    if text in SYMBOLS:
        coin = SYMBOLS[text]
        try:
            price = get_crypto_price(coin)
            bot.send_message(message.chat.id, f"💰 {coin.upper()} : ${price}")
        except:
            bot.send_message(message.chat.id, "❌ خطا در کریپتو")
        return

    # -------------------------
    # پیام پیشفرض
    # -------------------------
    bot.send_message(message.chat.id,
        "📌 بنویس:\n"
        "- BTC یا بیتکوین\n"
        "- دلار یا تتر\n"
        "- EURUSD یا USDJPY"
    )

print("bot started")
bot.polling()
