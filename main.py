import os
import asyncio
import re
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
# --- APNI DETAILS YAHAN DAALEIN ---
API_ID = 39711804                  # Apna api_id number dalein
API_HASH = "db774c3ee3ec09833ef6a516d9a33b8d"    # Apna api_hash dalein
BOT_TOKEN = "8886341619:AAGNxIaqURUThJyaCcSv_I8by4d5p6ibLDo"  # BotFather wala token dalein
CHANNEL_ID = -1004228329616        # Apne Telegram channel ki ID dalein

bot = Client("all_in_one_downloader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Helper: Link Type Pehchanne ke liye
def detect_provider(url):
    if "terabox" in url:
        return "terabox"
    elif "diskwala" in url:
        return "diskwala"
    elif "flezen" in url:
        return "flezen"
    elif any(x in url for x in ["youtube.com", "youtu.be", "instagram.com", "facebook.com", "fb.watch"]):
        return "social"
    return "unknown"

# Cloud Links Bypass Logic (TeraBox / DiskWala / Flezen)
async def bypass_cloud_link(url):
    try:
        # Yeh ek generic extractor mechanism hai jo links ke direct stream/download source ko target karta hai
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cloud providers ke page se direct video source dhundne ki koshish
        video_tag = soup.find('video')
        if video_tag and video_tag.get('src'):
            return video_tag['src']
        
        # Agar direct source na mile toh fallback API/Scraper logic
        # (Aap yahan apni custom bypass API endpoint bhi connect kar sakte hain)
        return None
    except Exception as e:
        print(f"Bypass Error: {str(e)}")
        return None

# /start Command Handler
@bot.on_message(filters.command(["start"]))
async def start_handler(client, message):
    await message.reply_text(
        "👋 **Welcome to All-in-One Media Bot!**\n\n"
        "Mujhe koi bhi link bhejo (TeraBox, DiskWala, Flezen, YouTube, Instagram, Facebook).\n"
        "Main aapko **Online Play (Stream)** aur **Download/Audio Trim** ke options dunga!"
    )

# General Link / Message Handler
@bot.on_message(filters.text & ~filters.command(["start"]))
async def main_handler(client, message):
    url = message.text.strip()
    provider = detect_provider(url)
    
    if provider == "unknown":
        await message.reply_text("❌ Yeh link supported nahi hai. Kripya valid TeraBox, DiskWala, Flezen ya Social Media link bhejiye.")
        return
    
    await message.reply_text(f"🔍 Link detect ho gaya ({provider.upper()}). Process shuru ho raha hai...")

    if provider in ["terabox", "diskwala", "flezen"]:
        # Cloud Links Processing
        direct_link = await bypass_cloud_link(url)
        if direct_link:
            await message.reply_text(
                f"✅ **Link Bypass Successful!**\n\n"
                f"🔗 **Stream Link:** {direct_link}\n\n"
                f"Aap is link ko kisi bhi video player (VLC/MX Player) mein chala sakte hain!"
            )
        else:
            await message.reply_text("⚠️ Is link ka direct stream link nahi mil paya. Yeh protected ho sakta hai.")
            
    elif provider == "social":
        # Social Media (YouTube/Insta/FB) Processing with Options
        await message.reply_text("📥 Social media video fetch ho rahi hai, kripya thoda intezaar karein...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'downloads/%(title)s.%(ext)s'}
            loop = asyncio.get_event_loop()
            
            def download_media():
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    return ydl.prepare_filename(info)
            
            file_path = await loop.run_in_executor(None, download_media)
            
            if file_path and os.path.exists(file_path):
                await client.send_video(
                    chat_id=CHANNEL_ID,
                    video=file_path,
                    caption=f"🎬 Downloaded from: {url}"
                )
                await message.reply_text("✅ Video aapke private channel par successfully save ho gayi hai!")
                os.remove(file_path)
            else:
                await message.reply_text("❌ Social media video download nahi ho payi.")
        except Exception as e:
            await message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    bot.run()
