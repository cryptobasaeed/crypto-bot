import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Bot Started...")

# =========================
# CRYPTO (DIRECT - NO MAP = NO BUG)
# =========================

def get_crypto(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r.get(symbol, {}).get("usd")
    except:
        return None

# =========================
# SMART NORMALIZER
# =========================

def normalize(text):

    text = text.lower().strip()

    mapping = {
        # BTC
        "btc": "bitcoin",
        "bitcoin": "bitcoin",
        "بیتکوین": "bitcoin",
        "بیت کوین": "bitcoin",

        # ETH
        "eth": "ethereum",
        "ethereum": "ethereum",
        "اتریوم": "ethereum",

        # SOL
        "sol": "solana",
        "solana": "solana",
        "سولانا": "solana",

        # DOGE
        "doge": "dogecoin",
        "dogecoin": "dogecoin",
        "دوج": "dogecoin",

        # XRP
        "xrp": "ripple",
        "ریپل": "ripple",

        # MEME
        "not": "notcoin",
        "نات": "notcoin",

        "dogs": "dogs-coin",
        "داگز": "dogs-coin",

        "hamster": "hamster-kombat",
        "همستر": "hamster-kombat",

        "xempire": "x-empire",
        "ایکس": "x-empire",
    }

    return mapping.get(text, text)

# =========================
# FOREX
# =========================

def get_forex(base, quote):
    try:
        r = requests.get(
            f"https://api.frankfurter.app/latest?from={base}&to={quote}",
            timeout=10
        ).json()
        return r["rates"][quote]
    except:
        return None

# =========================
# GOLD
# =========================

def get_gold():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        return r.get("price")
    except:
        return None

# =========================
# HANDLER
# =========================

@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text.lower().strip()

    print("Input:", text)

    # GOLD
    if text in ["gold", "xau", "طلا"]:
        price = get_gold()
        bot.send_message(m.chat.id, f"🥇 Gold: ${price}" if price else "❌ Gold error")
        return

    # FOREX
    if len(text) == 6 and text.isalpha():
        base = text[:3].upper()
        quote = text[3:].upper()

        price = get_forex(base, quote)
        if price:
            bot.send_message(m.chat.id, f"📊 {base}/{quote}: {price}")
        return

    # CRYPTO
    symbol = normalize(text)
    price = get_crypto(symbol)

    if price:
        bot.send_message(m.chat.id, f"💰 {text.upper()}: ${price}")
    else:
        bot.send_message(m.chat.id, "❌ پیدا نشد (btc / eth / sol / doge / bitcoin)")

print("Bot running...")
bot.infinity_polling()
