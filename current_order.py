from typing import List
from datetime import date
from extract_user_order import extract_items, extract_users, load_gsheet, BUY_EVENT_MARKER


class CurrentOrder:
    class __CurrentOrder:
        def __init__(self):
            self._table = None

        def set_table(self, url):
            """
            Return true if table has been successfully set
            False if was already been set
            """
            if self._table is None:
                self._table = load_gsheet(url)
                return True
            return False

        def clear_table(self):
            self._table = None

        def get_order(self, user_name):
            users = extract_users(self._table)
            items = extract_items(self._table)

            user_items = items[users[user_name] == BUY_EVENT_MARKER].tolist()
            return user_items

    instance = None

    def __init__(self, participants_list=List[str], start_index=0):
        if not self.instance:
            CurrentOrder.instance = self.__CurrentOrder()

    def __getattr__(self, name):
        return getattr(self.instance, name)
