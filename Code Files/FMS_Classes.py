from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLabel, QVBoxLayout, QGridLayout, QHBoxLayout, QStackedWidget, QScrollArea)

from PySide6.QtCore import Qt


class SimpleButton(QPushButton):
    """This class should allow me to work with parameters and not have to call in the
    Parent widgets 24/7  
    """
    def __init__(self, title, function, param_data):
        super().__init__(title)
        self.func = function
        self.param_data = param_data
        self.clicked.connect(self.triggered)
        

    def triggered(self):
        self.func(self.param_data)
     
        

class FolderScreen(QWidget):
    def __init__(self, files, functions):
        super().__init__()

        self.width = 8

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(20,20,20,20)

        self.folders = []
        self.files = []

        for id, name, file_id, tag_id in files:
            if file_id == None:
                self.but = SimpleButton(name, functions[0], id)
                self.folders.append(self.but)
            else:
                self.but = SimpleButton(name, functions[1], [file_id, tag_id])
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


class FileScreen(QWidget):
    def __init__(self, filename, contents, tag, back):
        super(). __init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.label = QLabel(filename)
        self.layout.addWidget(self.label, 0, 1)

        self.contents = QLabel(contents)
        self.layout.addWidget(self.contents, 1, 0, 3, 3)

        self.tag = QLabel(tag)
        self.layout.addWidget(self.tag, 5, 0)

        self.back = QPushButton("Back")
        self.back.clicked.connect(back)
        self.layout.addWidget(self.back, 6, 3)



class TestScreen(QWidget):
    def __init__(self, text, back):
        super().__init__()
        
        self.verse = text

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.text = QLabel(text)
        self.text.setAlignment(Qt.AlignmentFlag.AlignLeading)
        self.layout.addWidget(self.text)

        self.input = QLineEdit()
        self.layout.addWidget(self.input)

        self.but = QPushButton("Submit")
        self.but.clicked.connect(back)
        self.layout.addWidget(self.but)
        self.but.clicked.connect(self.submit_attempt)

        

    def submit_attempt(self):
        if self.input.text() == self.verse:
            print("yay")
            self.parentWidget().removeWidget()
        else:
            print("boo!")
            print(self.input.text())

