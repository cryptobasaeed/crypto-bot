import os
import requests
import telebot

# =========================
# Telegram
# =========================

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found")

bot = telebot.TeleBot(TOKEN)

# =========================
# Persian aliases
# =========================

PERSIAN_COINS = {
    "بیتکوین": "bitcoin",
    "بیت کوین": "bitcoin",
    "اتریوم": "ethereum",
    "سولانا": "solana",
    "ریپل": "ripple",
    "دوج": "dogecoin",
    "کاردانو": "cardano",
    "ترون": "tron",
    "تون": "the-open-network",
    "بایننس": "binancecoin",
    "شیبا": "shiba-inu",
    "پپه": "pepe"
}

# =========================
# Load CoinGecko list
# =========================

print("Loading CoinGecko coins...")

COIN_MAP = {}

try:
    coins = requests.get(
        "https://api.coingecko.com/api/v3/coins/list",
        timeout=30
    ).json()

    for coin in coins:
        symbol = coin["symbol"].lower()
        name = coin["name"].lower()

        COIN_MAP[symbol] = coin["id"]
        COIN_MAP[name] = coin["id"]

    print(f"Loaded {len(COIN_MAP)} symbols/names")

except Exception as e:
    print("Coin list error:", e)

# =========================
# Crypto Price
# =========================

def get_crypto_price(user_input):
    try:

        key = user_input.lower().strip()

        if key in PERSIAN_COINS:
            coin_id = PERSIAN_COINS[key]
        else:
            coin_id = COIN_MAP.get(key)

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

        data = requests.get(
            f"https://api.frankfurter.app/latest?from={base}&to={quote}",
            timeout=10
        ).json()

        return data["rates"][quote]

    except:
        return None

# =========================
# Gold
# =========================

def get_gold():
    try:

        data = requests.get(
            "https://api.gold-api.com/price/XAU",
            timeout=10
        ).json()

        return data.get("price")

    except:
        return None

# =========================
# Handler
# =========================

@bot.message_handler(func=lambda message: True)
def handle(message):

    text = message.text.strip().lower()

    # ---------------------
    # Gold
    # ---------------------

    if text in ["gold", "xau", "طلا"]:

        price = get_gold()

        if price:
            bot.send_message(
                message.chat.id,
                f"🥇 Gold (XAU/USD)\n💰 ${price}"
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ خطا در دریافت قیمت طلا"
            )

        return

    # ---------------------
    # Forex
    # ---------------------

    if len(text) == 6 and text.isalpha():

        base = text[:3].upper()
        quote = text[3:].upper()

        price = get_forex(base, quote)

        if price is not None:

            bot.send_message(
                message.chat.id,
                f"📊 {base}/{quote}\n💰 {price}"
            )

            return

    # ---------------------
    # Crypto
    # ---------------------

    crypto_price = get_crypto_price(text)

    if crypto_price is not None:

        bot.send_message(
            message.chat.id,
            f"🪙 {text.upper()}\n💰 ${crypto_price}"
        )

        return

    # ---------------------
    # Help
    # ---------------------

    bot.send_message(
        message.chat.id,
        "📌 نمونه‌ها:\n\n"
        "btc\n"
        "bitcoin\n"
        "بیت کوین\n\n"
        "eth\n"
        "ethereum\n"
        "اتریوم\n\n"
        "sol\n"
        "solana\n"
        "سولانا\n\n"
        "eurusd\n"
        "gbpusd\n"
        "usdjpy\n\n"
        "gold\n"
        "طلا"
    )

print("Bot Started...")

bot.infinity_polling(skip_pending=True)
