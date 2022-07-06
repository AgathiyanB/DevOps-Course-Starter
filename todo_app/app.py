from flask import Flask, render_template, request, redirect, url_for
from operator import itemgetter
from todo_app.data.session_items import get_items, add_item, change_item_status, remove_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=sorted(get_items(), key=itemgetter('status'), reverse=True))


@app.route('/item/add', methods=["POST"])
def add_an_item():
    add_item(request.form.get('item-title'))
    return redirect(url_for('index'))


@app.route('/item/status', methods=["POST"])
def change_status():
    change_item_status(request.form.get('item-id'))
    return redirect(url_for('index'))


@app.route('/item/remove', methods=["POST"])
def remove_an_item():
    remove_item(request.form.get('item-id'))
    return redirect(url_for('index'))
