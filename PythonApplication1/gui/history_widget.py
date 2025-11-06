# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                                 QLineEdit, QListWidget, QPushButton, QListWidgetItem)
from PySide6.QtCore import Qt


class HistoryWidget(QDialog):
    """Компонент окна истории транзакций: поиск, список и кнопки."""

    def __init__(self, transaction_manager, parent=None):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self._init_ui()
        self.load_transactions()

    def _init_ui(self):
        self.setWindowTitle("📊 История транзакций")
        self.setGeometry(250, 250, 900, 600)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        search_layout = QHBoxLayout()
        search_label = QLabel(self.tr("🔍 Поиск:"))
        search_label.setFixedWidth(80)
        search_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(self.tr("Введите текст для поиска по категории или описанию..."))
        self.search_input.textChanged.connect(self.search_transactions)
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        self.transactions_list = QListWidget()
        self.transactions_list.setAlternatingRowColors(True)
        layout.addWidget(self.transactions_list)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.refresh_btn = QPushButton(self.tr("🔄 Обновить"))
        self.close_btn = QPushButton(self.tr("❌ Закрыть"))
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.refresh_btn.clicked.connect(self.load_transactions)
        self.close_btn.clicked.connect(self.close)

    def is_valid_transaction(self, transaction):
        if not isinstance(transaction, dict):
            return False
        if 'amount' not in transaction or 'category' not in transaction or 'date' not in transaction:
            return False
        if not isinstance(transaction['amount'], (int, float)):
            return False
        return True

    def load_transactions(self):
        self.transactions_list.clear()
        transactions = self.transaction_manager.get_all_transactions()
        if not transactions:
            it = QListWidgetItem(self.tr("Нет транзакций для отображения"))
            it.setForeground(Qt.gray)
            self.transactions_list.addItem(it)
            return

        for t in transactions:
            if not self.is_valid_transaction(t):
                continue
            amount = t['amount']
            cat = t['category']
            date = t['date']
            desc = t.get('description', '')
            amount_str = f"+{amount:.2f}" if amount >= 0 else f"{amount:.2f}"
            text = f"{date} | {cat:<15} | {amount_str:>10} руб."
            if desc:
                text += f" | {desc}"
            it = QListWidgetItem(text)
            if amount > 0:
                it.setForeground(Qt.darkGreen)
            elif amount < 0:
                it.setForeground(Qt.darkRed)
            self.transactions_list.addItem(it)

    def search_transactions(self):
        text = self.search_input.text().lower().strip()
        if not text:
            self.load_transactions()
            return
        self.transactions_list.clear()
        for t in self.transaction_manager.search_transactions(text):
            if not self.is_valid_transaction(t):
                continue
            amount = t['amount']
            cat = t['category']
            date = t['date']
            desc = t.get('description', '')
            amount_str = f"+{amount:.2f}" if amount >= 0 else f"{amount:.2f}"
            text = f"{date} | {cat:<15} | {amount_str:>10} руб."
            if desc:
                text += f" | {desc}"
            it = QListWidgetItem(text)
            if amount > 0:
                it.setForeground(Qt.darkGreen)
            elif amount < 0:
                it.setForeground(Qt.darkRed)
            self.transactions_list.addItem(it)
