from flask import Flask, render_template, request, redirect, url_for
from operator import attrgetter
import todo_app.data.trello_items as trello_items
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    return render_template('index.html', items=sorted(trello_items.get_items(), key=attrgetter('status'), reverse=True))


@app.route('/item/add', methods=["POST"])
def add_item():
    trello_items.add_item(request.form.get('item-title'), request.form.get('item-desc'), request.form.get('due-date'))
    return redirect(url_for('index'))


@app.route('/item/status/', methods=["POST"])
def change_status():
    trello_items.change_status(request.form.get('item-id'))
    return redirect(url_for('index'))


@app.route('/item/remove', methods=["POST"])
def remove_item():
    trello_items.remove_item(request.form.get('item-id'))
    return redirect(url_for('index'))
