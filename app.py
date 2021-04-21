from flask import Flask, request, jsonify
import sqlite3 as lite
from newsapi import NewsApiClient
from config import newsApi_token

user_cred = 0

app = Flask(__name__)

con = lite.connect('test.db', check_same_thread=False)
cur = con.cursor()


def add_user(user_id):
    global user_cred
    user_cred = user_id
    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY,'
                ' f_name varchar(50), l_name varchar(50));')
    cur.execute('CREATE TABLE IF NOT EXISTS categories (category_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'cat_name varchar(100), user_id INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS keywords (keyword_id integer primary key AUTOINCREMENT,'
                'word_name varchar(100), user_id INTEGER)')
    user_data = cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
    if user_data is None:
        cur.execute(f"INSERT INTO users (user_id) VALUES "
                    f" ({user_id})")
        con.commit()
        return "User added"
    return f"Hello {user_id}"


def add_category(category):
    cat_data = cur.execute(f"SELECT * FROM categories WHERE cat_name = '{category}' "
                           f"AND user_id = {user_cred}").fetchone()
    print(cat_data)
    if cat_data is None:
        cur.execute(f"INSERT INTO categories (cat_name, user_id) VALUES "
                    f" ('{category}',"
                    f" {user_cred})")
        con.commit()
        return "Category was added"
    else:
        return "This category is already exists"


def add_keyword(message):
    key_data = cur.execute(f"SELECT * FROM keywords WHERE word_name = '{message}' "
                           f"AND user_id = {user_cred}").fetchone()
    if key_data is None:
        cur.execute(f"INSERT INTO keywords (word_name, user_id) VALUES "
                    f" ('{message}',"
                    f" {user_cred})")
        con.commit()
        return "Keyword was added successfully"
    else:
        return "This keyword is already exists"


def show_categories():
    user_cats = cur.execute(f"SELECT cat_name FROM categories WHERE user_id = {user_cred}").fetchall()
    if user_cats is None:
        return "You haven't any categories"
    else:
        return f"List of your chosen categories {user_cats}"


def show_keywords():
    user_keyw = cur.execute(f"SELECT word_name FROM keywords WHERE user_id = {user_cred}").fetchall()
    if user_keyw is None:
        return "You haven't any keywords"
    else:
        return f"List of your chosen categories : {user_keyw}"


def remove_category(cat_name):
    cur.execute(f"DELETE FROM categories WHERE cat_name = '{cat_name}'")
    con.commit()


def remove_keyword(word_name):
    cur.execute(f"DELETE FROM keywords WHERE word_name = '{word_name}'")
    con.commit()


@app.route('/subscriptions/categories/<category>', methods=['GET', 'PUT', 'DELETE'])
def categories(category):
    if request.method == 'GET':
        cats = show_categories()
        return jsonify(f'{cats}')
    if request.method == 'PUT':
        add_category(category)
        return jsonify(f'Category was added')
    if request.method == 'DELETE':
        remove_category(category)
        return f'Category {category} was DELETED'


@app.route('/subscriptions/keywords/<keyword>', methods=['GET', 'PUT', 'DELETE'])
def keywords(keyword):
    if request.method == 'GET':
        keywords = show_keywords()
        return jsonify(keywords)
    if request.method == 'PUT':
        add_keyword(keyword)
        return jsonify(f'keyword was added')
    if request.method == 'DELETE':
        remove_keyword(keyword)
        return f'keyword {keyword} was DELETED'


@app.route('/users/<user_id>', methods=['GET'])
def users(user_id):
    if request.method == 'GET':
        ret = add_user(user_id)
        return jsonify(ret)
    return jsonify("Error mzfk")


@app.route('/news/', methods=['GET'])
def get_news():
    newsapi = NewsApiClient(api_key=newsApi_token)
    if request.method == 'GET':
        user_cats = cur.execute(
            f"SELECT cat_name FROM categories WHERE user_id = {user_cred}").fetchall()
        user_keyw = cur.execute(
            f"SELECT word_name FROM keywords WHERE user_id = {user_cred}").fetchall()

        category_list = [item for t in user_cats for item in t]
        keyword_list = [item for t in user_keyw for item in t]
        links = []
        titles = []
        for cat in category_list:
            for keyword in keyword_list:
                top_headlines = newsapi.get_top_headlines(q=keyword,
                                                          category=cat,
                                                          page_size=10,
                                                          page=1)
                print( f"News category is \"{cat}\"\n News keyword is \"{keyword}\"\n")
                articles = []
                articles = top_headlines['articles']
                if articles:
                    if len(articles) > 10:
                        cnt = 10
                    else:
                        cnt = len(articles)
                    for i in range(cnt):
                        print( f"====== {i} Article =========\n")
                        print("cnt = ", cnt)
                        print(top_headlines)
                        # print( f" Title \n {top_headlines['articles'][i]['title']}\n"
                        #       f" Link {top_headlines['articles'][i]['url']}\n")
                        links.append(top_headlines['articles'][i]['url'])
                        titles.append(top_headlines['articles'][i]['title'])
                else:
                    print("Can't found any news!\n")

        return jsonify(ok = 200, link = links)
    return jsonify("ok")


if __name__ == '__main__':
    app.run()
