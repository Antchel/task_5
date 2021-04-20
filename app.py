from flask import Flask, request, jsonify
import sqlite3 as lite

app = Flask(__name__)

con = lite.connect('test.db', check_same_thread=False)
cur = con.cursor()


@app.route('/subscriptions/categories/<operation_id>', methods=['GET', 'POST'])
def categories(operation_id):
    return f'Category operation number: {operation_id}'


@app.route('/subscriptions/keywords/<operation_id>', methods=['GET', 'POST'])
def keywords(operation_id):
    if request.method == 'GET':
        user = {"name": "nick", 'email': 'example.com', 'tel': ['+790853535', '+783294892384']}
        return jsonify(user)
    return f'Category operation number: {operation_id}'


@app.route('/users/', methods=['GET', 'POST'])
def users():
    user = {"name": "nick", 'email': 'example.com', 'tel': ['+790853535', '+783294892384']}
    return jsonify(user)


@app.route('/news/', methods=['GET'])
def get_news():
    news = {"News": "All is good"}
    return jsonify(news)


if __name__ == '__main__':
    app.run()
