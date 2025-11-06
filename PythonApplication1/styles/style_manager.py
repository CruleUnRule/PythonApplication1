# styles/style_manager.py
from PySide6.QtCore import QObject
import logging
# -*- coding: cp1251 -*-
logger = logging.getLogger(__name__)

class StyleManager(QObject):
    """стиль менеджер работа со стилями"""
    
    @staticmethod
    def get_main_window_style():
        """получение главного окна стилей"""
        return """
            QMainWindow {
                background-color: #f5f5dc;
                font-family: "Segoe UI", "Arial", Sans-Serif;
                font-size: 12pt;
            }
            QGroupBox {
                font-weight: bold;
                border: 3px solid #d2b48c;
                border-radius: 15px;
                margin-top: 1ex;
                padding-top: 15px;
                background-color: #faf0e6;
                font-size: 11pt;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #8b4513;
                background-color: #faf0e6;
                border-radius: 10px;
            }
            QPushButton {
                background-color: #d2b48c;
                border: none;
                padding: 12px 20px;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c19a7b;
            }
            QPushButton:pressed {
                background-color: #a0522d;
                padding: 13px 19px 11px 21px;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #a0a0a0;
            }
            QListWidget {
                background-color: white;
                border: 2px solid #d2b48c;
                border-radius: 10px;
                padding: 10px;
                font-size: 11pt;
                alternate-background-color: #fafafa;
            }
            QListWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #e8e8e8;
            }
            QListWidget::item:selected {
                background-color: #d2b48c;
                color: white;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
                border-radius: 8px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 12px;
                border: 2px solid #d2b48c;
                border-radius: 10px;
                background-color: white;
                font-size: 11pt;
                selection-background-color: #d2b48c;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #a0522d;
                background-color: #fffaf0;
            }
            QLineEdit[error="true"] {
                border-color: #ff6b6b;
                background-color: #ffe6e6;
            }
            QLabel {
                color: #8b4513;
                font-weight: bold;
                font-size: 11pt;
                padding: 5px 0px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 6px solid transparent;
                border-right: 6px solid transparent;
                border-top: 6px solid #8b4513;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #d2b48c;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #d2b48c;
                padding: 5px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #d2b48c;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """
    
    @staticmethod
    def get_dialog_style():
        """возврат обьекта типа style"""
        return """
            QDialog {
                background-color: #f5f5dc;
                font-family: Sans-Serif;
                font-size: 11pt;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 10px;
                border: 2px solid #d2b48c;
                border-radius: 8px;
                background-color: white;
                font-size: 11pt;
                selection-background-color: #d2b48c;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border-color: #a0522d;
                background-color: #fffaf0;
            }
            QLineEdit[error="true"] {
                border-color: #ff6b6b;
                background-color: #ffe6e6;
            }
            QLabel {
                color: #8b4513;
                font-weight: bold;
                font-size: 11pt;
                padding: 5px 0px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #8b4513;
                width: 0px;
                height: 0px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #d2b48c;
                border-radius: 5px;
                background-color: white;
                selection-background-color: #d2b48c;
            }
        """
    
    @staticmethod
    def get_button_style():
        """получение стилей через кнопку"""
        return """
            QPushButton {
                background-color: #d2b48c;
                border: none;
                padding: 10px 20px;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                min-width: 80px;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #c19a7b;
            }
            QPushButton:pressed {
                background-color: #a0522d;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #a0a0a0;
            }
        """
    
    @staticmethod
    def get_history_window_style():
        """история окон стилей"""
        return """
            QDialog {
                background-color: #f5f5dc;
                font-family: Sans-Serif;
                font-size: 11pt;
            }
            QListWidget {
                background-color: white;
                border: 2px solid #d2b48c;
                border-radius: 10px;
                padding: 10px;
                font-size: 11pt;
                alternate-background-color: #fafafa;
            }
            QListWidget::item {
                padding: 12px 8px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #d2b48c;
                color: white;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #d2b48c;
                border-radius: 10px;
                background-color: white;
                font-size: 11pt;
            }
            QLineEdit:focus {
                border-color: #a0522d;
                background-color: #fffaf0;
            }
            QPushButton {
                background-color: #d2b48c;
                border: none;
                padding: 12px 25px;
                border-radius: 15px;
                color: white;
                font-weight: bold;
                font-size: 11pt;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c19a7b;
            }
            QPushButton:pressed {
                background-color: #a0522d;
            }
            QLabel {
                color: #8b4513;
                font-weight: bold;
                font-size: 11pt;
            }
        """