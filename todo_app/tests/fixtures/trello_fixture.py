import os
import requests
from dotenv import load_dotenv
from time import sleep
from threading import Thread
from todo_app import app
import pytest


def create_organization(api_key, token):
    response = requests.post('https://api.trello.com/1/organizations',
                             params={'displayName': "test", 'key': api_key, 'token': token}).json()
    return response['id']


def create_board(org_id, api_key, token):
    response = requests.post('https://api.trello.com/1/boards',
                             params={'idOrganization': org_id, 'name': "test", 'key': api_key, 'token': token}).json()
    return response['id']


def delete_board(board_id, api_key, token):
    requests.delete(f'https://api.trello.com/1/boards/{board_id}',
                    params={'key': api_key, 'token': token})


def delete_organization(org_id, api_key, token):
    requests.delete(f'https://api.trello.com/1/organizations/{org_id}',
                    params={'key': api_key, 'token': token})


@pytest.fixture(scope='module')
def app_with_temp_board():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    token = os.getenv("TOKEN")
    org_id = create_organization(api_key, token)
    board_id = create_board(org_id, api_key, token)
    os.environ['BOARD_ID'] = board_id
    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    sleep(1)
    yield application

    thread.join(1)
    delete_board(board_id, api_key, token)
    delete_organization(org_id, api_key, token)
