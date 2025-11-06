import json
import os
import logging
from datetime import datetime
from storage.data_storage import DataStorage

logger = logging.getLogger(__name__)


class TransactionManager:
    """Менеджер транзакций - бизнес-логика приложения"""

    def __init__(self):
        self.data_storage = DataStorage()

    def add_transaction(self, amount, category, date, description=""):
        """Добавляет новую транзакцию"""
        transaction = {
            'amount': amount,
            'category': category,
            'date': date,
            'description': description
        }
        self.data_storage.add_transaction(transaction)

    def get_all_transactions(self):
        """Возвращает все транзакции"""
        return self.data_storage.get_all_transactions()

    def get_transaction_by_index(self, index):
        """Возвращает транзакцию по индексу"""
        transactions = self.get_all_transactions()
        if 0 <= index < len(transactions):
            return transactions[index]
        return None

    def update_transaction(self, index, updated_data):
        """Обновляет транзакцию по индексу"""
        self.data_storage.update_transaction(index, updated_data)

    def delete_transaction(self, index):
        """Удаляет транзакцию по индексу"""
        self.data_storage.delete_transaction(index)

    def get_categories(self):
        """Возвращает список уникальных категорий"""
        transactions = self.get_all_transactions()
        categories = set()

        for transaction in transactions:
            categories.add(transaction['category'])

        return sorted(list(categories))

    def calculate_balance(self):
        """Рассчитывает общий баланс"""
        transactions = self.get_all_transactions()
        balance = 0

        for transaction in transactions:
            balance += transaction['amount']

        return balance

    def filter_by_category(self, category):
        """Фильтрует транзакции по категории"""
        transactions = self.get_all_transactions()
        filtered = []

        for transaction in transactions:
            if transaction['category'] == category:
                filtered.append(transaction)

        return filtered

    def search_transactions(self, search_text):
        """Ищет транзакции по тексту (без учета регистра)"""
        transactions = self.get_all_transactions()
        results = []
        search_text = search_text.lower()

        for transaction in transactions:
            if (search_text in transaction['category'].lower() or
                    search_text in transaction.get('description', '').lower()):
                results.append(transaction)

        return results

    def export_to_json(self, file_path):
        """
        Экспортирует все транзакции в JSON файл

        Args:
            file_path (str): Путь для сохранения файла

        Returns:
            bool: True если успешно, False в случае ошибки
        """
        try:
            transactions = self.get_all_transactions()

            export_data = {
                "export_info": {
                    "version": "1.0",
                    "export_date": datetime.now().isoformat(),
                    "transaction_count": len(transactions),
                    "application": "Finance Manager"
                },
                "transactions": transactions
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2,
                          default=self._json_serializer)

            logger.info(f"Успешно экспортировано {len(transactions)} транзакций в {file_path}")
            return True

        except Exception as e:
            logger.error(f"Ошибка экспорта в {file_path}: {str(e)}")
            return False

    def import_from_json(self, file_path):
        """
        Импортирует транзакции из JSON файла

        Args:
            file_path (str): Путь к файлу для импорта

        Returns:
            tuple: (success, message) - успех и сообщение
        """
        try:
            if not os.path.exists(file_path):
                return False, f"Файл не найден: {file_path}"

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            transactions = self._validate_import_data(data)
            if transactions is None:
                return False, "Некорректный формат файла"

            if not transactions:
                return False, "Файл не содержит корректных транзакций"

            backup_success = self._create_pre_import_backup()
            if not backup_success:
                logger.warning("Не удалось создать резервную копию перед импортом")

            self.data_storage.replace_all_transactions(transactions)

            report = self._generate_import_report(transactions, data.get('export_info', {}))

            logger.info(f"Успешно импортировано {len(transactions)} транзакций из {file_path}")
            return True, report

        except json.JSONDecodeError as e:
            logger.error(f"Ошибка JSON в файле {file_path}: {str(e)}")
            return False, f"Ошибка формата JSON: {str(e)}"
        except Exception as e:
            logger.error(f"Ошибка импорта из {file_path}: {str(e)}")
            return False, f"Ошибка импорта: {str(e)}"

    def create_backup(self, backup_path=None):
        """
        Создает резервную копию данных

        Args:
            backup_path (str, optional): Путь для бэкапа. Если None - автоматический

        Returns:
            bool: True если успешно, False в случае ошибки
        """
        try:
            if backup_path is None:
                backup_dir = "backups"
                if not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(backup_dir, f"backup_{timestamp}.json")

            return self.export_to_json(backup_path)

        except Exception as e:
            logger.error(f"Ошибка создания резервной копии: {str(e)}")
            return False

    def _json_serializer(self, obj):
        """Сериализатор для объектов, которые не могут быть сериализованы JSON по умолчанию"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def _validate_import_data(self, data):
        """
        Валидирует и извлекает транзакции из импортируемых данных

        Args:
            data: Загруженные данные

        Returns:
            list: Список валидных транзакций или None при ошибке
        """
        try:
            if isinstance(data, dict) and 'transactions' in data:
                transactions = data['transactions']
            elif isinstance(data, list):
                transactions = data
            else:
                return None

            valid_transactions = []
            for i, transaction in enumerate(transactions):
                if self._is_valid_transaction_structure(transaction):
                    normalized = self._normalize_transaction(transaction)
                    valid_transactions.append(normalized)
                else:
                    logger.warning(f"Пропущена некорректная транзакция #{i}: {transaction}")

            return valid_transactions

        except Exception as e:
            logger.error(f"Ошибка валидации импортируемых данных: {str(e)}")
            return None

    def _is_valid_transaction_structure(self, transaction):
        """Проверяет валидность структуры транзакции"""
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

    def _normalize_transaction(self, transaction):
        """Нормализует данные транзакции"""
        try:
            normalized = transaction.copy()

            if isinstance(normalized['amount'], str):
                try:
                    normalized['amount'] = float(normalized['amount'])
                except ValueError:
                    normalized['amount'] = 0.0

            normalized['category'] = normalized['category'].strip()

            if 'description' in normalized:
                if not isinstance(normalized['description'], str):
                    normalized['description'] = str(normalized.get('description', ''))
                normalized['description'] = normalized['description'].strip()
            else:
                normalized['description'] = ''

            return normalized

        except Exception as e:
            logger.error(f"Ошибка нормализации транзакции: {str(e)}")
            return transaction

    def _create_pre_import_backup(self):
        """Создает резервную копию перед импортом"""
        try:
            backup_dir = "backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"pre_import_backup_{timestamp}.json")

            return self.export_to_json(backup_path)

        except Exception as e:
            logger.error(f"Ошибка создания предварительной резервной копии: {str(e)}")
            return False

    def _generate_import_report(self, transactions, export_info):
        """Генерирует отчет об импорте"""
        try:
            total_count = len(transactions)
            income_count = sum(1 for t in transactions if t.get('amount', 0) > 0)
            expense_count = sum(1 for t in transactions if t.get('amount', 0) < 0)
            categories = len(set(t.get('category', '') for t in transactions))

            report = f"""✅ Импорт завершен успешно!

📊 Статистика импортированных данных:
• Всего транзакций: {total_count}
• Доходы: {income_count}
• Расходы: {expense_count}
• Уникальных категорий: {categories}"""

            if export_info:
                source_app = export_info.get('application', 'Неизвестно')
                export_date = export_info.get('export_date', 'Неизвестно')

                try:
                    if export_date != 'Неизвестно':
                        export_date = datetime.fromisoformat(export_date).strftime("%d.%m.%Y %H:%M")
                except:
                    pass

                report += f"\n\n📁 Источник данных:"
                report += f"\n• Приложение: {source_app}"
                report += f"\n• Дата экспорта: {export_date}"

            return report

        except Exception as e:
            logger.error(f"Ошибка генерации отчета: {str(e)}")
            return "✅ Импорт завершен успешно!"