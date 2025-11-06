# Data storage for transactions
import json
import os
import logging

logger = logging.getLogger(__name__)


class DataStorage:
    """Класс для работы с хранением данных в JSON файле"""

    def __init__(self, filename="transactions.json"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Создает файл, если он не существует"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def get_all_transactions(self):
        """Читает все транзакции из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def add_transaction(self, transaction):
        """Добавляет транзакцию в файл"""
        transactions = self.get_all_transactions()
        transactions.append(transaction)
        self._save_transactions(transactions)

    def delete_transaction(self, index):
        """Удаляет транзакцию по индексу"""
        transactions = self.get_all_transactions()
        if 0 <= index < len(transactions):
            transactions.pop(index)
            self._save_transactions(transactions)

    def update_transaction(self, index, updated_data):
        """Обновляет транзакцию по индексу"""
        transactions = self.get_all_transactions()
        if 0 <= index < len(transactions):
            transactions[index] = updated_data
            self._save_transactions(transactions)
            logger.info(f"Транзакция #{index} обновлена в хранилище")
        else:
            raise IndexError(f"Индекс {index} вне диапазона")

    def replace_all_transactions(self, new_transactions):
        """
        Полностью заменяет все транзакции новыми

        Args:
            new_transactions (list): Новый список транзакций

        Returns:
            bool: True если успешно, False в случае ошибки
        """
        try:
            if not isinstance(new_transactions, list):
                raise ValueError("new_transactions должен быть списком")

            self._save_transactions(new_transactions)
            logger.info(f"Все транзакции заменены. Новое количество: {len(new_transactions)}")
            return True

        except Exception as e:
            logger.error(f"Ошибка замены транзакций: {str(e)}")
            return False

    def get_transactions_count(self):
        """
        Возвращает количество транзакций

        Returns:
            int: Количество транзакций
        """
        try:
            transactions = self.get_all_transactions()
            return len(transactions)
        except Exception as e:
            logger.error(f"Ошибка получения количества транзакций: {str(e)}")
            return 0

    def _save_transactions(self, transactions):
        """Сохраняет транзакции в файл"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(transactions, f, ensure_ascii=False, indent=2)