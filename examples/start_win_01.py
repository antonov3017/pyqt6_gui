import sys
from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt

from examples.view.main_window import Ui_MainWindow


class StartWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('example.db')

        if not self.db.open():
            print("Could not open database")
            return

        self.tbl_contracts_view()
        self.tableWidget_Contracts.itemSelectionChanged.connect(self.on_contract_selected)

    def tbl_contracts_view(self):
        """ Инициализация таблицы с данными без фильтрации. """
        # Создаем модели для таблиц
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts')
        self.contracts_model.select()

        self.update_table()

    def update_table(self):
        self.tableWidget_Contracts.setRowCount(self.contracts_model.rowCount())
        self.tableWidget_Contracts.setColumnCount(self.contracts_model.columnCount())

        for row in range(self.contracts_model.rowCount()):
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))
                item = qtw.QTableWidgetItem(
                    str(item_data)) if column != 5 else qtw.QTableWidgetItem()
                if column == 5:  # If this is a boolean value
                    item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Checkbox
                else:
                    if column == 3:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make non-editable
                self.tableWidget_Contracts.setItem(row, column, item)

    def on_contract_selected(self):
        # Получаем выбранные индексы
        selected_indexes = self.tableWidget_Contracts.selectedIndexes()
        if selected_indexes:
            # Получаем строку из первого выбранного индекса
            row = selected_indexes[0].row()
            # Предполагаем, что ID договора находится в 0 столбце
            contract_id = self.contracts_model.data(self.contracts_model.index(row, 0))
            self.load_selected_contract(contract_id)

    def load_selected_contract(self, contract_id):
        print(contract_id)
        # Инициализация модели для выбранного контракта
        self.selected_contract_model = QtSql.QSqlTableModel(self)
        self.selected_contract_model.setTable('contracts')

        # Установка фильтра по contract_id
        self.selected_contract_model.setFilter(f"id = {contract_id}")
        self.selected_contract_model.select()  # Это загрузит данные согласно фильтру

        # Проверка на ошибки после выполнения запроса
        if self.selected_contract_model.lastError().isValid():
            print("Ошибка запроса:", self.selected_contract_model.lastError().text())
            return

        # Обновление данных
        if self.selected_contract_model.rowCount() > 0:
            print(f'{self.selected_contract_model.rowCount()=}')
            # Установка данных в поля с дополнительными проверками
            def get_data(col):
                if self.selected_contract_model.data(self.selected_contract_model.index(0, col)) is not None:
                    return str(self.selected_contract_model.data(self.selected_contract_model.index(0, col)))
                return ""

            self.lineEdit_ContractNumber.setText(get_data(0))
            self.lineEdit_ContractRemaks.setText(get_data(1))
            self.lineEdit_ContractDate.setText(get_data(2))
            self.lineEdit_ContractDateStart.setText(get_data(3))  # Начало договора
            self.lineEdit_ContractDateEnd.setText(get_data(4))    # Конец договора
        else:
            print(f"Нет данных для contract_id: {contract_id}.")


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = StartWindow()
    window.show()
    window.showMaximized()

    sys.exit(app.exec())
