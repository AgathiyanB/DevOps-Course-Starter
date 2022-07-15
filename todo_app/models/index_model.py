from operator import attrgetter


class IndexModel:
    def __init__(self, items):
        self._items = items

    @property
    def doing_items(self):
        return self._find_items_by_status("Doing")

    @property
    def to_do_items(self):
        return self._find_items_by_status("To Do")

    @property
    def done_items(self):
        return self._find_items_by_status("Done")

    def _find_items_by_status(self, status):
        return [item for item in self._items if item.status == status]
