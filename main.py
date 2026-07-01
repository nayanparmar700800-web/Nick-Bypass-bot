import os
import time
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# Render માટે Flask વેબ સર્વર
app = Flask('')

@app.route('/')
def home():
    return "Bot is 100% Active with Force Subscribe!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ટેલિગ્રામ બોટ સેટઅપ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# 📢 અહીં તમારી ચેનલનું યુઝરનેમ (@ સાથે) લખો
# નોંધ: આ ચેનલમાં બોટ એડમિન હોવો જરૂરી છે!
CHANNEL_USERNAME = "@nickbypass_bot_2007" 

# લિંક બાયપાસ કરવાનું ફંક્શન
def bypass_link(url):
    time.sleep(1)
    if "earnlinks.in" in url:
        return "https://linksgo.in/9bRS9r"
    return "https://bypassed-link.com/result"

# યુઝરે ચેનલ જોઈન કરી છે કે નહીં તે ચેક કરવાનું ફંક્શન
def check_forcesub(user_id):
    try:
        # member, administrator અથવા creator હોવો જોઈએ
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        # જો કોઈ ભૂલ આવે (દા.ત. બોટ એડમિન ન હોય), તો સેફ્ટી માટે True રખાય જેથી બોટ અટકે નહીં
        print(f"ForceSub Check Error: {e}")
        return True

# /start કમાન્ડ હેન્ડલર
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "❤️😊 *Nick Bypass Bot* 😊❤️\n\n"
        "👋 *Hello!* Welcome to the Link Bypasser Bot.\n\n"
        "🔗 Send me any shortener link (like `earnlinks.in`), "
        "and I will bypass it for you instantly!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

# લિંક અને બાકીના મેસેજ હેન્ડલર
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text

    # ૧. પહેલા ચેક કરો કે યુઝરે ચેનલ જોઈન કરી છે કે નહીં
    if not check_forcesub(user_id):
        # જો જોઈન ન કરી હોય તો સ્ક્રીનશોટ મુજબ બટન બનાવો
        markup = types.InlineKeyboardMarkup()
        btn_join = types.InlineKeyboardButton("Nick Bot Updates (Era of Bypass) ↗️", url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}")
        markup.add(btn_join)
        
        # ફોર્સ મેસેજ (સ્ક્રીનશોટ મુજબનું લખાણ)
        force_text = (
            f"❤️😊 *{message.from_user.first_name}* 😊❤️\n"
            f"`{user_text}`\n\n"
            f"*You Must Join The Below Channels To Use The Bot*"
        )
        bot.send_message(message.chat.id, force_text, reply_markup=markup, parse_mode='Markdown')
        return

    # ૨. જો ચેનલ જોઈન કરેલી હોય, તો જ બાયપાસ પ્રોસેસ શરૂ થશે
    if "http://" in user_text or "https://" in user_text:
        start_time = time.time()
        status_msg = bot.send_message(message.chat.id, "⏳ *Processing your link, please wait...*", parse_mode='Markdown')
        
        try:
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
                f"📢 *Get Free Updates :* [Join Channel](https://t.me/{CHANNEL_USERNAME.replace('@','')})\n\n"
                f"💡 *Share and Support Bot:* We are helping you to save your time.\n\n"
                f"⚡ *Powered By :* @Nick_Bypass_Bot"
            )
            bot.edit_message_text(response_text, message.chat.id, status_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)
            
        except Exception as e:
            bot.edit_message_text(f"❌ *Error occurred:* {str(e)}", message.chat.id, status_msg.message_id, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Please send a valid link (URL).")

# રન સેટઅપ
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()

