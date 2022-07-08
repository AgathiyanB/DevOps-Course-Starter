from todo_app.data.item import Item
import requests
from os import getenv

board_id = getenv('BOARD_ID')
api_key = getenv("API_KEY")
token = getenv("TOKEN")
auth_params = f'key={api_key}&token={token}'

board_lists = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists?fields=name&{auth_params}').json()
for board_list in board_lists:
    if board_list['name'] == "To Do":
        to_do_list_id = board_list['id']
    elif board_list['name'] == "Done":
        done_list_id = board_list['id']

list_names = {to_do_list_id: "To Do", done_list_id: "Done"}


def get_items():
    cards = requests.get(f'https://api.trello.com/1/boards/{board_id}/cards?fields=name,idList&{auth_params}').json()
    items = [Item(item['id'], item['name'], list_names[item['idList']]) for item in cards]
    return items


def get_item(item_id):
    """
    Fetches the saved item with the specified ID.

    Args:
        item_id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item.id == item_id), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """

    requests.post(f'https://api.trello.com/1/cards?name={title}&idList={to_do_list_id}&{auth_params}')


def change_status(item_id):
    item = get_item(item_id)

    if item:
        new_list_id = to_do_list_id if item.status == "Done" else done_list_id
        requests.put(f"https://api.trello.com/1/cards/{item_id}?idList={new_list_id}&{auth_params}").json()


def remove_item(item_id):
    """
    Removes the item with given id from the items in the session. If no existing item matched the ID, nothing is done.

    Args:
        item_id: The id of the item to delete
    """

    requests.delete(f"https://api.trello.com/1/cards/{item_id}?{auth_params}")