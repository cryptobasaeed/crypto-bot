import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Bot Started...")

# =========================
# FIND COIN ID (REAL SEARCH)
# =========================

def find_coin_id(query):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/search",
            params={"query": query},
            timeout=10
        ).json()

        coins = r.get("coins", [])

        if not coins:
            return None

        return coins[0]["id"]

    except:
        return None

# =========================
# PRICE
# =========================

def get_price(text):
    try:
        coin_id = find_coin_id(text)

        if not coin_id:
            return None

        r = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin_id, "vs_currencies": "usd"},
            timeout=10
        ).json()

        return r.get(coin_id, {}).get("usd")

    except:
        return None

# =========================
# PERSIAN SUPPORT
# =========================

PERSIAN = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "اتریوم": "ethereum",
    "سولانا": "solana",
    "دوج": "dogecoin",
    "ریپل": "ripple",
    "شیبا": "shiba-inu",
    "نات": "notcoin",
    "داگز": "dogs",
    "همستر": "hamster-kombat",
    "ایکس امپایر": "x-empire",
}

def normalize(text):
    text = text.lower().strip()
    return PERSIAN.get(text, text)

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
        bot.send_message(m.chat.id, f"🥇 Gold: ${p}" if p else "❌ Gold error")
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
    query = normalize(text)
    price = get_price(query)

    if price:
        bot.send_message(m.chat.id, f"💰 {text}: ${price}")
    else:
        bot.send_message(m.chat.id, "❌ پیدا نشد")

print("Bot running...")
bot.infinity_polling()
