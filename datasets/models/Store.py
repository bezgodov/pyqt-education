class Store():
    current_tab = 0
    tabs = []

    @staticmethod
    def set_current_tab(acitve_tab):
        Store.current_tab = acitve_tab

    @staticmethod
    def get_current_tab():
        return Store.tabs[Store.current_tab]

    @staticmethod
    def add_tab(tab):
        Store.tabs.append(tab)

    @staticmethod
    def set_last_row(tab, value):
        tab['last_row_loaded'] = value
        # Store.tabs[tab]['last_row_loaded'] = value
