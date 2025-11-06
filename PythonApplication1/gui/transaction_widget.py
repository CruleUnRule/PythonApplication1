from PySide6.QtWidgets import (QGroupBox, QFormLayout, QLineEdit, QComboBox,
                                 QDateEdit, QHBoxLayout, QPushButton)
from PySide6.QtCore import QDate


class TransactionWidget(QGroupBox):
    """Виджет для ввода новой транзакции (группа с полями и кнопками)."""

    def __init__(self, parent=None):
        super().__init__("💳 Новая транзакция", parent)
        self._init_ui()

    def _init_ui(self):
        layout = QFormLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(10, 12, 10, 12)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("0.00")
        layout.addRow(self.tr("Сумма*:"), self.amount_input)

        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.setInsertPolicy(QComboBox.InsertAtTop)
        self.category_input.lineEdit().setPlaceholderText(self.tr("Выберите или введите категорию..."))
        layout.addRow(self.tr("Категория*:"), self.category_input)

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd.MM.yyyy")
        layout.addRow(self.tr("Дата:"), self.date_input)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText(self.tr("Необязательное описание..."))
        layout.addRow(self.tr("Описание:"), self.description_input)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("💾 Добавить")
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.delete_btn = QPushButton("🗑️ Удалить")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addRow(btn_layout)

        self.setLayout(layout)

    def get_transaction_data(self):
        """Вернуть словарь с данными из полей (строки)"""
        return {
            'amount_text': self.amount_input.text().strip(),
            'category': self.category_input.currentText().strip(),
            'date': self.date_input.date().toString("yyyy-MM-dd"),
            'description': self.description_input.text().strip()
        }

    def clear(self):
        self.amount_input.clear()
        self.description_input.clear()

    def set_categories(self, categories):
        """Обновляет список категорий в поле выбора"""
        current = self.category_input.currentText()
        self.category_input.clear()
        for c in categories:
            self.category_input.addItem(c)
        if current and self.category_input.findText(current) >= 0:
            self.category_input.setCurrentText(current)

