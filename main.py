# main.py
import feedparser, time, os, requests
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)
scheduler = BlockingScheduler()

# Define tus feeds de seguimiento
FEEDS = {
    "Rigetti": "https://www.globenewswire.com/RssFeed/organization/33039/",
    "D-Wave": "https://www.globenewswire.com/RssFeed/organization/33085/"
}

# Registro de URLs ya notificadas para evitar duplicados
seen_urls = set()

def fetch_and_notify():
    for company, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if entry.link not in seen_urls:
                seen_urls.add(entry.link)
                message = f"\u2728 *Nuevo anuncio de {company}*\n[{entry.title}]({entry.link})"
                bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

scheduler.add_job(fetch_and_notify, 'interval', minutes=10)

if __name__ == '__main__':
    print("Bot iniciado...")
    fetch_and_notify()
    scheduler.start()


