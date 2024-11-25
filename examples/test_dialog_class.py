import sys
from PyQt6 import QtWidgets as qtw, QtSql
from PyQt6.QtCore import Qt
from PyQt6 import QtCore, QtGui, QtWidgets



class ValueInputDialog(object):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Введите значение")

        self.layout = qtw.QVBoxLayout(self)

        self.line_edit = qtw.QLineEdit(self)

        self.layout.addWidget(self.line_edit)

        self.button_box = qtw.QDialogButtonBox(self)
        self.button_box.setStandardButtons(
            qtw.QDialogButtonBox.StandardButton.Ok | qtw.QDialogButtonBox.StandardButton.Cancel)
        self.layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_value(self):
        return self.line_edit.text()

class DateDialog(qtw.QDialog, ValueInputDialog):
    def __init__(self, current_value):
        super().__init__()

        self.line_edit.setText(current_value)  # Устанавливаем текущее значение



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
        self.contracts_view.setRowCount(self.contracts_model.rowCount())  # Устанавливаем количество строк
        self.contracts_view.setColumnCount(self.contracts_model.columnCount())  # Устанавливаем количество столбцов
        # Отключаем отображение номеров строк
        self.contracts_view.verticalHeader().setVisible(False)

        # Заполнение QTableWidget данными из модели
        for row in range(self.contracts_model.rowCount()):
            for column in range(self.contracts_model.columnCount()):
                item_data = self.contracts_model.data(self.contracts_model.index(row, column))
                if column == 5:  # Если это логическое значение
                    item = qtw.QTableWidgetItem()
                    item.setCheckState(Qt.CheckState.Checked if item_data else Qt.CheckState.Unchecked)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)  # Делаем элемент чекбоксом
                else:
                    item = qtw.QTableWidgetItem(str(item_data))  # Для остальных значений

                # Запрет редактирования 4 колонки (индекс 3)
                if column == 3:  # Если это четвертая колонка
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Убираем флаг редактирования

                self.contracts_view.setItem(row, column, item)

        self.invoices_model = QtSql.QSqlTableModel(self)
        self.invoices_model.setTable('invoices')
        self.invoices_model.select()

        self.invoices_view = qtw.QTableView(self)
        self.invoices_view.setModel(self.invoices_model)

        # Устанавливаем связь
        self.contracts_view.itemSelectionChanged.connect(self.on_contract_selected)
        self.contracts_view.cellDoubleClicked.connect(self.on_cell_double_clicked)

        # Компоновка интерфейса
        layout = qtw.QVBoxLayout(self)
        layout.addWidget(self.contracts_view)
        layout.addWidget(self.invoices_view)
        self.setLayout(layout)

        self.resize(800, 500)
        # Центрирование окна на экране
        self.center()

    def center(self):
        # Получаем доступный экран
        screen = qtw.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Получаем размеры окна
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def on_contract_selected(self):
        # Получаем выбранный договор
        selected_indexes = self.contracts_view.selectedIndexes()
        if selected_indexes:
            contract_id = self.contracts_model.data(
                selected_indexes[0])  # Предполагается, что ID договора в первой колонке
            self.load_invoices_for_contract(contract_id)

    def load_invoices_for_contract(self, contract_id):
        # Фильтруем счета по выбранному договору
        self.invoices_model.setFilter(
            f'contract_id = {contract_id}')  # Предполагается, что contract_id - это ID внешнего ключа
        self.invoices_model.select()

    def on_cell_double_clicked(self, row, column):
        if column == 3:  # Проверяем, что это 4 колонка
            current_value = self.contracts_view.item(row, column).text()  # Получаем текущее значение ячейки

            dialog = DateDialog(current_value)  # Создаем диалог с текущим значением
            if dialog.exec() == qtw.QDialog.DialogCode.Accepted:  # Проверяем, нажал ли пользователь "ОК"
                new_value = dialog.get_value()  # Получаем новое значение из диалога
                self.update_value(row, column, new_value)  # Обновляем значение ячейки

    def update_value(self, row, column, new_value):
        self.contracts_view.item(row, column).setText(new_value)
        # Здесь можно добавить код для сохранения в базе данных, если это нужно


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
