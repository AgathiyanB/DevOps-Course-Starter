import os
import pytest
import requests
from dotenv import load_dotenv, find_dotenv
from todo_app import app


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data


def stub(request_string, params={}):
    url = request_string.split('?')[0]
    test_board_id = os.environ.get('BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{'id': '1', 'name': "To Do"},
                              {'id': '2', 'name': "Doing"},
                              {'id': '3', 'name': "Done"}]
    elif url == f'https://api.trello.com/1/boards/{test_board_id}/cards':
        fake_response_data = [{'id': 'a', 'name': "ItemToDo", 'idList': '1', 'desc': "Desc1", 'due': "2022-07-15T00:00:00.000000Z"},
                              {'id': 'a', 'name': "ItemDoing", 'idList': '2', 'desc': "Desc1", 'due': "2022-07-15T00:00:00.000000Z"},
                              {'id': 'a', 'name': "ItemDone", 'idList': '3', 'desc': "Desc1", 'due': "2022-07-15T00:00:00.000000Z"}]
    if fake_response_data:
        return StubResponse(fake_response_data)
    else:
        raise Exception(f'Unexpected URL in integration test')


@pytest.fixture
def client(monkeypatch):
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    monkeypatch.setattr(requests, 'get', stub)
    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client


def test_index_page(monkeypatch, client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'ItemToDo' in response.data.decode()
    assert 'ItemDoing' in response.data.decode()
    assert 'ItemDone' in response.data.decode()