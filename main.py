import os
import telebot
from flask import Flask
from threading import Thread

# Render ની પોર્ટ એરર ફિક્સ કરવા માટે વેબ સર્વર
app = Flask('')

@app.route('/')
def home():
    return "બોટ લાઈવ છે!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# ટેલિગ્રામ બોટ સેટઅપ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "નમસ્તે! મને લિંક મોકલો, હું તેને ચેક કરીશ.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "http" in message.text:
        bot.send_message(message.chat.id, "લિંક મળી ગઈ છે! પ્રોસેસ શરૂ થઈ રહી છે...")
    else:
        bot.send_message(message.chat.id, "કૃપા કરીને સાચી લિંક મોકલો.")

# બંને વસ્તુ એકસાથે ચલાવવા માટે
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("બોટ ચાલુ થઈ ગયો છે...")
    bot.infinity_polling()
