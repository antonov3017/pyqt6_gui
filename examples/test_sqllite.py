import sqlite3

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('example.db')

# Создаем курсор для выполнения SQL-команд
cursor = conn.cursor()
#
# # Создаем таблицу contracts
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS contracts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     contract_name TEXT NOT NULL,
#     client_name TEXT NOT NULL,
#     start_date TEXT NOT NULL,
#     end_date TEXT NOT NULL
# )
# ''')
#
# # Создаем таблицу invoices, которая ссылается на contracts
# cursor.execute('''
# CREATE TABLE IF NOT EXISTS invoices (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     invoice_number TEXT NOT NULL,
#     amount REAL NOT NULL,
#     contract_id INTEGER,
#     FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
# )
# ''')
#
# # Добавим несколько тестовых данных в таблицу contracts
# cursor.execute("INSERT INTO contracts (contract_name, client_name, start_date, end_date) VALUES ('Contract A', 'Client 1', '2024-01-01', '2024-12-31')")
# cursor.execute("INSERT INTO contracts (contract_name, client_name, start_date, end_date) VALUES ('Contract B', 'Client 2', '2024-02-01', '2024-08-31')")
# cursor.execute("INSERT INTO contracts (contract_name, client_name, start_date, end_date) VALUES ('Contract C', 'Client 3', '2024-03-01', '2024-09-30')")

# Добавим несколько тестовых данных в таблицу invoices
cursor.execute("INSERT INTO invoices (invoice_number, amount, contract_id) VALUES ('INV001', 1000.00, 3)")
cursor.execute("INSERT INTO invoices (invoice_number, amount, contract_id) VALUES ('INV002', 2000.00, 3)")
cursor.execute("INSERT INTO invoices (invoice_number, amount, contract_id) VALUES ('INV003', 1500.00, 3)")

# Зафиксируем изменения и закроем соединение
conn.commit()
conn.close()

print("База данных создана, и данные добавлены.")
