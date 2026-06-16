import os
import requests
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# =========================
# Special coins (meme / telegram trend)
# =========================

SPECIAL = {
    "not": "notcoin",
    "notcoin": "notcoin",
    "نات": "notcoin",

    "dogs": "dogs-coin",
    "dog": "dogs-coin",
    "داگز": "dogs-coin",

    "hamster": "hamster-kombat",
    "hmstr": "hamster-kombat",
    "همستر": "hamster-kombat",

    "xempire": "x-empire",
    "empire": "x-empire",
    "ایکس": "x-empire",
}

# =========================
# Persian names
# =========================

PERSIAN = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "اتریوم": "ethereum",
    "سولانا": "solana",
    "ریپل": "ripple",
    "دوج": "dogecoin",
    "کاردانو": "cardano",
    "ترون": "tron",
    "تون": "the-open-network",
    "شیبا": "shiba-inu",
}

# =========================
# Load TOP 300 correctly
# (ONLY by market cap, correct ids)
# =========================

print("Loading TOP 300 coins...")

TOP = {}

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

    for coin in r:
        symbol = coin["symbol"].lower()
        name = coin["name"].lower()
        cid = coin["id"]

        TOP[symbol] = cid
        TOP[name] = cid

    print("Loaded coins:", len(TOP))

except Exception as e:
    print("Error loading TOP coins:", e)

# =========================
# Crypto price
# =========================

def get_crypto(text):
    try:
        key = text.lower().strip()

        if key in SPECIAL:
            coin_id = SPECIAL[key]

        elif key in PERSIAN:
            coin_id = PERSIAN[key]

        else:
            coin_id = TOP.get(key)

        if not coin_id:
            return None

        data = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd",
            timeout=10
        ).json()

        return data.get(coin_id, {}).get("usd")

    except:
        return None

# =========================
# Forex
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
# Gold
# =========================

def get_gold():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        return r.get("price")
    except:
        return None

# =========================
# Handler
# =========================

@bot.message_handler(func=lambda m: True)
def handle(m):

    text = m.text.lower().strip()

    # GOLD
    if text in ["gold", "xau", "طلا"]:
        p = get_gold()
        bot.send_message(m.chat.id, f"🥇 Gold: ${p}" if p else "❌ طلا")
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
    p = get_crypto(text)
    if p:
        bot.send_message(m.chat.id, f"💰 {text.upper()}: ${p}")
        return

    bot.send_message(
        m.chat.id,
        "📌 مثال:\n"
        "btc / bitcoin / بیت کوین\n"
        "sol / سولانا\n"
        "not / داگز / همستر / x empire\n"
        "eurusd\n"
        "gold / طلا"
    )

print("Bot Started...")
bot.infinity_polling()
