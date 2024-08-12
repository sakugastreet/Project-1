from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLabel, QVBoxLayout, QGridLayout, QHBoxLayout, QStackedWidget, QScrollArea)
from PyQt6.QtCore import Qt
import sys
from window_types import *
from db_interface import *
import pandas as pd

class Header(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)

        # Parameters
        self.HEAD_BUT_HEIGHT = 40
        self.HM = 10
        self.WM = 20

        # Create and set layout
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setMaximumHeight(self.HEAD_BUT_HEIGHT + 2*self.HM)
        self.setContentsMargins(self.WM, self.HM, self.WM, self.HM)


        # Set back Button
        self.back_but = QPushButton("<-")
        self.back_but.setFixedHeight(self.HEAD_BUT_HEIGHT)
        self.back_but.clicked.connect(parent.back)
        self.layout.addWidget(self.back_but)

        # Set Home Button
        self.home_but = QPushButton("Home")
        self.home_but.setFixedHeight(self.HEAD_BUT_HEIGHT)
        self.home_but.clicked.connect(self.parentWidget().home)
        self.layout.addWidget(self.home_but)

        # Set ____ Button
        self.head_but_2 = QPushButton("____")
        self.head_but_2.setFixedHeight(self.HEAD_BUT_HEIGHT)
        # self.button.clicked.connect(self.display)
        self.layout.addWidget(self.head_but_2)

        # Set ____ Button
        self.head_but_3 = QPushButton("____")
        self.head_but_3.setFixedHeight(self.HEAD_BUT_HEIGHT)
        # self.button.clicked.connect(self.display)
        self.layout.addWidget(self.head_but_3)
        

class MainStack(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        # gets all the files for a 
        self.conn = DBInterface()
        # 101 is the current id for the root folder
        self.home()

    def home(self):
        root = self.get_dir_children("101")
            
        self.base = FolderScreen(self, root)
        self.setCurrentIndex(self.addWidget(self.base))
        
    

    def add_folder_screen(self, new_dir):
        filenames = self.get_dir_children(new_dir)
        folder = FolderScreen(self, filenames)
        print(self.count())
        self.setCurrentIndex(self.addWidget(folder))

        
    def open_file_screen(self):
        file = FileScreen(self)
        self.setCurrentIndex(self.addWidget(file))

    def back(self):
        self.parentWidget().back()

    def get_dir_children(self, dir):
        """Returns a list of tuples, each one containing the directory text and
        the correspoding id
        """
        root = self.conn.execute("*", "directory", f"WHERE par_dir = {dir}")
        files = []
        for index, row in root.iterrows():
            files.append((row["dir"], row["id"], row["verse_id"]))
        return files


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # self.resize(300, 300)
        self.showMaximized()
        self.setWindowTitle("hoooplaaah")
        self.setContentsMargins(20, 10, 20, 20)
        self.slot_int = 2

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


        self.head = Header(self)
        self.layout.addWidget(self.head)

        self.main_stack = MainStack()
        # self.layout.addWidget(self.main_stack)

        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.main_stack)

        self.layout.addWidget(self.scrollarea)

    def display(self):
        newlabel = QLabel(str(self.slot_int))
        self.layout.addWidget(newlabel, self.slot_int, 1)
        self.slot_int += 1

    def back(self):
        if self.main_stack.count() > 1:

            self.main_stack.removeWidget(self.main_stack.currentWidget())

        
    def home(self):
        
        if self.main_stack.count() > 1:

            self.main_stack.home()






app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

