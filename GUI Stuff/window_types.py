from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLabel, QVBoxLayout, QGridLayout, QHBoxLayout, QStackedWidget)
from PyQt6.QtCore import Qt
# from main_window import MainStack

class FolderButton(QPushButton):
    def __init__(self, parent, title, dir_id):
        super().__init__(title, parent=parent)

        self.setContentsMargins(20, 20, 20, 20)

        self.clicked.connect(self.but_clicked)
        self.dir_id = dir_id

    def but_clicked(self):
        self.parentWidget().open_folder(self.dir_id)


class FileButton(QPushButton):
    def __init__(self, parent, title, dir_id):
        super().__init__(title + "file", parent=parent)

        self.setContentsMargins(20, 20, 20, 20)

        self.clicked.connect(self.but_clicked)
        self.dir_id = dir_id

    def but_clicked(self):
        self.parentWidget().open_file(self.dir_id)
        
        

class FolderScreen(QWidget):
    def __init__(self, parent, filenames):
        super().__init__(parent=parent)

        self.width = 8

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(20,20,20,20)

        self.folders = []
        self.files = []

        for name, dir, verse_id in filenames:
            if verse_id == None:
                self.but = FolderButton(self, name, dir)
                self.folders.append(self.but)
            else:
                self.but = FileButton(self, name, verse_id)
                self.files.append(self.but)
            self.but.setFixedSize(140, 60)
            # self.but.setFixedWidth(150)
            

        self.setButtonPositions()

        
    def setButtonPositions(self):
        row = 0
        col = 0
        for but in self.folders:
            self.layout.addWidget(but, row, col)
            col += 1
            if col >= self.width:
                col = 0
                row += 1
        for but in self.files:
            self.layout.addWidget(but, row, col)
            col += 1
            if col >= self.width:
                col = 0
                row += 1

    def open_folder(self, dir_id):
        # self.parent.add_folders_screen(38)
        self.parentWidget().add_folder_screen(dir_id)
    
    def open_file(self, verse_id):
        # self.parent.add_folders_screen(38)
        self.parentWidget().open_file_screen(verse_id)


class FileScreen(QWidget):
    def __init__(self, parent, text):
        super().__init__(parent=parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.but = QPushButton("hellloooooo")
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.submit_attempt)
        

    def submit_attempt(self):
        # self.parent.add_folders_screen(38)
        self.parentWidget().back()

