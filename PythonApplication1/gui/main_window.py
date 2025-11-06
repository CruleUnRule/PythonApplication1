# ui/main_window.py
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QGroupBox, QLabel, QLineEdit, QComboBox, QDateEdit,
                               QListWidget, QPushButton, QMessageBox, QFormLayout,
                               QListWidgetItem, QDialog)
from PySide6.QtCore import QDate, Qt
from logic.transaction_manager import TransactionManager
from gui.edit_transaction_dialog import EditTransactionDialog
from gui.history_widget import HistoryWidget
from gui.import_export_widget import ImportExportWidget
from styles.style_manager import StyleManager
from validators.data_validator import DataValidator
import logging

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        try:
            super().__init__()
            self.transaction_manager = TransactionManager()
            self.style_manager = StyleManager()
            self.validator = DataValidator()
            self.current_filter = None
            
            self.init_ui()
            self.safe_initial_load()
            logger.info("Главное окно приложения успешно инициализировано")
            
        except Exception as e:
            logger.critical(f"Критическая ошибка инициализации приложения: {str(e)}")
            raise

    def safe_initial_load(self):
        """Безопасная первоначальная загрузка данных"""
        try:
            self.load_categories()
            self.load_transactions()
            logger.info("Первоначальная загрузка данных выполнена успешно")
        except Exception as e:
            logger.error(f"Ошибка первоначальной загрузки: {str(e)}")
            self.show_warning_message("Предупреждение", 
                                    "Не удалось загрузить начальные данные. Проверьте файл данных.")

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        try:
            self.setWindowTitle("💼 Менеджер финансов")
            self.setGeometry(100, 100, 1200, 800)

            self.apply_main_styles()

            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            main_layout = QHBoxLayout(central_widget)
            main_layout.setSpacing(20)
            main_layout.setContentsMargins(25, 25, 25, 25)

            self.create_left_panel(main_layout)
            self.create_right_panel(main_layout)

            logger.debug("Интерфейс главного окна создан успешно")

        except Exception as e:
            logger.error(f"Ошибка инициализации интерфейса: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось создать интерфейс приложения")
            raise

    def apply_main_styles(self):
        """Применение основных стилей приложения"""
        try:
            self.setStyleSheet(self.style_manager.get_main_window_style())
        except Exception as e:
            logger.error(f"Ошибка применения стилей: {str(e)}")
            self.setStyleSheet("QMainWindow { background-color: #f5f5dc; }")

    def create_left_panel(self, main_layout):
        """Создание левой панели управления"""
        try:
            left_panel = QVBoxLayout()
            left_panel.setSpacing(20)

            self.create_transaction_group(left_panel)
            self.create_filter_group(left_panel)
            self.create_additional_elements(left_panel)

            left_panel.addStretch()
            main_layout.addLayout(left_panel)

        except Exception as e:
            logger.error(f"Ошибка создания левой панели: {str(e)}")
            raise

    def create_transaction_group(self, parent_layout):
        """Создание группы для управления транзакциями"""
        try:
            transaction_group = QGroupBox("💳 Новая транзакция")
            transaction_layout = QFormLayout()
            transaction_layout.setSpacing(15)
            transaction_layout.setContentsMargins(15, 20, 15, 15)

            self.amount_input = QLineEdit()
            self.amount_input.setPlaceholderText("0.00")
            self.amount_input.textChanged.connect(self.validate_transaction_form)
            transaction_layout.addRow(QLabel("Сумма*:"), self.amount_input)

            self.category_input = QComboBox()
            self.category_input.setEditable(True)
            self.category_input.setInsertPolicy(QComboBox.InsertAtTop)
            self.category_input.lineEdit().setPlaceholderText("Выберите или введите категорию...")
            self.category_input.currentTextChanged.connect(self.validate_transaction_form)
            transaction_layout.addRow(QLabel("Категория*:"), self.category_input)

            self.date_input = QDateEdit()
            self.date_input.setDate(QDate.currentDate())
            self.date_input.setCalendarPopup(True)
            self.date_input.setDisplayFormat("dd.MM.yyyy")
            transaction_layout.addRow(QLabel("Дата:"), self.date_input)

            self.description_input = QLineEdit()
            self.description_input.setPlaceholderText("Необязательное описание...")
            transaction_layout.addRow(QLabel("Описание:"), self.description_input)

            self.create_transaction_buttons(transaction_layout)

            transaction_group.setLayout(transaction_layout)
            parent_layout.addWidget(transaction_group)

        except Exception as e:
            logger.error(f"Ошибка создания группы транзакций: {str(e)}")
            raise

    def create_transaction_buttons(self, layout):
        """Создание кнопок для управления транзакциями"""
        try:
            buttons_layout = QHBoxLayout()

            self.add_btn = QPushButton("💾 Добавить")
            self.add_btn.clicked.connect(self.safe_add_transaction)
            self.add_btn.setEnabled(False)
            buttons_layout.addWidget(self.add_btn)

            self.edit_btn = QPushButton("✏️ Редактировать")
            self.edit_btn.clicked.connect(self.safe_edit_transaction)
            buttons_layout.addWidget(self.edit_btn)

            self.delete_btn = QPushButton("🗑️ Удалить")
            self.delete_btn.clicked.connect(self.safe_delete_transaction)
            buttons_layout.addWidget(self.delete_btn)

            layout.addRow(buttons_layout)

        except Exception as e:
            logger.error(f"Ошибка создания кнопок транзакций: {str(e)}")
            raise

    def create_filter_group(self, parent_layout):
        """Создание группы фильтрации"""
        try:
            filter_group = QGroupBox("🔍 Фильтрация")
            filter_layout = QVBoxLayout()
            filter_layout.setSpacing(12)
            filter_layout.setContentsMargins(15, 20, 15, 15)

            filter_layout.addWidget(QLabel("Категория:"))
            self.filter_category = QComboBox()
            self.filter_category.addItem("Все категории")
            filter_layout.addWidget(self.filter_category)

            filter_buttons_layout = QHBoxLayout()

            self.filter_btn = QPushButton("Применить фильтр")
            self.filter_btn.clicked.connect(self.safe_apply_filter)
            filter_buttons_layout.addWidget(self.filter_btn)

            self.clear_filter_btn = QPushButton("Очистить")
            self.clear_filter_btn.clicked.connect(self.safe_clear_filter)
            filter_buttons_layout.addWidget(self.clear_filter_btn)

            filter_layout.addLayout(filter_buttons_layout)
            filter_group.setLayout(filter_layout)
            parent_layout.addWidget(filter_group)

        except Exception as e:
            logger.error(f"Ошибка создания группы фильтрации: {str(e)}")
            raise

    def create_additional_elements(self, parent_layout):
        """Создание дополнительных элементов интерфейса"""
        try:
            self.history_btn = QPushButton("📊 История транзакций")
            self.history_btn.clicked.connect(self.safe_show_history)
            parent_layout.addWidget(self.history_btn)

            self.import_export_btn = QPushButton("📁 Импорт / Экспорт")
            self.import_export_btn.clicked.connect(self.safe_show_import_export)
            parent_layout.addWidget(self.import_export_btn)

            parent_layout.addSpacing(20)

            balance_container = QHBoxLayout()
            self.balance_label = QLabel("Общий баланс: 0.00 руб.")
            self.balance_label.setStyleSheet("""
                QLabel {
                    font-size: 16pt;
                    font-weight: bold;
                    padding: 15px;
                    border-radius: 10px;
                    background-color: #ffffff;
                    border: 2px solid #d2b48c;
                }
            """)
            balance_container.addWidget(self.balance_label)
            parent_layout.addLayout(balance_container)

        except Exception as e:
            logger.error(f"Ошибка создания дополнительных элементов: {str(e)}")
            raise

    def create_right_panel(self, main_layout):
        """Создание правой панели со списками"""
        try:
            right_panel = QVBoxLayout()
            right_panel.setSpacing(15)

            self.create_categories_section(right_panel)
            self.create_transactions_section(right_panel)

            main_layout.addLayout(right_panel)

        except Exception as e:
            logger.error(f"Ошибка создания правой панели: {str(e)}")
            raise

    def create_categories_section(self, parent_layout):
        """Создание секции категорий"""
        try:
            categories_label = QLabel("📂 Категории:")
            parent_layout.addWidget(categories_label)

            self.categories_list = QListWidget()
            self.categories_list.setMaximumHeight(150)
            parent_layout.addWidget(self.categories_list)

        except Exception as e:
            logger.error(f"Ошибка создания секции категорий: {str(e)}")
            raise

    def create_transactions_section(self, parent_layout):
        """Создание секции транзакций"""
        try:
            transactions_label = QLabel("💰 Транзакции:")
            parent_layout.addWidget(transactions_label)

            self.transactions_list = QListWidget()
            self.transactions_list.setAlternatingRowColors(True)
            parent_layout.addWidget(self.transactions_list)

        except Exception as e:
            logger.error(f"Ошибка создания секции транзакций: {str(e)}")
            raise

    def validate_transaction_form(self):
        """Валидация формы транзакции в реальном времени"""
        try:
            amount_text = self.amount_input.text().strip()
            category = self.category_input.currentText().strip()

            is_valid = True

            # Валидация суммы
            amount_valid, amount_error = self.validator.validate_amount(amount_text)
            if not amount_valid and amount_text:  # Показываем ошибку только если поле не пустое
                self.set_field_error(self.amount_input, True, amount_error)
                is_valid = False
            else:
                self.set_field_error(self.amount_input, False)

            # Валидация категории
            if not category:
                is_valid = False
                self.set_field_error(self.category_input, True, "Категория обязательна")
            else:
                self.set_field_error(self.category_input, False)

            self.add_btn.setEnabled(is_valid)

        except Exception as e:
            logger.error(f"Ошибка валидации формы: {str(e)}")
            self.add_btn.setEnabled(False)

    def set_field_error(self, field, has_error, tooltip=""):
        """Установка состояния ошибки для поля ввода"""
        try:
            if has_error:
                field.setProperty("error", "true")
                field.setToolTip(tooltip)
            else:
                field.setProperty("error", "false")
                field.setToolTip("")

            field.style().unpolish(field)
            field.style().polish(field)

        except Exception as e:
            logger.error(f"Ошибка установки состояния поля: {str(e)}")

    def safe_add_transaction(self):
        """Безопасное добавление транзакции"""
        try:
            self.add_transaction()
        except Exception as e:
            logger.error(f"Ошибка добавления транзакции: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось добавить транзакцию")

    def safe_edit_transaction(self):
        """Безопасное редактирование транзакции"""
        try:
            self.edit_transaction()
        except Exception as e:
            logger.error(f"Ошибка редактирования транзакции: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось редактировать транзакцию")

    def safe_delete_transaction(self):
        """Безопасное удаление транзакции"""
        try:
            self.delete_transaction()
        except Exception as e:
            logger.error(f"Ошибка удаления транзакции: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось удалить транзакцию")

    def safe_apply_filter(self):
        """Безопасное применение фильтра"""
        try:
            self.apply_filter()
        except Exception as e:
            logger.error(f"Ошибка применения фильтра: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось применить фильтр")

    def safe_clear_filter(self):
        """Безопасная очистка фильтра"""
        try:
            self.clear_filter()
        except Exception as e:
            logger.error(f"Ошибка очистки фильтра: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось очистить фильтр")

    def safe_show_history(self):
        """Безопасное открытие окна истории"""
        try:
            self.show_history()
        except Exception as e:
            logger.error(f"Ошибка открытия истории: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось открыть окно истории")

    def safe_show_import_export(self):
        """Безопасное открытие диалога импорта/экспорта"""
        try:
            self.show_import_export()
        except Exception as e:
            logger.error(f"Ошибка открытия диалога импорта/экспорта: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось открыть диалог импорта/экспорта")

    def load_categories(self):
        """Загрузка категорий в комбобоксы"""
        try:
            categories = self.transaction_manager.get_categories()

            current_category = self.category_input.currentText()
            current_filter = self.filter_category.currentText()

            self.category_input.clear()
            self.filter_category.clear()
            self.filter_category.addItem("Все категории")

            for category in categories:
                self.category_input.addItem(category)
                self.filter_category.addItem(category)

            if current_category and self.category_input.findText(current_category) >= 0:
                self.category_input.setCurrentText(current_category)
            if current_filter and self.filter_category.findText(current_filter) >= 0:
                self.filter_category.setCurrentText(current_filter)

            logger.debug(f"Загружено {len(categories)} категорий")

        except Exception as e:
            logger.error(f"Ошибка загрузки категорий: {str(e)}")
            self.category_input.clear()
            self.filter_category.clear()
            self.filter_category.addItem("Все категории")

    def load_transactions(self):
        """Загрузка транзакций в список"""
        try:
            self.transactions_list.clear()

            transactions = self.transaction_manager.get_all_transactions()
            if not transactions:
                item = QListWidgetItem("Нет транзакций для отображения")
                item.setForeground(Qt.gray)
                self.transactions_list.addItem(item)
                self.update_balance()
                return

            successful_items = 0
            for transaction in transactions:
                try:
                    if not self.validator.is_valid_transaction_structure(transaction):
                        logger.warning(f"Пропущена некорректная транзакция: {transaction}")
                        continue

                    amount = transaction['amount']
                    category = transaction['category']
                    date = transaction['date']
                    description = transaction.get('description', '')

                    amount_str = f"+{amount:.2f}" if amount >= 0 else f"{amount:.2f}"
                    item_text = f"{date} | {category} | {amount_str} руб."
                    if description:
                        item_text += f" | {description}"

                    item = QListWidgetItem(item_text)

                    if amount > 0:
                        item.setForeground(Qt.darkGreen)
                    elif amount < 0:
                        item.setForeground(Qt.darkRed)
                    else:
                        item.setForeground(Qt.darkGray)

                    self.transactions_list.addItem(item)
                    successful_items += 1

                except Exception as item_error:
                    logger.error(f"Ошибка обработки транзакции {transaction}: {item_error}")
                    continue

            self.update_balance()
            self.update_categories_list()
            logger.info(f"Успешно загружено {successful_items} транзакций")

        except Exception as e:
            logger.error(f"Критическая ошибка загрузки транзакций: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось загрузить список транзакций")

    def update_balance(self):
        """Обновление отображения баланса"""
        try:
            balance = self.transaction_manager.calculate_balance()
            balance_text = f"Общий баланс: {balance:.2f} руб."

            if balance > 0:
                style = """
                    QLabel {
                        font-size: 16pt;
                        font-weight: bold;
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #e8f5e8;
                        border: 2px solid #4caf50;
                        color: #2e7d32;
                    }
                """
            elif balance < 0:
                style = """
                    QLabel {
                        font-size: 16pt;
                        font-weight: bold;
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffebee;
                        border: 2px solid #f44336;
                        color: #c62828;
                    }
                """
            else:
                style = """
                    QLabel {
                        font-size: 16pt;
                        font-weight: bold;
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #f5f5f5;
                        border: 2px solid #9e9e9e;
                        color: #616161;
                    }
                """

            self.balance_label.setText(balance_text)
            self.balance_label.setStyleSheet(style)

        except Exception as e:
            logger.error(f"Ошибка обновления баланса: {str(e)}")
            self.balance_label.setText("Ошибка расчета баланса")
            self.balance_label.setStyleSheet("color: red; font-weight: bold;")

    def update_categories_list(self):
        """Обновление списка категорий"""
        try:
            self.categories_list.clear()
            categories = self.transaction_manager.get_categories()

            for category in categories:
                self.categories_list.addItem(category)

        except Exception as e:
            logger.error(f"Ошибка обновления списка категорий: {str(e)}")
            self.categories_list.clear()
            self.categories_list.addItem("Ошибка загрузки категорий")

    def add_transaction(self):
        """Добавление новой транзакции"""
        try:
            amount_text = self.amount_input.text().strip()
            category = self.category_input.currentText().strip()
            date = self.date_input.date().toString("yyyy-MM-dd")
            description = self.description_input.text().strip()

            # Валидация данных
            is_valid, error_message = self.validator.validate_transaction_data(
                amount_text, category, date, description
            )
            
            if not is_valid:
                self.show_warning_message("Ошибка ввода", error_message)
                return

            amount = float(amount_text)

            self.transaction_manager.add_transaction(amount, category, date, description)

            self.amount_input.clear()
            self.description_input.clear()
            self.load_categories()
            self.load_transactions()

            self.show_info_message("Успех", "✅ Транзакция успешно добавлена")
            logger.info(f"Добавлена новая транзакция: {category} - {amount} руб.")

        except Exception as e:
            logger.error(f"Критическая ошибка добавления транзакции: {str(e)}")
            self.show_error_message("Ошибка", "❌ Не удалось добавить транзакцию")

    def edit_transaction(self):
        """Редактирование выбранной транзакции"""
        try:
            current_row = self.transactions_list.currentRow()
            if current_row == -1:
                self.show_warning_message("Предупреждение", "📝 Выберите транзакцию для редактирования")
                return

            transaction_data = self.transaction_manager.get_transaction_by_index(current_row)
            if not transaction_data:
                raise ValueError("Не удалось загрузить данные выбранной транзакции")

            categories = self.transaction_manager.get_categories()

            dialog = EditTransactionDialog(transaction_data, categories, self)
            if dialog.exec() == QDialog.Accepted:
                updated_data = dialog.get_updated_data()

                self.transaction_manager.update_transaction(current_row, updated_data)

                self.load_categories()
                self.load_transactions()

                self.show_info_message("Успех", "✅ Транзакция успешно обновлена")
                logger.info(f"Обновлена транзакция #{current_row}")

        except ValueError as ve:
            logger.warning(f"Ошибка валидации при редактировании: {str(ve)}")
            self.show_warning_message("Ошибка", str(ve))
        except Exception as e:
            logger.error(f"Критическая ошибка редактирования: {str(e)}")
            self.show_error_message("Ошибка", "❌ Не удалось обновить транзакцию")

    def delete_transaction(self):
        """Удаление выбранной транзакции"""
        try:
            current_row = self.transactions_list.currentRow()
            if current_row == -1:
                self.show_warning_message("Предупреждение", "🗑️ Выберите транзакцию для удаления")
                return

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                "❓ Вы уверены, что хотите удалить выбранную транзакцию?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.transaction_manager.delete_transaction(current_row)
                self.load_transactions()
                self.show_info_message("Успех", "✅ Транзакция успешно удалена")
                logger.info(f"Удалена транзакция #{current_row}")

        except Exception as e:
            logger.error(f"Ошибка удаления транзакции: {str(e)}")
            self.show_error_message("Ошибка", "❌ Не удалось удалить транзакцию")

    def apply_filter(self):
        """Применение фильтра по категории"""
        try:
            category = self.filter_category.currentText()
            if category == "Все категории":
                self.load_transactions()
                self.current_filter = None
            else:
                self.transactions_list.clear()
                transactions = self.transaction_manager.filter_by_category(category)

                if not transactions:
                    item = QListWidgetItem(f"Нет транзакций в категории '{category}'")
                    item.setForeground(Qt.gray)
                    self.transactions_list.addItem(item)
                    return

                for transaction in transactions:
                    try:
                        if not self.validator.is_valid_transaction_structure(transaction):
                            continue

                        amount = transaction['amount']
                        cat = transaction['category']
                        date = transaction['date']
                        description = transaction.get('description', '')

                        amount_str = f"+{amount:.2f}" if amount >= 0 else f"{amount:.2f}"
                        item_text = f"{date} | {cat} | {amount_str} руб."
                        if description:
                            item_text += f" | {description}"

                        item = QListWidgetItem(item_text)

                        if amount > 0:
                            item.setForeground(Qt.darkGreen)
                        elif amount < 0:
                            item.setForeground(Qt.darkRed)

                        self.transactions_list.addItem(item)

                    except Exception as item_error:
                        logger.error(f"Ошибка обработки отфильтрованной транзакции: {item_error}")
                        continue

                self.current_filter = category
                logger.info(f"Применен фильтр по категории: {category}")

        except Exception as e:
            logger.error(f"Ошибка применения фильтра: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось применить фильтр")

    def clear_filter(self):
        """Очистка фильтров"""
        try:
            self.filter_category.setCurrentIndex(0)
            self.load_transactions()
            self.current_filter = None
            logger.info("Фильтры очищены")

        except Exception as e:
            logger.error(f"Ошибка очистки фильтра: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось очистить фильтр")

    def show_history(self):
        """Открытие окна истории транзакций"""
        try:
            self.history_window = HistoryWidget(self.transaction_manager, self)
            self.history_window.exec()
            logger.info("Окно истории транзакций закрыто")

        except Exception as e:
            logger.error(f"Ошибка открытия окна истории: {str(e)}")
            self.show_error_message("Ошибка", "Не удалось открыть окно истории транзакций")

    def show_import_export(self):
        """Открытие диалога импорта/экспорта данных"""
        try:
            dialog = ImportExportWidget(self.transaction_manager, self)
            result = dialog.exec()

            if result == QDialog.Accepted:
                self.load_categories()
                self.load_transactions()
                self.show_info_message("Успех", "✅ Данные успешно обновлены")

        except Exception as e:
            logger.error(f"Ошибка в диалоге импорта/экспорта: {str(e)}")
            self.show_error_message("Ошибка", "Произошла ошибка при работе с данными")

    def show_error_message(self, title, message):
        """Показать сообщение об ошибке"""
        QMessageBox.critical(self, title, message)
        logger.error(f"{title}: {message}")

    def show_warning_message(self, title, message):
        """Показать предупреждение"""
        QMessageBox.warning(self, title, message)
        logger.warning(f"{title}: {message}")

    def show_info_message(self, title, message):
        """Показать информационное сообщение"""
        QMessageBox.information(self, title, message)
        logger.info(f"{title}: {message}")