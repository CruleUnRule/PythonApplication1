# main.py
import sys
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from gui.main_window import MainWindow

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('financial_manager.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class FinancialManagerApp:
    """Главный класс приложения менеджера финансов"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
    
    def setup_application(self):
        """Настройка приложения"""
        try:
            # Установка атрибутов приложения
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
            
            self.app = QApplication(sys.argv)
            self.app.setApplicationName("Менеджер финансов")
            self.app.setApplicationVersion("1.0.0")
            self.app.setOrganizationName("FinancialSoft")
            
            # Установка стиля по умолчанию
            self.app.setStyle('Fusion')
            
            logger.info("Приложение успешно настроено")
            
        except Exception as e:
            logger.critical(f"Ошибка настройки приложения: {str(e)}")
            raise
    
    def create_main_window(self):
        """Создание главного окна"""
        try:
            self.main_window = MainWindow()
            logger.info("Главное окно создано")
            
        except Exception as e:
            logger.critical(f"Ошибка создания главного окна: {str(e)}")
            raise
    
    def run(self):
        """Запуск приложения"""
        try:
            logger.info("Запуск приложения Менеджер финансов")
            
            self.setup_application()
            self.create_main_window()
            
            # Показ главного окна
            self.main_window.show()
            
            logger.info("Приложение успешно запущено")
            
            # Запуск основного цикла
            return self.app.exec()
            
        except Exception as e:
            logger.critical(f"Критическая ошибка запуска приложения: {str(e)}")
            return 1

def main():
    """Точка входа в приложение"""
    app = FinancialManagerApp()
    exit_code = app.run()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()