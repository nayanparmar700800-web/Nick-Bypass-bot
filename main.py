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

# લિંક બાયપાસ કરવાનું ફંક્શન (તમારા અસલી API સાથે આને બદલી શકો છો)
def bypass_link(url):
    time.sleep(1) # ડેમો પ્રોસેસિંગ ટાઈમ માટે ૧ સેકન્ડનો હોલ્ડ
    if "earnlinks.in" in url:
        return "https://linksgo.in/9bRS9r"
    return "https://bypassed-link.com/result"

# /start કમાન્ડ હેન્ડલર (In English)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "❤️😊 *Nick Bypass Bot* 😊❤️\n\n"
        "👋 *Hello!* Welcome to the Link Bypasser Bot.\n\n"
        "🔗 Send me any shortener link (like `earnlinks.in`), "
        "and I will bypass it for you instantly!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

# લિંક મેસેજ હેન્ડલર (In English - exact same structure as screenshot)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text

    if "http://" in user_text or "https://" in user_text:
        # સમય ગણવાનું શરૂ કરો
        start_time = time.time()
        
        # વેટિંગ મેસેજ
        status_msg = bot.send_message(message.chat.id, "⏳ *Processing your link, please wait...*", parse_mode='Markdown')
        
        try:
            # બાયપાસ ફંક્શન કોલ
            bypassed_result = bypass_link(user_text)
            
            # સમયની ગણતરી
            end_time = time.time()
            time_taken = round(end_time - start_time)

            # સ્ક્રીનશોટ મુજબનું પ્રોફેસનલ ઇંગ્લિશ ફોર્મેટ
            response_text = (
                f"❤️😊 *{message.from_user.first_name}* 😊❤️\n"
                f"`{user_text}`\n\n"
                f"📝 *Original Link :* ❞\n"
                f"✅ {user_text}\n\n"
                f"🔓 *Bypassed Link :* ❞\n"
                f"✅ {bypassed_result}\n\n"
                f"⏱️ *Time Taken :* {time_taken} seconds ❞\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"📢 *Get Free Updates :* [Join Channel](https://t.me/your_channel_username)\n\n"
                f"💡 *Share and Support Bot:* We are helping you to save your time and you can help us by sharing to your friends.\n\n"
                f"⚡ *Powered By :* @Nick_Bypass_Bot"
            )
            
            # મેસેજ એડિટ કરીને ફાઇનલ રીઝલ્ટ મોકલો
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
