import os
import time
import telebot
import requests
from flask import Flask
from threading import Thread

# Render પોર્ટ ફિક્સ કરવા માટે Flask વેબ સર્વર
app = Flask('')

@app.route('/')
def home():
    return "Bot is 100% Active!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ટેલિગ્રામ બોટ સેટઅપ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# સાચું લિંક બાયપાસ કરવાનું ફંક્શન
def bypass_link(url):
    try:
        # બધી શોર્ટનર લિંક્સને સપોર્ટ કરતી પાવરફુલ ફ્રી API
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=15)
        data = response.json()
        
        # જો API સફળતાપૂર્વક લિંક બાયપાસ કરે તો સાચી લિંક મોકલો
        if data.get("status") == "success" and data.get("bypassed_url"):
            return data.get("bypassed_url")
        else:
            # જો કોઈ કારણસર સર્વર ૧ કામ ન કરે તો બેકઅપ તરીકે ડાયરેક્ટ રિસ્પોન્સ ચેક કરવો
            # આ લોજિક earnlinks અને linksgo જેવી સાઇટ્સ માટે બેકઅપ આપશે
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
            if res.url != url:
                return res.url
            return "❌ આ લિંક સપોર્ટેડ નથી અથવા હમણાં બાયપાસ થઈ શકે તેમ નથી."
    except Exception as e:
        return f"❌ સર્વર એરર: {str(e)}"

# /start કમાન્ડ હેન્ડલર
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "❤️😊 *Nick Bypass Bot* 😊❤️\n\n"
        "👋 *Hello!* Welcome to the Link Bypasser Bot.\n\n"
        "🔗 Send me any shortener link (like earnlinks, linksgo, followyou),\n"
        "and I will bypass it for you instantly!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

# લિંક મેસેજ હેન્ડલર
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    if "http://" in user_text or "https://" in user_text:
        start_time = time.time()
        
        # વેટિંગ મેસેજ
        status_msg = bot.send_message(message.chat.id, "⏳ *Processing your link, please wait...*", parse_mode='Markdown')
        
        try:
            # બાયપાસ ફંક્શન કોલ
            bypassed_result = bypass_link(user_text)
            
            end_time = time.time()
            time_taken = round(end_time - start_time)

            response_text = (
                f"❤️😊 *{message.from_user.first_name}* 😊❤️\n"
                f"`{user_text}`\n\n"
                f"📝 *Original Link :* ❞\n"
                f"✅ {user_text}\n\n"
                f"🔓 *Bypassed Link :* ❞\n"
                f"✅ {bypassed_result}\n\n"
                f"⏱️ *Time Taken :* {time_taken} seconds ❞\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"📢 *Get Free Updates :* [Join Channel](https://t.me/nickbypass_bot_2007)\n\n"
                f"💡 *Share and Support Bot:* We are helping you to save your time and you can help us by sharing to your friends.\n\n"
                f"⚡ *Powered By :* @Nick_Bypass_Bot"
            )
            
            bot.edit_message_text(response_text, message.chat.id, status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)
            
        except Exception as e:
            bot.edit_message_text(f"❌ *Error occurred:* {str(e)}", message.chat.id, status_msg.message_id, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Please send a valid link (URL).")

# બોટ અને સર્વર રન કરવા માટે
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Bot architecture is running successfully...")
    bot.infinity_polling()
