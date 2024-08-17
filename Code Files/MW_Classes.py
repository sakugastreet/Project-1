# from window_types import *
from FMS_Classes import *
from DBI_Class import DBInterface

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
        

class Sidebar(QWidget):
    def __init__(self, layout, button_data, max_width=None, max_height=None):
        super().__init__()

        if max_height != None:
            self.setMaximumHeight(max_height)
        if max_width != None:
            self.setMaximumWidth(max_width)

        # self.setContentsMargins(0,0,0,0)

        self.layout = layout()
        self.setLayout(self.layout)

        for name, function in button_data:
            but = QPushButton(name)
            but.clicked.connect(function)
            self.layout.addWidget(but)

        

        

class MainStack(QStackedWidget):
    def __init__(self):
        super().__init__()
        
        # gets all the files for a 
        self.conn = DBInterface()
        print("database connected")
        # 101 is the current id for the root folder


    def openFMS(self):
        folder_contents = self.conn.get_folder_contents(1)
        if folder_contents == []:
            print("Error Finding file in database")
            return

        self.base = FolderScreen(folder_contents, [self.add_folder_screen, self.add_file_screen])
        self.base.add_buttons()
        self.setCurrentIndex(self.addWidget(self.base))

    def openLQ(self):
        pass
    #     root = self.get_dir_children("101")
            
    #     self.base = FolderScreen(self, root, [self.add_LQfolder_screen, self.add_test_screen])
    #     self.setCurrentIndex(self.addWidget(self.base))

    def openTS(self):
        pass

    def open_ST(self):
        pass
        

    def add_folder_screen(self, new_dir):
        filenames = self.conn.get_folder_contents(new_dir)
        folder = FolderScreen(self, filenames, [self.add_folder_screen, self.add_file_screen])
        print(folder.widthMM)
        print(self.count())
        self.setCurrentIndex(self.addWidget(folder))
    

    # def add_LQfolder_screen(self, new_dir):
    #     filenames = self.get_dir_children(new_dir)
    #     folder = FolderScreen(self, filenames, [self.add_LQfolder_screen, self.add_test_screen])
    #     print(self.count())
    #     self.setCurrentIndex(self.addWidget(folder))

    # def add_test_screen(self, verse_id):
    #     screen = TestScreen(self.get_verse(verse_id), self.back)
    #     self.setCurrentIndex(self.addWidget(screen))

    def add_file_screen(self, param_data):
        file = self.conn.get_file_contents(f"{param_data[0]}", f"{param_data[1]}")
        print(file)
        file_screen = FileScreen(file[0], file[1], file[2], self.back)
        self.push(file_screen)


    def back(self):
        if self.count() > 1:
            self.removeWidget(self.currentWidget())
            
    
    def push(self, widget):
        self.setCurrentIndex(self.addWidget(widget))
    
    def get_file(self, verse_id):
        """Returns a verse from the "verses" table based on the given verse ID"""


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # self.resize(300, 300)
        self.showMaximized()
        self.setWindowTitle("hoooplaaah")
        # self.setContentsMargins(20, 10, 20, 20)
        self.slot_int = 2

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Creates main stack. It is created before most everything
        # so the nav_bar can use its methods
        self.main_stack = MainStack()
        self.main_stack.openFMS()

        # Header
        self.header = Sidebar(QHBoxLayout, [("Back", self.main_stack.back)], max_height=40)
        self.layout.addWidget(self.header, 0, 0, 1, -1, Qt.AlignmentFlag.AlignLeft)

        # Navigation Bar
        self.nav_bar = Sidebar(QVBoxLayout, [
            ("File Management", self.main_stack.openFMS),
            ("Learning Queue", self.main_stack.openLQ),
            ("Testing Station", self.main_stack.openTS),
            ("Settings", self.main_stack.open_ST)
            ], max_width=80)
        self.layout.addWidget(self.nav_bar, 1, 0, -1, 1, Qt.AlignmentFlag.AlignVCenter)


        # the main stack is added to a scroll area, in case it
        # ever gets too large
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.main_stack)

        self.layout.addWidget(self.scrollarea, 1, 1)


           

    # TODO: run this functionality only in one class,
    # not in both the window and mainstack classes
    def home(self):
        
        if self.main_stack.count() > 1:

            self.main_stack.home()
