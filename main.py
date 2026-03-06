import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== SOZLAMALAR ==================
# Koyeb "Environment Variables" bo'limidan olinadi
API_ID = 25573417 
API_HASH = "b56082f4d86578c5a6948c7b964008f9"
SESSION_STRING = os.getenv("SESSION_STRING") 

SOURCE_CHANNELS = [
    "@uzdavgeolcom", "@shmirziyoyev", "@senatuz", 
    "@adliyangiliklari", "@huquqiyaxborot", "@xavfsizlik_uz", "@antikor_uzb", 
    "@SShMirziyoyeva",
]
TARGET_CHANNEL = "@kontexnazorat"

# ================== ASOSIY LOGIKA ==================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    source_name = event.chat.title if event.chat else "Kanal"
    try:
        await client.send_message(TARGET_CHANNEL, event.message)
        logging.info(f"✅ REPOST: [{source_name}] -> {TARGET_CHANNEL}")
    except Exception as e:
        logging.error(f"❌ Xatolik: {e}")

async def main():
    if not SESSION_STRING:
        logging.error("❌ SESSION_STRING topilmadi! Sozlamalarni tekshiring.")
        return

    await client.start()
    logging.info("🚀 USER-BOT KOYEBDA ISHGA TUSHDI!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:

        pass

