from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class Encryptor:
    """Класс для шифрования и дешифрования текста с поддержкой Unicode."""

    def __init__(self, key):
        self.key = key

    def encrypt(self, text):
        """Шифрование текста с использованием заданного ключа."""
        result = ""
        for char in text:
            encrypted_char = (ord(char) + self.key) % 65536  # Поддержка Unicode символов
            result += f"{encrypted_char:04x}"  # Перевод в шестнадцатеричный вид
        return result

    def decrypt(self, text):
        """Дешифрование текста с использованием заданного ключа."""
        if len(text) % 4 != 0:
            return "Ошибка! Неправильный шифротекст."

        result = ""
        for i in range(0, len(text), 4):
            encrypted_char = int(text[i:i + 4], 16)
            decrypted_char = chr((encrypted_char - self.key) % 65536)
            result += decrypted_char
        return result


class SettingsDialog(QtWidgets.QDialog):
    """Класс для настроек приложения."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setGeometry(400, 300, 300, 200)

        layout = QtWidgets.QVBoxLayout()

        self.auto_copy_checkbox = QtWidgets.QCheckBox("Автоматически копировать результат")
        layout.addWidget(self.auto_copy_checkbox)

        self.theme_button = QtWidgets.QPushButton("Переключить тему")
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)

        # Кнопка для туториала
        self.tutorial_button = QtWidgets.QPushButton("Туториал")
        self.tutorial_button.clicked.connect(self.show_tutorial)
        layout.addWidget(self.tutorial_button)

        self.setLayout(layout)

    def is_auto_copy_enabled(self):
        """Проверка, включено ли автоматическое копирование."""
        return self.auto_copy_checkbox.isChecked()

    def toggle_theme(self):
        """Переключение темы."""
        self.parent().toggle_theme()

    def show_tutorial(self):
        """Показ окна с туториалом."""
        QtWidgets.QMessageBox.information(self, "Туториал",
                                          "1. Введите текст для шифрования или дешифрования.\n"
                                          "2. Укажите ключ (целое число).\n"
                                          "3. Нажмите 'Шифровать' или 'Дешифровать'.\n"
                                          "4. Результат можно скопировать в буфер обмена.\n"
                                          "5. История операций сохраняется для быстрого доступа.\n\n"
                                          "Дополнительно: настройте тему и автоматическое копирование результата в меню 'Настройки'.")


class EncryptDecryptApp(QtWidgets.QWidget):
    """Основной класс приложения шифрования и дешифрования."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Шифратор и дешифратор текста")
        self.setGeometry(300, 300, 600, 500)
        self.is_dark_mode = True
        self.initUI()

    def initUI(self):
        """Инициализация пользовательского интерфейса."""
        layout = QtWidgets.QVBoxLayout()

        title_label = QtWidgets.QLabel("Шифратор и дешифратор текста")
        title_label.setFont(QtGui.QFont("Rostov", 24, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title_label)

        self.input_text = QtWidgets.QTextEdit()
        self.input_text.setFont(QtGui.QFont("Segoe UI", 14))
        layout.addWidget(QtWidgets.QLabel("Введите текст для шифрования/дешифрования:"))
        layout.addWidget(self.input_text)

        key_layout = QtWidgets.QHBoxLayout()
        self.key_label = QtWidgets.QLabel("Ключ (число):")
        key_layout.addWidget(self.key_label)
        self.key_input = QtWidgets.QLineEdit()
        self.key_input.setText("5")
        key_layout.addWidget(self.key_input)
        layout.addLayout(key_layout)

        button_layout = QtWidgets.QHBoxLayout()
        self.encrypt_button = QtWidgets.QPushButton("🔒 Шифровать")
        self.encrypt_button.clicked.connect(self.encrypt_text)
        button_layout.addWidget(self.encrypt_button)

        self.decrypt_button = QtWidgets.QPushButton("🔓 Дешифровать")
        self.decrypt_button.clicked.connect(self.decrypt_text)
        button_layout.addWidget(self.decrypt_button)
        layout.addLayout(button_layout)

        layout.addWidget(QtWidgets.QLabel("Результат:"))
        self.result_text = QtWidgets.QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QtGui.QFont("Segoe UI", 14))
        layout.addWidget(self.result_text)

        self.history_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("История:"))
        layout.addWidget(self.history_list)

        button_panel = QtWidgets.QHBoxLayout()
        copy_button = QtWidgets.QPushButton("📋 Копировать результат")
        copy_button.clicked.connect(self.copy_result)
        button_panel.addWidget(copy_button)

        settings_button = QtWidgets.QPushButton("Настройки")
        settings_button.clicked.connect(self.open_settings)
        button_panel.addWidget(settings_button)

        clear_button = QtWidgets.QPushButton("Очистить поля")
        clear_button.clicked.connect(self.clear_fields)
        button_panel.addWidget(clear_button)

        layout.addLayout(button_panel)
        self.setLayout(layout)

        self.apply_theme()  # Установка начальной темы

    def apply_theme(self):
        """Применение выбранной темы."""
        style_dark = """
        QWidget {
            background-color: #1e1e1e;
            color: #e0e0e0;
            font-family: 'Segoe UI';
        }
        QLabel {
            font-size: 16px;
        }
        QPushButton {
            background-color: #333333;
            color: #e0e0e0;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QTextEdit, QLineEdit {
            background-color: #2e2e2e;
            color: #e0e0e0;
            border: 1px solid #555555;
            padding: 5px;
            font-size: 14px;
        }
        """

        style_light = """
        QWidget {
            background-color: #f5f5f5;
            color: #333;
            font-family: 'Segoe UI';
        }
        QLabel {
            font-size: 16px;
        }
        QPushButton {
            background-color: #e7e7e7;
            color: #333;
            border-radius: 5px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        QTextEdit, QLineEdit {
            background-color: #ffffff;
            color: #333;
            border: 1px solid #cccccc;
            padding: 5px;
            font-size: 14px;
        }
        """

        self.setStyleSheet(style_dark if self.is_dark_mode else style_light)

    def toggle_theme(self):
        """Переключение между темами."""
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def encrypt_text(self):
        """Шифрование текста."""
        self.process_text("encrypt")

    def decrypt_text(self):
        """Дешифрование текста."""
        self.process_text("decrypt")

    def process_text(self, mode):
        """Обработка текста (шифрование или дешифрование)."""
        text = self.input_text.toPlainText().strip()
        try:
            key = int(self.key_input.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Ключ должен быть числом.")
            return

        if not text:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Текст не должен быть пустым.")
            return

        encryptor = Encryptor(key)
        result = encryptor.encrypt(text) if mode == "encrypt" else encryptor.decrypt(text)
        self.result_text.setPlainText(result)
        self.history_list.addItem(result)

        if hasattr(self, 'settings_dialog') and self.settings_dialog.is_auto_copy_enabled():
            self.copy_result()

    def copy_result(self):
        """Копирование результата в буфер обмена."""
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())
        QtWidgets.QMessageBox.information(self, "Скопировано", "Результат скопирован в буфер обмена!")

    def clear_fields(self):
        """Очистка полей ввода и вывода."""
        self.input_text.clear()
        self.key_input.clear()
        self.result_text.clear()
        self.history_list.clear()

    def open_settings(self):
        """Открытие диалогового окна настроек."""
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EncryptDecryptApp()
    window.show()
    sys.exit(app.exec_())

