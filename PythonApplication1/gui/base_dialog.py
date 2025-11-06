# ui/base_dialog.py
from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt
import logging
from styles.style_manager import StyleManager
from validators.data_validator import DataValidator

logger = logging.getLogger(__name__)

class BaseDialog(QDialog):
    """Базовый класс для всех диалоговых окон"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.style_manager = StyleManager()
        self.validator = DataValidator()
    
    def apply_styles(self):
        """Применение стилей к диалогу"""
        try:
            self.setStyleSheet(self.style_manager.get_dialog_style())
        except Exception as e:
            logger.error(f"Ошибка применения стилей: {str(e)}")
            self.setStyleSheet("QDialog { background-color: #f5f5dc; }")
    
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
    
    def safe_execute(self, operation, error_title="Ошибка"):
        """
        Безопасное выполнение операции с обработкой исключений
        
        Args:
            operation: Функция для выполнения
            error_title: Заголовок ошибки
            
        Returns:
            Результат операции или None при ошибке
        """
        try:
            return operation()
        except Exception as e:
            self.show_error_message(error_title, f"Неожиданная ошибка: {str(e)}")
            logger.error(f"{error_title}: {str(e)}")
            return None