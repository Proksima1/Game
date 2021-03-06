import json
import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.action.setShortcut('Ctrl+N')
        self.action_2.setShortcut('Ctrl+O')
        self.action_3.setShortcut('Ctrl+X')
        self.pushButton.clicked.connect(self.generate_file)

    def generate_file(self):
        """Сгенерировать файл по заданным настройкам, если файла с таким именем не существует,
        иначе выдаётся диалог с выбором."""
        def write():
            """Запись в файл с заданным именем"""
            try:
                with open(f'../data/{self.lineEdit.text()}.json', 'w', encoding='utf-8') as editor:
                    editor.write(json.dumps([{'amount_of_waves': waves, 'amount_of_enemies': enemies,
                                              'max_level': max_level, 'max_speed': max_speed}],
                                            indent=4, separators=(',', ': '), sort_keys=True))
            except Exception as e:
                raise Exception(e)
            else:
                return True
        if self.tabWidget.currentIndex() == 0:
            waves = self.spinBox.value()
            enemies = self.spinBox_2.value()
            max_level = self.spinBox_3.value()
            max_speed = self.spinBox_4.value()
            if all(list(map(int, [waves, enemies, max_speed, max_level]))):
                if not os.path.exists(f'../data/{self.lineEdit.text()}.json'):
                    try:
                        write()
                    except Exception as e:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setWindowTitle("Ошибка!")
                        msg.setText(f"Произошла ошибка {e} при создании файла!")
                        okButton = msg.addButton(QMessageBox.Ok)
                        msg.exec()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setWindowTitle("Успех!")
                        msg.setText(f"Файл под названием {self.lineEdit.text()}.json успешно записан!")
                        okButton = msg.addButton(QMessageBox.Ok)
                        msg.exec()
                else:
                    # создание диалога
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Предупреждение!")
                    msg.setText("Такой файл уже существует, перезаписать?")
                    okButton = msg.addButton(QMessageBox.Ok)
                    cancelButton = msg.addButton(QMessageBox.Cancel)
                    msg.exec()  # вызов диалога
                    # проверка нажатия кнопки
                    if msg.clickedButton() == okButton:
                        write()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Внимание!")
                msg.setText("Один из настроек равен 0! Измените, и попробуйте снова!")
                okButton = msg.addButton(QMessageBox.Ok)
                msg.exec()  # вызов диалога
        #elif self.tabWidget.currentIndex() == 1:
           # x = 1
           # for level in range(1, int(self.spinBox_5.value()) + 1):
              #  print(x)
              #  x += self.spinBox_6.value()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    edit = Editor()
    edit.show()
    sys.exit(app.exec())