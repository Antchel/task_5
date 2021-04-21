import requests
import telebot
from config import telegram_token

state = 0

bot = telebot.TeleBot(telegram_token, parse_mode=None)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Add news category', 'Add news keyword')
keyboard.row('Show my categories', 'Show my keywords')
keyboard.row('Remove category', 'Remove keyword')


@bot.message_handler(commands=['start'])
def send_start(message):
    a = requests.get(f'http://127.0.0.1:5000/users/{message.from_user.id}')
    print(a.json())
    bot.reply_to(message, f"Hello {message.from_user.first_name}, nice to meet you!\n Choose what you want!",
                 reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    a = requests.get('http://127.0.0.1:5000/rest')
    print(a.json())
    bot.reply_to(message, f"msg = {message.text} There is a short list of possible commands\n"
                          f"Yuo should start you discussion with bot with /start command\n"
                          f"/start - this command registry user (if he isn't registry) and opens main menu\n"
                          f"/show_news - this command show news based on chosen categories and keywords\n")


@bot.message_handler(commands=['show_news'])
def get_news(message):
    a = requests.get('http://127.0.0.1:5000/news/')
    for i in range(len(a.json()['link'])):
        bot.reply_to(message, (a.json()['link'][i]))


@bot.message_handler(content_types=["text"])
def main(message):
    global state

    if state == 1:
        print(message.text)
        requests.put(f'http://127.0.0.1:5000/subscriptions/categories/{message.text}')
        state = 0
    elif state == 2:
        print(message.text)
        requests.put(f'http://127.0.0.1:5000/subscriptions/keywords/{message.text}')
        state = 0
    elif state == 5:
        requests.delete(f'http://127.0.0.1:5000/subscriptions/categories/{message.text}')
        state = 0
    elif state == 6:
        requests.delete(f'http://127.0.0.1:5000/subscriptions/keywords/{message.text}')
        state = 0
        # FIXME: Реализовать "вечную" клавиатуру

    bot.send_message(message.chat.id, 'done', reply_markup=telebot.types.ReplyKeyboardRemove())
    if message.text == "Add news category":
        state = 1
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        keyboard1.row('sports', 'business')
        keyboard1.row('entertainment', 'general')
        keyboard1.row('health', 'science')
        keyboard1.row('technology')
        bot.send_message(message.chat.id, "Choose the possible categories", reply_markup=keyboard1)
    elif message.text == 'Add news keyword':
        state = 2
        bot.send_message(message.chat.id, "Enter new keyword name")
    elif message.text == 'Show my categories':
        a = requests.get(f'http://127.0.0.1:5000/subscriptions/categories/{1}')
        bot.send_message(message.chat.id, f"{a.json()}")
    elif message.text == 'Show my keywords':
        a = requests.get(f'http://127.0.0.1:5000/subscriptions/keywords/{1}')
        bot.send_message(message.chat.id, f"{a.json()}")
    elif message.text == 'Remove category':
        state = 5
        bot.send_message(message.chat.id, "Enter name of category what you want to delete")
    elif message.text == 'Remove keyword':
        state = 6
        bot.send_message(message.chat.id, "Enter name of keyword what you want to delete")


bot.polling()
