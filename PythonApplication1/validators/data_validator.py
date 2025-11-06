# validators/data_validator.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataValidator:
    """Класс для валидации финансовых данных"""
    
    @staticmethod
    def validate_transaction_data(amount, category, date=None, description=None):
        """
        Валидация данных транзакции
        
        Args:
            amount: Сумма транзакции
            category: Категория транзакции
            date: Дата транзакции (опционально)
            description: Описание транзакции (опционально)
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            validation_errors = []
            
            # Валидация суммы
            if amount is None or amount == "":
                validation_errors.append("Сумма является обязательным полем")
            else:
                try:
                    amount_float = float(amount)
                    if amount_float == 0:
                        validation_errors.append("Сумма не может быть равна нулю")
                    elif abs(amount_float) > 1000000000:
                        validation_errors.append("Слишком большая сумма")
                except (ValueError, TypeError):
                    validation_errors.append("Сумма должна быть числом")
            
            # Валидация категории
            if not category or not category.strip():
                validation_errors.append("Категория является обязательным полем")
            elif len(category.strip()) > 100:
                validation_errors.append("Категория слишком длинная (макс. 100 символов)")
            
            # Валидация описания
            if description and len(description) > 500:
                validation_errors.append("Описание слишком длинное (макс. 500 символов)")
            
            # Валидация даты
            if date:
                try:
                    if isinstance(date, str):
                        datetime.strptime(date, "%Y-%m-%d")
                except ValueError:
                    validation_errors.append("Некорректный формат даты")
            
            if validation_errors:
                return False, "Обнаружены ошибки:\n• " + "\n• ".join(validation_errors)
            
            return True, "Данные валидны"
            
        except Exception as e:
            logger.error(f"Ошибка валидации данных: {str(e)}")
            return False, f"Ошибка валидации: {str(e)}"
    
    @staticmethod
    def validate_amount(amount_text):
        """
        Валидация суммы в реальном времени
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            if not amount_text.strip():
                return True, ""  # Пустое поле - нормально при вводе
            
            try:
                value = float(amount_text)
                if abs(value) > 1000000000:
                    return False, "Слишком большая сумма"
                return True, ""
            except ValueError:
                return False, "Должно быть числом"
                
        except Exception as e:
            logger.error(f"Ошибка валидации суммы: {str(e)}")
            return False, "Ошибка валидации"
    
    @staticmethod
    def is_valid_transaction_structure(transaction):
        """
        Проверка валидности структуры транзакции
        
        Args:
            transaction: Словарь с данными транзакции
            
        Returns:
            bool: True если структура валидна
        """
        try:
            if not isinstance(transaction, dict):
                return False
            
            required_fields = ['amount', 'category', 'date']
            for field in required_fields:
                if field not in transaction:
                    return False
            
            if not isinstance(transaction['amount'], (int, float)):
                return False
            
            if not isinstance(transaction['category'], str) or not transaction['category'].strip():
                return False
            
            if not isinstance(transaction['date'], str) or not transaction['date'].strip():
                return False
            
            return True
            
        except Exception:
            return False