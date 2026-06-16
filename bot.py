import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Bot Starting...")

# =========================
# SPECIAL COINS
# =========================

SPECIAL = {
    "not": "notcoin",
    "notcoin": "notcoin",
    "نات": "notcoin",

    "dogs": "dogs-coin",
    "داگز": "dogs-coin",

    "hamster": "hamster-kombat",
    "همستر": "hamster-kombat",

    "xempire": "x-empire",
    "ایکس": "x-empire",
}

PERSIAN = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "اتریوم": "ethereum",
    "سولانا": "solana",
    "ریپل": "ripple",
    "دوج": "dogecoin",
    "شیبا": "shiba-inu",
}

# =========================
# TOP COINS (SAFE VERSION)
# =========================

TOP = {}

def load_coins():
    try:
        print("Loading coins...")
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 300,
                "page": 1
            },
            timeout=30
        )

        data = r.json()

        if not isinstance(data, list):
            print("CoinGecko error:", data)
            return

        for c in data:
            TOP[c["symbol"].lower()] = c["id"]
            TOP[c["name"].lower()] = c["id"]

        print("Coins loaded:", len(TOP))

    except Exception as e:
        print("Load error:", e)

load_coins()

# =========================
# CRYPTO PRICE (DEBUG VERSION)
# =========================

def get_crypto(text):
    key = text.lower().strip()

    print("Searching:", key)

    coin_id = None

    if key in SPECIAL:
        coin_id = SPECIAL[key]
    elif key in PERSIAN:
        coin_id = PERSIAN[key]
    else:
        coin_id = TOP.get(key)

    print("Coin ID:", coin_id)

    if not coin_id:
        return None

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()

        print("API response:", data)

        return data.get(coin_id, {}).get("usd")

    except Exception as e:
        print("Price error:", e)
        return None

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

    print("Message:", text)

    # GOLD
    if text in ["gold", "xau", "طلا"]:
        p = get_gold()
        bot.send_message(m.chat.id, f"🥇 Gold: ${p}" if p else "❌ Gold error")
        return

    # FOREX
    if len(text) == 6 and text.isalpha():
        base = text[:3].upper()
        quote = text[3:].upper()

        p = get_forex(base, quote)
        if p:
            bot.send_message(m.chat.id, f"📊 {base}/{quote}: {p}")
        return

    # CRYPTO
    price = get_crypto(text)

    if price is not None:
        bot.send_message(m.chat.id, f"💰 {text.upper()}: ${price}")
    else:
        bot.send_message(m.chat.id, "❌ پیدا نشد (کنسول رو چک کن)")

print("Bot Started...")
bot.infinity_polling()
