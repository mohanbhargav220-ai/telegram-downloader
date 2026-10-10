import asyncio
import threading
from flask import Flask

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

def start_bot():
    import main  # Yeh bot ko background mein chalayega

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live!"

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    app.run(host="0.0.0.0", port=10000)
