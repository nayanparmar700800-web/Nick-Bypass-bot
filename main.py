import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "નમસ્તે! મને લિંક મોકલો, હું તેને ચેક કરીશ. (નોંધ: આ એક ટેસ્ટ બોટ છે)")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if "http" in message.text:
        bot.reply_to(message, "લિંક મળી ગઈ છે! પ્રોસેસ શરૂ થઈ રહી છે...")
    else:
        bot.reply_to(message, "કૃપા કરીને સાચી લિંક મોકલો.")

print("બોટ ચાલુ થઈ ગયો છે...")
bot.infinity_polling()
