class Store():
    current_tab = 0
    tabs = []
    app = None

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

    @staticmethod
    def show_message_in_status_bar(message):
        Store.app.statusBar().showMessage(message)
