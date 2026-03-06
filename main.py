import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== SOZLAMALAR ==================
API_ID = 25573417 
API_HASH = "b56082f4d86578c5a6948c7b964008f9"
SESSION_STRING = os.getenv("SESSION_STRING") 

SOURCE_CHANNELS = [
    "@uzdavgeolcom", "@shmirziyoyev", "BSA_uz", 
    "@adliyangiliklari", "@huquqiyaxborot", "@xavfsizlik_uz", "@antikor_uzb", 
    "@SShMirziyoyeva",
]
TARGET_CHANNEL = "@kontexnazorat"

# ================== ASOSIY LOGIKA ==================

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# Albumlarni (bir nechta rasm/video) va oddiy xabarlarni birdek boshqarish
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    # Agar xabar biror albumning qismi bo'lsa, uni to'liq yig'ilishini kutish kerak
    # Lekin eng oddiy va samarali yo'li - har bir media guruhini o'z ID'si bilan yuborish
    try:
        if event.grouped_id:
            # Agar bu album (media group) bo'lsa
            # Biz faqat birinchi xabar kelganda butun albumni yuboramiz
            # Buning uchun kodingizni biroz murakkablashtirmaslik uchun 'forward'dan foydalanamiz
            await client.forward_messages(TARGET_CHANNEL, event.message)
        else:
            # Oddiy xabar bo'lsa
            await client.send_message(TARGET_CHANNEL, event.message)
            
        logging.info(f"✅ REPOST: {TARGET_CHANNEL} kanaliga yuborildi.")
    except Exception as e:
        logging.error(f"❌ Xatolik: {e}")

async def main():
    if not SESSION_STRING:
        logging.error("❌ SESSION_STRING topilmadi! Sozlamalarni tekshiring.")
        return

    await client.start()
    logging.info("🚀 USER-BOT ALBUM QO'LLAB-QUVVATLASH BILAN ISHGA TUSHDI!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
