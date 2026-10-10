import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL

# --- APNI DETAILS YAHAN DAALEIN ---
API_ID = 39711804                  # Apna api_id number dalein
API_HASH = "db774c3ee3ec09833ef6a516d9a33b8d"    # Apna api_hash dalein
BOT_TOKEN = "8886341619:AAGNxIaqURUThJyaCcSv_I8by4d5p6ibLDo"  # BotFather wala token dalein
CHANNEL_ID = -1004228329616        # Apne Telegram channel ki ID dalein

app = Client("my_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.text & ~filters.command(["start"]))
def handle_link(client, message):
    link = message.text
    message.reply_text("🔄 Link mil gaya hai, process shuru ho raha hai...")
    
    file_path = None
    try:
        message.reply_text("📥 Video/File download ho rahi hai...")
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            file_path = ydl.prepare_filename(info)

        # Upload to Telegram Cloud Channel
        if file_path and os.path.exists(file_path):
            message.reply_text("📤 Aapke Telegram Cloud Channel par upload ho raha hai...")
            client.send_document(
                chat_id=CHANNEL_ID,
                document=file_path,
                caption=f"Downloaded from: {link}"
            )
            message.reply_text("✅ Success! Cloud par save ho gaya hai.")
            
            # Clean up local storage
            os.remove(file_path)
        else:
            message.reply_text("❌ File download nahi ho payi.")

    except Exception as e:
        message.reply_text(f"❌ Error aa gaya: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    print("🤖 Bot live ho gaya hai!")
    app.run()
