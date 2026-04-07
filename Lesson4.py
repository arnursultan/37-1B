# import sqlite3
#
# conn = sqlite3.connect("academy.db")
#
# cursor = conn.cursor()
#
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS students (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER,
#         city TEXT
#     )
# """)
#
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("Азиза", 18, "Ош")
# )
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("Ислам", 18, "Ош")
# )
# cursor.execute(
#     "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
#     ("АБдуллох", 18, "Ош")
# )
#
# conn.commit()
#
# cursor.execute("SELECT * FROM students")
# rows = cursor.fetchall()
#
# print("Все студенты:")
# for row in rows:
#     print(row)
# conn.close()

import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QMessageBox
)

class Database:
    def __init__(self, path="geeks.db"):
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        self._init()

    def _init(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                city TEXT
            )
        """)
        self.cursor.execute("SELECT COUNT(*) FROM students")
        if self.cursor.fetchone()[0] == 0:
            data = [
                ("Ажибек", 22, "Ош"),
                ("Тимур", 22, "Бишкек"),
                ("Эмили", 19, "Москва"),
            ]
            self.cursor.executemany(
                "INSERT INTO students (name, age, city) VALUES (?, ?, ?)", data
            )
            self.conn.commit()

    def get_all(self)
        self.cursor.execute("SELECT * FROM students ORDER BY id")
        return self.cursor.fetchall()

    def add(self, name, age, city):
        self.cursor.execute(
            "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
            (name, age, city)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle("Студенты - база данных")
        self.resize(600, 480)
        self.init_ui()
        self.load_data()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContensMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Список студентов:"))

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Имя", "Возраст", "Город"])
        self.table.setEditTriggers(
            QTableWidget.EditTriggers.NoEditTriggers
        )
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)

        layout.addWidget(QLabel("Добавить студента:"))
        form_layout = QHBoxLayout()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("")