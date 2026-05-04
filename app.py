import os
import asyncio
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8704796295:AAHc3WPYZs0Vxn6PdLVJcDLkjUgjtOZmJx8"
MONGO_URL = os.environ.get("MONGO_URL") # Render Environment Variable se aayega
TARGET_CHANNEL = -100xxxxxxxxx # Jahan drop karna hai

# --- DATABASE SETUP ---
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["IG_DROP_BOT"]
collection = db["bins_history"]

# --- WEB SERVER FOR RENDER (KEEP-ALIVE) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Running!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- BOT LOGIC ---
bot = Client("ig_drop_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.group | filters.channel)
async def bin_scraper(client, message):
    if not message.text: return
    
    # Regex to find 6-digit BINs
    bins = set(re.findall(r'\b\d{6}\b', message.text))
    
    for bin_code in bins:
        # Check if BIN already in MongoDB
        exists = await collection.find_one({"bin": bin_code})
        
        if not exists:
            # Instagram Compatibility Check (Simple logic)
            # Yahan hum check kar sakte hain ki BIN naya hai ya nahi
            await collection.insert_one({"bin": bin_code})
            
            drop_text = (
                f"🚀 **New IG Support BIN Found**\n\n"
                f"💳 **BIN:** `{bin_code}`\n"
                f"📱 **Status:** Checking for Meta/Instagram...\n"
                f"📅 **Date:** {asyncio.get_event_loop().time()}"
            )
            await bot.send_message(TARGET_CHANNEL, drop_text)

if __name__ == "__main__":
    # Start Keep-Alive Server
    Thread(target=run_web).start()
    # Start Bot
    bot.run()
