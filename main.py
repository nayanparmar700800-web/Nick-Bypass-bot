import os
import time
import telebot
import requests
from flask import Flask
from threading import Thread

# Flask web server to fix Render port binding
app = Flask('')

@app.route('/')
def home():
    return "Universal Bypasser Bot is 100% Active!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Telegram Bot Setup
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Super Multi-Server Bypasser Function to bypass ALL links
def bypass_link(url):
    # Server 1: Premium Universal Bypass API
    try:
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if data.get("status") == "success" and data.get("bypassed_url"):
            return data.get("bypassed_url")
    except:
        pass  # If Server 1 fails, move to Server 2

    # Server 2: Powerful Multi-Bypasser Backup API
    try:
        api_url2 = f"https://api.g9bypasser.xyz/bypass?url={url}"
        response2 = requests.get(api_url2, timeout=10)
        data2 = response2.json()
        if data2.get("success") and data2.get("bypassed_url"):
            return data2.get("bypassed_url")
    except:
        pass  # If Server 2 fails, move to Server 3

    # Server 3: Advanced Redirect Scraper & Unshortener
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        res = requests.get(url, headers=headers, allow_redirects=True, timeout=12)
        if res.url and res.url != url:
            return res.url
    except:
        pass

    return None

# /start Command Handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "❤️😊 <b>Universal Link Bypass Bot</b> 😊❤️\n\n"
        "👋 <b>Hello!</b> Welcome to the Ultimate Link Bypasser Bot.\n\n"
        "🔗 Just send me any shortener link, and I will bypass it to find the original main link instantly!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

# Message Handler with Premium Blue Link Texture Layout
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    if "http://" in user_text or "https://" in user_text:
        start_time = time.time()
        
        # Processing message
        status_msg = bot.send_message(message.chat.id, "⏳ <b>Bypassing your link using Multi-Servers, please wait...</b>", parse_mode='HTML')
        
        try:
            bypassed_result = bypass_link(user_text)
            end_time = time.time()
            time_taken = round(end_time - start_time)

            # Check if bypass was successful, else fallback to safe link
            if bypassed_result and bypassed_result != user_text:
                final_bypassed = bypassed_result
            else:
                final_bypassed = "https://t.me/nickbypassbot007" # Fallback if link is totally dead

            # Added <a href='...'> tag inside blockquotes to make links bright BLUE
            response_text = (
                f"❤️😊 <b>{message.from_user.first_name}</b> 😊❤️\n"
                f"<a href='{user_text}'>{user_text}</a>\n\n"
                f"<blockquote><b>Original Link :</b> ❞\n"
                f"✅ <a href='{user_text}'>{user_text}</a></blockquote>\n"
                f"<blockquote><b>Bypassed Link :</b> ❞\n"
                f"✅ <a href='{final_bypassed}'>{final_bypassed}</a></blockquote>\n"
                f"<blockquote><b>Time Taken : {time_taken} seconds</b> ❞</blockquote>\n"
                f"_____________________\n\n"
                f"<blockquote><b>24-6-2026 : Universal Multi-Server Active</b> ❞</blockquote>\n\n"
                f"<b>Get Free update chennal :</b> <a href='https://t.me/nickbypassbot007'>Join Channel</a>\n\n"
                f"<blockquote>Share and Support Bot, We are helping you to save your time and you can help us by sharing to your friends. ❞</blockquote>\n"
                f"<blockquote><b>Powered By</b> @nickbypassbot007 ❞</blockquote>"
            )
            
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=status_msg.message_id,
                text=response_text,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            
        except Exception as e:
            bot.edit_message_text(f"❌ <b>Error occurred:</b> {str(e)}", message.chat.id, status_msg.message_id, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "❌ Please send a valid link (URL).")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot architecture is running successfully with universal multi-server layout...")
    bot.infinity_polling()
