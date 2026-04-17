import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QComboBox, QSpinBox, QMessageBox, QHeaderView, QFrame, QCheckBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import GameDatabase

STATUS_COLORS={
    "Играю": "d4edda", # Светло-зелёный
    "Пройдено": "cce5ff", #Светло-голубой
    "Хочу играть": "fff3cd", #Светло-жёлтый
    "Брошено": "f8d7da", #Светло-розовый или бледно-красный
}

class GameVault(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = GameDatabase()
        self.setWindowTitle("Моя библиотека игр")
        self.resize(900, 600)
        self.init_ui()
        self.load_table()
        self.update_stats()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        root.addLayout(self._build_header())

        root.addLayout(self._build_filters())

        root.addLayout(self._build_table())

        root.addLayout(self._build_divider("Добавить игру"))
        root.addLayout(self._build_add_form())

    def _build_header(self):
        layout = QHBoxLayout()
        title = QLabel("GameVault")
        title.setStyleSheet("font-size:20px; font-weight: bold")
        layout.addWidget(title)
        layout.addStretch()

        self.lbl_total = QLabel()
        self.lbl_hours = QLabel()
        self.lbl_completed = QLabel()
        self.lbl_avg = QLabel()

        for lbl in [self.lbl_total, self.lbl_hours, self.lbl_completed, self.lbl_avg]:
            lbl.setStyleSheet(
                "background:#f0f0f0; padding:4px 10px, border-radius:8px;"
                "font-size:12px;"
            ) ##f0f0f0 — очень светло-серый
            layout.addWidget(lbl)

        return layout

    def _build_filters(self) -> QHBoxLayout:
        layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию")
        self.search.input.textChanged.connect(self.on_search)

        self.filter_status = QComboBox()
        self.filter_status.addItem("Все статусы")
        self.filter_status.addItems(GameDatabase.STATUSES)
        self.filter_status.currentTextChanged.connect(self.on_filter)

        self.filter_genre = QComboBox()
        self.filter_genre.addItem("Все жанры")
        self.filter_genre.addItems(GameDatabase.GENRES)
        self.filter_genre.currentTextChanged.connect(self.on_filter)

        btn_reset = QPushButton("Сбросить")
        btn_reset.clicked.connect(self.reset_filters)

        layout.addWidget(QLabel("Поиск:"))
        layout.addWidget(self.search_input, 2)
        layout.addWidget(QLabel("Статус:"))
        layout.addWidget(self.filter_status)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(btn_reset)

        return layout

    def _build_table(self) -> QTableWidget:
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Название", "Жанр", "Рейтинг", "Статус", "Часов"]
        )
        self.table.setEditTriggers(QTableWidget.EditTriggers.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRowsBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(5, 70)

        self.table.doubleClicked.connect(self.on_double_click)
        return self.table

    def _build_add_form(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        self.inp_title = QLineEdit()
        self.inp_title.setPlaceholderText("Название игры")

        self.inp_genre = QComboBox()
        self.inp_genre.addItems(GameDatabase.GENRES)

        self.inp_rating = QSpinBox()
        self.inp_rating.setRange(1, 10)
        self.inp_rating.setValue(7)
        self.inp_rating.setPrefix("★")

        self.inp_status = QComboBox()
        self.inp_status.addItems(GameDatabase.STATUSES)

        self.inp_hours = QSpinBox()
        self.inp_hours.setRange(0,99999)
        self.inp_hours.setSuffix(" ч")

        btn_add = QPushButton("Добавить")
        btn_add.setStyleSheet(
            "background:#4CAF50; color:white; font-weight:bold;"
            "padding: 6px 14px, border-radius:6px;"
        ) #4CAF50 - зеленый

        btn_add.clicked.connect(self.add_game)

        btn_del = QPushButton("Удалить")
        btn_del.setStyleSheet(
            "background:#e53935"
        ) #e53935 - насыщенный тёплый оттенок красного цвета







