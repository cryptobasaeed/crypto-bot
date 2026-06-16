import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Bot Started...")

# =========================
# SPECIAL COINS (MEME + TELEGRAM)
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

# =========================
# PERSIAN MAP (FIXED CORE COINS)
# =========================

PERSIAN = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "btc": "bitcoin",
    "bitcoin": "bitcoin",

    "اتریوم": "ethereum",
    "eth": "ethereum",
    "ethereum": "ethereum",

    "سولانا": "solana",
    "sol": "solana",

    "دوج": "dogecoin",
    "doge": "dogecoin",

    "ریپل": "ripple",
    "xrp": "ripple",

    "شیبا": "shiba-inu",
    "shib": "shiba-inu",

    "ترون": "tron",
    "trx": "tron",

    "تون": "the-open-network",
    "ton": "the-open-network",
}

# =========================
# TOP 300 COINS CACHE (REAL IDs)
# =========================

TOP = {}

def load_top():
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 300,
                "page": 1
            },
            timeout=30
        ).json()

        for c in r:
            TOP[c["symbol"].lower()] = c["id"]
            TOP[c["name"].lower()] = c["id"]

        print("Loaded TOP coins:", len(TOP))

    except Exception as e:
        print("TOP load error:", e)

load_top()

# =========================
# NORMALIZER
# =========================

def resolve(text):
    t = text.lower().strip()

    if t in SPECIAL:
        return SPECIAL[t]

    if t in PERSIAN:
        return PERSIAN[t]

    return TOP.get(t)

# =========================
# PRICE
# =========================

def get_price(text):
    coin_id = resolve(text)

    if not coin_id:
        return None

    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin_id, "vs_currencies": "usd"},
            timeout=10
        ).json()

        return r.get(coin_id, {}).get("usd")

    except:
        return None

# =========================
# FOREX
# =========================

def forex(base, quote):
    try:
        r = requests.get(
            f"https://api.frankfurter.app/latest?from={base}&to={quote}"
        ).json()
        return r["rates"][quote]
    except:
        return None

# =========================
# GOLD
# =========================

def gold():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU").json()
        return r.get("price")
    except:
        return None

# =========================
# HANDLER
# =========================

@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text.lower().strip()

    # GOLD
    if text in ["gold", "xau", "طلا"]:
        p = gold()
        bot.send_message(m.chat.id, f"🥇 Gold: ${p}" if p else "❌")
        return

    # FOREX
    if len(text) == 6 and text.isalpha():
        base = text[:3].upper()
        quote = text[3:].upper()
        p = forex(base, quote)
        if p:
            bot.send_message(m.chat.id, f"📊 {base}/{quote}: {p}")
        return

    # CRYPTO
    price = get_price(text)

    if price:
        bot.send_message(m.chat.id, f"💰 {text}: ${price}")
    else:
        bot.send_message(m.chat.id, "❌ پیدا نشد (نماد را درست وارد کن)")

print("Bot running...")
bot.infinity_polling()
