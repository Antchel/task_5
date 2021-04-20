import requests
import telebot
from config import telegram_token


bot = telebot.TeleBot(telegram_token, parse_mode=None)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Add news category', 'Add news keyword')
keyboard.row('Show my categories', 'Show my keywords')
keyboard.row('Remove category', 'Remove keyword')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    a = requests.get('http://127.0.0.1:5000/users/')
    print(a.json())


@bot.message_handler(commands=['help'])
def send_welcome(message):
    a = requests.get('http://127.0.0.1:5000/rest')
    print(a.json())
    bot.reply_to(message, f"msg = {message.text} There is a short list of possible commands\n"
                          f"/start - this command registry user (if he isn't registry) and opens main menu\n"
                          f"/show_news - this command show news based on chosen categories and keywords\n")


@bot.message_handler(commands=['show_news'])
def get_news(message):
    a = requests.get('http://127.0.0.1:5000/news')
    print(a.json())
    bot.reply_to(message, a.json()['News'])


bot.polling()
