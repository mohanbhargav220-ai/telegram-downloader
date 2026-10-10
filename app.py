from flask import Flask
import threading
import main  # Yeh aapke bot ko background mein chalu karega

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running live!"

def run_bot():
    # Agar aapke main.py mein app.run() hai toh theek, nahi toh Pyrogram client start hoga
    pass

if __name__ == "__main__":
    # Web server ko start karna taaki Render free tier active rakhe
    app.run(host="0.0.0.0", port=10000)