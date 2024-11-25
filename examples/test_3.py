import sys
from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt

class MyApp(qtw.QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем соединение с базой данных
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('example.db')
        if not self.db.open():
            print("Could not open database")
            return

        # Создаем модели для таблиц
        self.contracts_model = QtSql.QSqlTableModel(self)
        self.contracts_model.setTable('contracts')
        self.contracts_model.select()

        self.contracts_view = qtw.QTableWidget(self)
        self.contracts_view.setRowCount(0)  # Сбрасываем количество строк
        self.contracts_view.setColumnCount(
            self.contracts_model.columnCount())  # Устанавливаем количество столбцов

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            self.contracts_view.insertRow(row)  # Вставляем новую строку
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))
                if isinstance(item_data, bool):  # Если это логическое значение
                    item = qtw.QTableWidgetItem()
                    item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Делаем элемент чекбоксом
                else:
                    item = qtw.QTableWidgetItem(str(item_data))  # Для остальных значений

        self.contracts_view.setItem(row, column, item)

        self.invoices_model = QtSql.QSqlTableModel(self)
        self.invoices_model.setTable('invoices')
        self.invoices_model.select()

        # Создаем таблицы для отображения данных
        # self.contracts_view = QtWidgets.QTableView(self)
        # self.contracts_view.setModel(self.contracts_model)

        self.invoices_view = qtw.QTableView(self)
        self.invoices_view.setModel(self.invoices_model)

        # Устанавливаем связь
        self.contracts_view.selectionModel().selectionChanged.connect(self.on_contract_selected)

        # Компоновка интерфейса
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.contracts_view)
        layout.addWidget(self.invoices_view)
        self.setLayout(layout)

    def on_contract_selected(self):
        # Получаем выбранный договор
        selected_indexes = self.contracts_view.selectedIndexes()
        if selected_indexes:
            contract_id = self.contracts_model.data(selected_indexes[0])  # Предполагается, что ID договора в первой колонке
            self.load_invoices_for_contract(contract_id)

    def load_invoices_for_contract(self, contract_id):
        # Фильтруем счета по выбранному договору
        self.invoices_model.setFilter(f'contract_id = {contract_id}')  # Предполагается, что contract_id - это ID внешнего ключа
        self.invoices_model.select()

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
