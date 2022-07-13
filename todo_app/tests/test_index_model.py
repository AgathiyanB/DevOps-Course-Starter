import pytest
from todo_app.models.index_model import IndexModel
from todo_app.classes.item import Item

doing_item = Item('1', 'Title', 'Desc', status="Doing")
to_do_item = Item('2', 'Title', 'Desc', status="To Do")
done_item = Item('3', 'Title', 'Desc', status="Done")

fake_items = [doing_item, to_do_item, done_item]


@pytest.fixture
def index_model(monkeypatch):
    model = IndexModel(fake_items)
    return model


def test_doing_items(index_model):
    assert doing_item in index_model.doing_items


def test_to_do_items(index_model):
    assert to_do_item in index_model.to_do_items


def test_done_items(index_model):
    assert done_item in index_model.done_items