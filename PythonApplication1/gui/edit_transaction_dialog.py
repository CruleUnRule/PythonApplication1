from PySide6.QtWidgets import (QDialog, QFormLayout, QLabel, QLineEdit, 
                               QComboBox, QDateEdit, QDialogButtonBox)
from PySide6.QtCore import QDate
from gui.base_dialog import BaseDialog
from validators.data_validator import DataValidator
import logging

logger = logging.getLogger(__name__)

class EditTransactionDialog(BaseDialog):
    def __init__(self, transaction_data, categories, parent=None):
        super().__init__(parent)
        self.transaction_data = transaction_data
        self.categories = categories
        self.init_ui()
        self.load_transaction_data()

    def init_ui(self):
        self.setWindowTitle("Редактирование транзакции")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.apply_styles()

        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.create_input_fields(layout)
        self.create_action_buttons(layout)
        self.setLayout(layout)

    def create_input_fields(self, layout):
        self.amount_edit = QLineEdit()
        self.amount_edit.textChanged.connect(self.validate_amount)
        layout.addRow(QLabel("Сумма*:"), self.amount_edit)

        self.category_edit = QComboBox()
        self.category_edit.setEditable(True)
        if self.categories:
            self.category_edit.addItems(self.categories)
        layout.addRow(QLabel("Категория*:"), self.category_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        layout.addRow(QLabel("Дата:"), self.date_edit)

        self.description_edit = QLineEdit()
        layout.addRow(QLabel("Описание:"), self.description_edit)

    def create_action_buttons(self, layout):
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def load_transaction_data(self):
        # Реализация загрузки данных
        try:
            if not self.transaction_data:
                return

            amount = self.transaction_data.get('amount', 0)
            category = self.transaction_data.get('category', '')
            date_str = self.transaction_data.get('date', '')
            description = self.transaction_data.get('description', '')

            self.amount_edit.setText(f"{amount}")
            if category and self.category_edit.findText(category) >= 0:
                self.category_edit.setCurrentText(category)
            else:
                self.category_edit.setCurrentText(category)

            try:
                if date_str:
                    parts = date_str.split('-')
                    if len(parts) == 3:
                        y, m, d = map(int, parts)
                        self.date_edit.setDate(QDate(y, m, d))
            except Exception:
                pass

            self.description_edit.setText(description)
        except Exception as e:
            logger.error(f"Ошибка загрузки данных транзакции в диалог: {e}")

    def validate_amount(self):
        # Простая валидация суммы
        text = self.amount_edit.text().strip()
        try:
            if text == '':
                self.set_field_error(self.amount_edit, False)
                return
            float(text)
            self.set_field_error(self.amount_edit, False)
        except ValueError:
            self.set_field_error(self.amount_edit, True, "Некорректная сумма")

    def validate_and_accept(self):
        # Валидация перед принятием
        amount_text = self.amount_edit.text().strip()
        category = self.category_edit.currentText().strip()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        description = self.description_edit.text().strip()

        is_valid, error = self.validator.validate_transaction_data(amount_text, category, date, description)
        if not is_valid:
            self.show_warning_message("Ошибка ввода", error)
            return

        self.accept()

    def get_updated_data(self):
        try:
            amount = float(self.amount_edit.text().strip())
        except Exception:
            amount = 0.0

        return {
            'amount': amount,
            'category': self.category_edit.currentText().strip(),
            'date': self.date_edit.date().toString("yyyy-MM-dd"),
            'description': self.description_edit.text().strip()
        }