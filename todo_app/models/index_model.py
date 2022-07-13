from operator import attrgetter


class IndexModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return sorted(self._items, key=attrgetter('status'), reverse=True)

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == "Doing"]

