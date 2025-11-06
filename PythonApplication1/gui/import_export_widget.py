from PySide6.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QLabel,
                                 QPushButton, QFileDialog, QMessageBox, QWidget)
from datetime import datetime
import os


class ImportExportWidget(QDialog):
    """Компонент диалога импорта/экспорта, отделённый от основного файла."""

    def __init__(self, transaction_manager, parent=None):
        super().__init__(parent)
        self.transaction_manager = transaction_manager
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("📁 Импорт / Экспорт данных")
        self.setModal(True)
        self.setFixedSize(500, 380)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        export_group = QGroupBox("📤 Экспорт данных")
        export_layout = QVBoxLayout()
        info_label = QLabel(self.get_export_info())
        info_label.setWordWrap(True)
        export_layout.addWidget(info_label)

        btn_export_json = QPushButton("Экспорт в JSON файл")
        btn_export_json.clicked.connect(self.export_to_json)
        btn_export_backup = QPushButton("Создать резервную копию")
        btn_export_backup.clicked.connect(self.create_backup)
        export_layout.addWidget(btn_export_json)
        export_layout.addWidget(btn_export_backup)
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)

        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #d2b48c;")
        layout.addWidget(line)

        import_group = QGroupBox("📥 Импорт данных")
        import_layout = QVBoxLayout()
        warning_label = QLabel("⚠️ Внимание: Импорт данных перезапишет текущие транзакции!")
        warning_label.setWordWrap(True)
        import_layout.addWidget(warning_label)

        btn_import_json = QPushButton("Импорт из JSON файла")
        btn_import_json.clicked.connect(self.import_from_json)
        btn_import_backup = QPushButton("Восстановить из резервной копии")
        btn_import_backup.clicked.connect(self.restore_from_backup)
        import_layout.addWidget(btn_import_json)
        import_layout.addWidget(btn_import_backup)
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.setLayout(layout)

    def get_export_info(self):
        try:
            transactions = self.transaction_manager.get_all_transactions()
            total_count = len(transactions)
            if total_count == 0:
                return "📊 Нет данных для экспорта"
            income_count = sum(1 for t in transactions if t.get('amount', 0) > 0)
            expense_count = sum(1 for t in transactions if t.get('amount', 0) < 0)
            categories = len(set(t.get('category', '') for t in transactions))
            return f"""📊 Статистика данных:\n• Всего транзакций: {total_count}\n• Доходы: {income_count}\n• Расходы: {expense_count}\n• Уникальных категорий: {categories}"""
        except Exception:
            return "❌ Ошибка получения информации о данных"

    def export_to_json(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Экспорт данных в JSON",
            f"financial_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;All Files (*)"
        )
        if not file_path:
            return
        if not file_path.lower().endswith('.json'):
            file_path += '.json'
        success = self.transaction_manager.export_to_json(file_path)
        if success:
            QMessageBox.information(self, "Успех", f"✅ Данные успешно экспортированы в файл:\n{file_path}")

    def create_backup(self):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"backup_{timestamp}.json")
        success = self.transaction_manager.create_backup(backup_path)
        if success:
            QMessageBox.information(self, "Успех", f"✅ Резервная копия создана:\n{backup_path}")

    def import_from_json(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение импорта",
            "⚠️ Вы уверены, что хотите импортировать данные?\n\nВсе текущие транзакции будут заменены данными из файла.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Импорт данных из JSON", "", "JSON Files (*.json);;All Files (*)")
        if not file_path:
            return
        success, message = self.transaction_manager.import_from_json(file_path)
        if success:
            QMessageBox.information(self, "Успех", f"✅ Данные успешно импортированы!\n\n{message}")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", f"❌ Не удалось импортировать данные:\n{message}")

    def restore_from_backup(self):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            QMessageBox.information(self, "Информация", "Папка с резервными копиями не найдена.")
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите резервную копию для восстановления", backup_dir, "JSON Files (*.json);;All Files (*)")
        if not file_path:
            return
        reply = QMessageBox.question(self, "Подтверждение восстановления", f"⚠️ Вы уверены, что хотите восстановить данные из:\n{os.path.basename(file_path)}?\n\nВсе текущие транзакции будут заменены данными из резервной копии.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        success, message = self.transaction_manager.import_from_json(file_path)
        if success:
            QMessageBox.information(self, "Успех", f"✅ Данные успешно восстановлены!\n\n{message}")
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", f"❌ Не удалось восстановить данные:\n{message}")
