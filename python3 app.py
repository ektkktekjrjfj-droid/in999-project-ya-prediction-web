# -*- coding: utf-8 -*-
import os
import asyncio
import logging
from io import BytesIO
from datetime import datetime
from pyrogram import Client, filters, types
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont

# Logging setup taaki errors saaf dikhein
logging.basicConfig(level=logging.INFO)

# --- CONFIG ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8056440527:AAHtaVS-1kSRqu0d0YZ9-ugTU-V6nZiGsXI"
MONGO_URL = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority"

# Client & DB Initialization
app = Client("protection_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = MongoClient(MONGO_URL)
db = db_client["ProtectionBotDB"]
reports_col = db["user_reports"]

# --- EXACT TEXT FORMAT ---
START_TEXT = (
    "┏━━━━━ 👋 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 👋 ━━━━━┓\n\n"
    "Hello There! I'm the Copyright Protection Bot – your channel's guardian.\n\n"
    "✨ Features:\n"
    "  ┣━ Protect from copyright strikes\n"
    "  ┣━ Prevent fake reports\n"
    "  ┣━ Monitor suspicious activity\n"
    "  ┗━ Secure your content 24/7\n\n"
    "🔰 Tap /start to use me and save your channel from being banned! 🚀\n\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"
)

async def create_welcome_image(user_id, user_photo_id):
    bg = Image.new('RGB', (800, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(bg)
    draw.rectangle([0, 0, 30, 400], fill=(76, 175, 80))

    if user_photo_id:
        try:
            path = await app.download_media(user_photo_id)
            user_img = Image.open(path).convert("RGBA").resize((160, 160))
            mask = Image.new("L", (160, 160), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 160, 160), fill=255)
            bg.paste(user_img, (60, 120), mask)
            os.remove(path)
        except Exception as e:
            logging.error(f"Image Error: {e}")

    try:
        font = ImageFont.load_default()
        draw.text((250, 160), "🛡️ SHIELD ACTIVE ✅", fill=(0, 0, 0), font=font)
    except:
        draw.text((250, 160), "SHIELD ACTIVE ✅", fill=(0, 0, 0))

    img_io = BytesIO()
    bg.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

# --- HANDLERS ---
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_photo = message.from_user.photo.big_file_id if message.from_user.photo else None
    photo = await create_welcome_image(message.from_user.id, user_photo)
    await message.reply_photo(photo=photo, caption=START_TEXT)

@app.on_message(filters.group & (filters.regex("(?i)report") | filters.regex("(?i)copyright")))
async def anti_report_shield(client, message):
    try:
        reports_col.insert_one({
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "time": datetime.now()
        })
        await message.delete()
    except Exception as e:
        logging.error(f"DB/Delete Error: {e}")

# --- REFRESHED STARTUP LOGIC ---
async def start_bot():
    try:
        await app.start()
        logging.info("✅ BOT IS LIVE AND SECURE")
        await asyncio.Event().wait()
    except Exception as e:
        logging.error(f"Startup Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
