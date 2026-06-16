import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

print("Bot Started...")

# =========================
# LOAD REAL COINS MAP (FIXED)
# =========================

COINS = {}

def load():
    r = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets",
        params={
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1
        },
        timeout=20
    ).json()

    for c in r:
        COINS[c["symbol"].lower()] = c["id"]

load()

# =========================
# PERSIAN FIX
# =========================

PERSIAN = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "btc": "bitcoin",

    "اتریوم": "ethereum",
    "eth": "ethereum",

    "سولانا": "solana",
    "sol": "solana",

    "دوج": "dogecoin",
    "doge": "dogecoin",

    "ریپل": "ripple",
    "xrp": "ripple",
}

SPECIAL = {
    "not": "notcoin",
    "hamster": "hamster-kombat",
    "dogs": "dogs-coin",
    "xempire": "x-empire",
}

def resolve(t):
    t = t.lower().strip()

    if t in PERSIAN:
        return PERSIAN[t]

    if t in SPECIAL:
        return SPECIAL[t]

    return COINS.get(t)

# =========================
# PRICE
# =========================

def price(t):
    cid = resolve(t)
    if not cid:
        return None

    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={"ids": cid, "vs_currencies": "usd"},
        timeout=10
    ).json()

    return r.get(cid, {}).get("usd")

# =========================
# HANDLER
# =========================

@bot.message_handler(func=lambda m: True)
def h(m):

    text = m.text.lower().strip()

    p = price(text)

    if p:
        bot.send_message(m.chat.id, f"💰 {text}: ${p}")
    else:
        bot.send_message(m.chat.id, "❌ پیدا نشد")

print("RUNNING")
bot.infinity_polling()
