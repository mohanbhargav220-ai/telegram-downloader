import asyncio
import threading
from flask import Flask

# Pyrogram aur Python 3.14 ke event loop error ko fix karne ke liye
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import main  # Yeh aapke downloader bot ko background mein chalu karega

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
