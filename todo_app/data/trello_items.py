from todo_app.classes.item import Item
import requests
from os import getenv


# I decided to go for class design instead of an init method as then get_list_ids doesn't have to be called multiple times and doesn't over provide information
class TrelloClient:
    def __init__(self):
        self.board_id = getenv('BOARD_ID')
        self.api_key = getenv("API_KEY")
        self.token = getenv("TOKEN")
        self.auth_params = {"key": self.api_key, "token": self.token}
        self.base_api_url = 'https://api.trello.com/1'
        board_lists = requests.get(self.build_url(self.base_api_url, f'/boards/{self.board_id}/lists', {"fields": "name"})).json()
        for board_list in board_lists:
            board_name = board_list['name']
            if board_name == "To Do":
                self.to_do_list_id = board_list['id']
            elif board_name == "Done":
                self.done_list_id = board_list['id']
            elif board_name == "Doing":
                self.doing_list_id = board_list['id']
        self.list_names = {self.to_do_list_id: "To Do", self.done_list_id: "Done", self.doing_list_id: "Doing"}
        self.list_ids = {"To Do": self.to_do_list_id, "Done": self.done_list_id, "Doing": self.doing_list_id}

    def build_url(self, base_url, path, params={}):
        """
        Args:
            base_url: Base_url of request
            path: Path (beginning with / character)
            params: Parameters for the query excluding auth

        Returns:
            URL string with auth added
        """
        param_string = ""
        for key in params:
            param_string += f"{key}={params[key]}&"
        param_string += f'key={self.api_key}&token={self.token}'
        return f"{base_url}{path}?{param_string}"

    def get_items(self):
        """
        Fetches the saved items.

        Returns:
            items: All items from the trello board.
        """
        cards = requests.get(self.build_url(self.base_api_url, f'/boards/{self.board_id}/cards', {"fields": "name,idList,desc,due"})).json()
        items = [Item.from_trello_card(card, self.list_names[card['idList']]) for card in cards]
        return items

    def get_item(self, item_id):
        """
        Fetches the saved item with the specified ID.

        Args:
            item_id: The ID of the item.

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        items = self.get_items()
        return next((item for item in items if item.id == item_id), None)

    def add_item(self, title, desc, due_date):
        """
        Adds a new item with the specified title to the session.

        Args:
            title: The title of the item.
            desc: The description of the item
            due_date: Date due of item

        Returns:
            item: The saved item.
        """
        requests.post(self.build_url(self.base_api_url, '/cards', {"name": title, "desc": desc, "due": due_date, "idList": self.to_do_list_id}))

    def change_status(self, item_id, new_status):
        item = self.get_item(item_id)

        if item:
            new_list_id = self.list_ids[new_status]
            requests.put(self.build_url(self.base_api_url, f'/cards/{item_id}', {"idList": new_list_id})).json()

    def remove_item(self, item_id):
        """
        Removes the item with given id from the items in the session. If no existing item matched the ID, nothing is done.

        Args:
            item_id: The id of the item to delete
        """

        requests.delete(self.build_url(self.base_api_url, f'/cards/{item_id}'))
