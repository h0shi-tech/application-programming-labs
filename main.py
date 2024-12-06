import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from pathlib import Path
from lab2_iterator import DatasetIterator  # Импортируем итератор из лабораторной работы №2


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Просмотр датасета")
        self.setGeometry(100, 100, 800, 600)

        # Элементы интерфейса
        self.layout = QVBoxLayout()

        self.image_label = QLabel("Выберите папку с датасетом", self)
        self.image_label.setAlignment(QtGui.Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(600, 400)
        self.layout.addWidget(self.image_label)

        self.select_folder_button = QPushButton("Выбрать папку с датасетом", self)
        self.select_folder_button.clicked.connect(self.select_folder)
        self.layout.addWidget(self.select_folder_button)

        self.next_button = QPushButton("Следующее изображение", self)
        self.next_button.clicked.connect(self.show_next_image)
        self.next_button.setEnabled(False)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        # Переменные
        self.iterator = None
        self.dataset_path = None

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку с датасетом")
        if folder:
            self.dataset_path = Path(folder)
            self.iterator = DatasetIterator(self.dataset_path)  # Создаем итератор
            self.next_button.setEnabled(True)
            self.show_next_image()

    def show_next_image(self):
        if self.iterator:
            try:
                image_path = next(self.iterator)  # Получаем следующий путь
                pixmap = QtGui.QPixmap(str(image_path))
                self.image_label.setPixmap(pixmap)
            except StopIteration:
                self.image_label.setText("Все изображения просмотрены.")
                self.next_button.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
