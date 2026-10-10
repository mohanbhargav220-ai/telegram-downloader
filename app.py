import asyncio
import threading
from flask import Flask

# Pyrogram aur Python ke event loop error ko fix karnetry:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Background mein bot ko chalane ke liye function
def start_bot():
    import main  # Yeh aapke downloader bot ko import aur run karega

# Flask App Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live!"

if __name__ == "__main__":
    # Bot ko ek alag background thread mein start karein
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask web server ko start karein taaki Render khush rahe
    app.run(host="0.0.0.0", port=10000)
