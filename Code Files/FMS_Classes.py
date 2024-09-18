from PySide6.QtGui import QMouseEvent, QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QLabel, QVBoxLayout, QGridLayout, QHBoxLayout, QStackedWidget, QScrollArea,
    QSpacerItem, QSizePolicy, QPlainTextEdit, QStackedLayout, QMenu)

from PySide6.QtCore import Qt, QSize



class TextEntry(QWidget):
    """This class should help me get titles for folders
    and files and such"""
    def __init__(self, title_text, ret_slot, dir_id=0):
        super().__init__()

        self.setFixedSize(250, 40)

        self.ret_slot = ret_slot
        self.dir_id = dir_id

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        #implement title, textedit and

        self.title = QLabel(f"Enter new {title_text} title/name")
        self.layout.addWidget(self.title)

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

        self.confirm_but = QPushButton("Confirm")
        self.confirm_but.clicked.connect(self.verify_text)
        self.layout.addWidget(self.confirm_but)

        self.error_label = QLabel("")
        self.layout.addWidget(self.error_label)

        

    def verify_text(self):
        if self.line_edit.text().strip():
            self.ret_slot(self.line_edit.text(), self.dir_id)
        else:
            self.error_label.setText("Please Enter a name with valid charaters")
 

class SimpleButton(QPushButton):
    """This class should allow me to work with parameters and not have to call in the
    Parent widgets 24/7  
    """
    def __init__(self, title, functions:dict, param_data, size, icon_path:str):
        super().__init__()
        self.funcs = functions
        self.param_data = param_data
        self.setFixedSize(size[0], size[1])
        self.clicked.connect(self.triggered)
        self.selected = False
        if type(param_data) == int:
            self.dir_id = param_data
        else:
            self.dir_id = param_data[0]

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.icon_label = QLabel(self)
        icon_pixmap = QIcon(icon_path).pixmap(QSize(50, 50))  # Adjust the size here as needed
        self.icon_label.setPixmap(icon_pixmap)
        self.layout.addWidget(self.icon_label)

        label = QLabel(title)
        self.layout.addWidget(label)



    def mousePressEvent(self, e: QMouseEvent):
        self.funcs["Set Selected"](self)
          

    
    def mouseDoubleClickEvent(self, event):
        self.funcs["Open"](self.param_data)

    def contextMenuEvent(self, event):
        # Create the context menu
        context_menu = QMenu(self)

        # Add actions to the menu

        for function in self.funcs.items():
            action = QAction(function[0], self)
            action.triggered.connect(function[1])
            context_menu.addAction(action)
        

        # Show the menu at the cursor position
        context_menu.exec_(event.globalPos())

    def triggered(self):
        pass

class FolderScreen(QWidget):
    def __init__(self, contents, funcs, dir_id, button_size=(100,100)):
        super().__init__()
        # the "button_size" Parameter will be (w,h)
        self.num_col = (self.width() * self.devicePixelRatio()) // button_size[0]
        # this is here just cause the freaking witdth seems to be off 
        # and I don't know why. its just bugging me to see so much dead space.
        # self.num_col += 3
        self.but_size = button_size
        self.contents = contents
        self.funcs = funcs

        # Keeping this for refreshing
        self.dir_id = dir_id
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.add_buttons()



    def add_buttons(self):

        self.folders = []
        self.files = []

        if self.contents == None:
            print("nothing in folder")
        else:
            for id, name, file_id, in self.contents:
                if file_id == None:
                    but = SimpleButton(name, self.funcs["Folder Actions"], id, self.but_size, "FolderIcon.png")
                    # but.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
                    self.folders.append(but)
                else:
                    but = SimpleButton(name, self.funcs["File Actions"], (id, file_id), self.but_size, "FileIcon.png")
                    self.files.append(but)
                # self.but.setFixedSize(140, 60)
                # self.but.setFixedWidth(150)
                

            self.setButtonPositions()

        
    def setButtonPositions(self):
        row = 0
        col = 0
        for but in self.folders:
            self.layout.addWidget(but, row, col, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
            col += 1
            if col >= self.num_col:
                col = 0
                row += 1
        for but in self.files:
            self.layout.addWidget(but, row, col, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
            col += 1
            if col >= self.num_col:
                col = 0
                row += 1
        while col <= self.num_col:
            spacer = QSpacerItem(self.but_size[0], self.but_size[1], QSizePolicy.Minimum, QSizePolicy.Expanding)
            # spacer = SimpleButton("spacer", self.height, 94, self.but_size)
            self.layout.addItem(spacer, row, col, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
            col += 1

    # def resizeEvent(self, event):
    #     self.num_col = (self.width() * self.devicePixelRatio()) // self.but_size[0]
    #     self.setButtonPositions()  # Rearrange the buttons based on the new column count



class FileScreen(QWidget):
    def __init__(self, file_id:int, filename:str, contents:str, funcs, new_file=False):
        super(). __init__()
        self.is_new_file = new_file
        self.lay = QGridLayout()
        self.setLayout(self.lay)

        self.filename = filename
        self.contents = contents
        self.label_col_width = 60
        self.funcs = funcs
        # self.file_id = file_id

        self.file_label = QLabel("File Name:")
        # self.file_label.setFixedWidth(self.label_col_width)
        self.lay.addWidget(self.file_label, 0, 0)

        self.filename_widget = QLineEdit(self.filename)
        self.filename_widget.setReadOnly(True)
        self.lay.addWidget(self.filename_widget, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.con_label = QLabel("Contents:")
        # self.con_label.setFixedWidth(self.label_col_width)
        self.lay.addWidget(self.con_label, 1, 0, Qt.AlignmentFlag.AlignTop)

        self.contents_widget = QPlainTextEdit(self.contents)
        self.contents_widget.setReadOnly(True)
        # self.contents_widget.setFixedSize(self.size() * self.devicePixelRatio())
        self.lay.addWidget(self.contents_widget, 1, 1, 3, 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.but_1 = QPushButton("Edit")
        self.but_1.clicked.connect(self.change_mode)
        self.lay.addWidget(self.but_1, 3, 0, 1, 2)

        self.but_2 = QPushButton("Back")
        self.but_2.clicked.connect(self.funcs["back"])
        self.lay.addWidget(self.but_2, 3, 2, 1, 2)


        if self.is_new_file:
            self.change_mode()
        else:
            self.file_id = file_id

    def change_mode(self):
        if self.filename_widget.isReadOnly():
            self.filename_widget.setReadOnly(False)
            self.contents_widget.setReadOnly(False)

            self.update_buttons(True)

        else:
            self.filename_widget.setText(self.filename)
            self.contents_widget.setPlainText(self.contents)
            self.filename_widget.setReadOnly(True)
            self.contents_widget.setReadOnly(True)

            self.update_buttons(False)

    def save_file(self):
        #Verify the data

        # update the actual values
        self.filename = self.filename_widget.text()
        self.contents = self.contents_widget.toPlainText()

        # Call the appropriate functions. the mainstack either needs to 
        # update the file in the DB or create a new one based on if this
        # is a new file. We can use self.edit to be sure of that
        if self.is_new_file:
            self.file_id = self.funcs["add_file_to_DB"](
                self.filename,
                self.contents
            )
            self.is_new_file = False
        
        else:
            self.funcs["update_file"](
                self.file_id,
                self.filename,
                self.contents
            )
        
        # Change the mode back to view
        self.change_mode()

    def update_buttons(self, editing:bool):
        self.but_1.clicked.disconnect()
        self.but_2.clicked.disconnect()

        if editing:
            self.but_1.setText("Cancel")
            if self.is_new_file:
                self.but_1.clicked.connect(self.funcs["back"])
            else:
                self.but_1.clicked.connect(self.change_mode)

            self.but_2.setText("Confirm")
            self.but_2.clicked.connect(self.save_file)
        
        else:
            self.but_1.setText("Edit File")
            self.but_1.clicked.connect(self.change_mode)

            self.but_2.setText("Back")
            self.but_2.clicked.connect(self.funcs["back"])


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
            self.parentWidget().removeWidget()
        else:
            print(self.input.text())

    

