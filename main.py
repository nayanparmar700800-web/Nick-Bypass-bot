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
    return "Bot is 100% Active!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# Telegram Bot Setup
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Link Bypasser Function
def bypass_link(url):
    try:
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        if data.get("status") == "success" and data.get("bypassed_url"):
            return data.get("bypassed_url")
        else:
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            if res.url != url:
                return res.url
            return None
    except Exception as e:
        return None

# /start Command Handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "❤️😊 <b>Nick Bypass Bot</b> 😊❤️\n\n"
        "👋 <b>Hello!</b> Welcome to the Link Bypasser Bot.\n\n"
        "🔗 Send me any shortener link and I will bypass it instantly!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

# Message Handler with Premium Blue Link Texture Layout
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    if "http://" in user_text or "https://" in user_text:
        start_time = time.time()
        
        # Processing message
        status_msg = bot.send_message(message.chat.id, "⏳ <b>Processing your link, please wait...</b>", parse_mode='HTML')
        
        try:
            bypassed_result = bypass_link(user_text)
            end_time = time.time()
            time_taken = round(end_time - start_time)

            # Check if bypass was successful, else fallback to safe link
            final_bypassed = bypassed_result if bypassed_result else "https://t.me/nickbypassbot007"

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
                f"<blockquote><b>24-6-2026 : Fixed v2links Bypass</b> ❞</blockquote>\n\n"
                f"<b>Get Free update chennal 👉 :</b> <a href='https://t.me/nickbypassbot007'>Join Channel</a>\n\n"
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
    print("Bot architecture is running successfully with premium blue-link layout...")
    bot.infinity_polling()
