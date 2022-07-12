class Item:
    def __init__(self, item_id, title, desc, due_date, status='Not Started'):
        self.id = item_id
        self.title = title
        self.status = status
        self.desc = desc
        self.due_date = due_date

    @classmethod
    def from_trello_card(cls, card, list_name):
        # Taking the first 10 characters of 'due' is a result of the ISO 8601 datetime return of the Trello API
        due_date = card['due'][:10] if card['due'] else "None"
        desc = card['desc'] if len(card['desc']) > 0 else "No description"
        return Item(card['id'], card['name'], desc, due_date, list_name)