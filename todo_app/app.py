from flask import Flask, render_template, request, redirect, url_for
import todo_app.data.trello_items as trello_items
from todo_app.flask_config import Config
from todo_app.models.index_model import IndexModel

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    index_model = IndexModel(trello_items.get_items())
    return render_template('index.html', view_model=index_model)


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
