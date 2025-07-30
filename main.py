import feedparser, time, telegram, os, requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telegram.Bot(token=TOKEN)

# Enviar mensaje de prueba al iniciar
bot.send_message(chat_id=CHAT_ID, text="✅ Bot desplegado correctamente y funcionando en Render.")

FEEDS = {
    "Rigetti": "https://investors.rigetti.com/ir-resources/rss-feeds",
    "D-Wave": "https://www.dwavequantum.com/company/newsroom/rss",
    "SeekingAlpha": "https://seekingalpha.com/symbol/RGTI/news.xml"
}

KEYWORDS = ["milestone", "fidelity", "quantum", "scaling", "breakthrough", "SEC filing", "RGTI", "QBTS", "gate"]

last_titles = {}

def send_msg(name, title, link):
    msg = f"📡 *{name}*\n*{title}*\n{link}"
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

def check_feeds():
    for name, url in FEEDS.items():
        feed = feedparser.parse(url)
        if not feed.entries:
            continue
        entry = feed.entries[0]
        if last_titles.get(name) != entry.title:
            if any(k.lower() in entry.title.lower() for k in KEYWORDS):
                last_titles[name] = entry.title
                send_msg(name, entry.title, entry.link)

def check_price(ticker, threshold):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"
    try:
        r = requests.get(url)
        data = r.json()
        price = data['quoteResponse']['result'][0]['regularMarketPrice']
        change = data['quoteResponse']['result'][0]['regularMarketChangePercent']
        if abs(change) >= threshold:
            msg = f"📈 {ticker} movió {change:.2f}% hoy. Precio actual: ${price:.2f}"
            bot.send_message(chat_id=CHAT_ID, text=msg)
    except:
        pass

if __name__ == "__main__":
    while True:
        check_feeds()
        check_price("RGTI", 5)
        check_price("QBTS", 5)
        time.sleep(600)
