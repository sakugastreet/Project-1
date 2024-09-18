# from window_types import *
from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtWidgets import QMenu
from FMS_Classes import *
from DBI_Class import DBInterface

        

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
        self.selected_widget = None
    
        # 101 is the current id for the root folder
        self.root_dir = 1
        self.curr_dir = self.root_dir
        self.curr_file_id = None

        self.cut_id = None
        self.copy_id = None

        folder_actions = {
            "Open":self.add_folder_screen,
            "Rename Folder":self.rename_folder,
            "Copy":self.copy,
            "Cut":self.cut,
            "Delete":self.delete,
            "Set Selected":self.set_selected
        }
        file_actions = {
            "Open":self.add_file_screen,
            "Copy":self.copy,
            "Cut":self.cut,
            "Delete":self.delete,
            "Set Selected":self.set_selected

        }
        file_functions = {
            "back":self.back,
            "add_file_to_DB":self.add_file_to_DB,
            "update_file":self.update_file}
    
        self.functions = {
            "Folder Actions":folder_actions,
            "File Actions":file_actions,
            "File Functions":file_functions,
        }

    
    def set_selected(self, widget):
        self.selected_widget = widget
        print(widget.dir_id)


    def contextMenuEvent(self, event):
        # Create the context menu
        context_menu = QMenu(self)

        # Add actions to the menu
        action1 = QAction("New Folder", self)
        action1.triggered.connect(self.new_folder)
        action2 = QAction("New File", self)
        action2.triggered.connect(self.new_file)


        context_menu.addAction(action1)
        context_menu.addAction(action2)

        if self.copy_id != None or self.cut_id != None:
            action3 = QAction("Paste", self)
            if self.cut_id == None:
                action3.triggered.connect(self.paste_copy)
            else:
                action3.triggered.connect(self.paste_cut)
            context_menu.addAction(action3)



        # Show the menu at the cursor position
        context_menu.exec_(event.globalPos())


    def openFMS(self):
        self.add_folder_screen(self.root_dir)
        

    def add_folder_screen(self, dir_id):
        # if type(IDs) == int:
        #     dir_id = IDs
        # else:
        #     dir_id = IDs[0]

        filenames = self.conn.get_folder_contents(dir_id)
        folder = FolderScreen(filenames, self.functions, dir_id)
        self.push(folder)
        self.curr_dir = dir_id
        print(self.curr_dir) 

    def add_file_screen(self, IDs):
        file_id = IDs[1]
        dir_id = IDs[0]

        filename, contents = self.conn.get_file_contents(file_id)

        file_screen = FileScreen(file_id, filename, contents, self.functions["File Functions"])
        self.push(file_screen)
        self.curr_file_id = file_id
        self.curr_dir = dir_id

    def back(self):
        if self.count() > 1:
            self.removeWidget(self.currentWidget())
            # if at the root file, then we fault out, so Im adding an if
            # statment to protect from that
            self.curr_dir = self.conn.get_par_id(self.curr_dir)
            self.refresh()
            self.curr_file_id = None
                   
    def push(self, widget):
        self.setCurrentIndex(self.addWidget(widget))
    
    def new_folder(self):
        text_entry = TextEntry("New Folder", self.add_folder_to_DB, self.curr_dir)
        self.push(text_entry)

    def add_folder_to_DB(self, folder_name, dir_id):
        self.conn.insert("Directory", ["Name", "Par_id"], [folder_name, f"{dir_id}"])
        self.refresh()

    def update_file(self, file_id, filename, contents):
        self.conn.update_file(filename, contents, file_id)

    def new_file(self):
        new_file = FileScreen(None, "", "", {"back":self.back, "add_file_to_DB":self.add_file_to_DB, "update_file":self.update_file}, True)
        self.push(new_file)

    def add_file_to_DB(self, filename:str, contents:str):
        """Given a filename and a string, it creates a new row in the Files table
        and returns the ID of said new row."""
        
        file_id = self.conn.add_file(self.curr_dir, filename, contents)
        self.curr_file_id = file_id
        return file_id
    
    def refresh(self):
            self.removeWidget(self.currentWidget())
            
            if self.conn.is_folder(self.curr_dir):
                self.add_folder_screen(self.curr_dir)

            else:
                self.add_file_screen((self.curr_dir, self.curr_file_id))
                
    def copy(self):
        self.copy_id = self.selected_widget.dir_id

    def delete(self):
        self.conn.delete_from_DB(self.selected_widget.dir_id)
        self.refresh()

    def cut(self):
        self.cut_id = self.selected_widget.dir_id

    def paste_cut(self):
        self.conn.move(self.cut_id, self.curr_dir)
        self.refresh()
        self.cut_id = None

    def paste_copy(self):
        print("item copied")
        self.conn.copy(self.copy_id, self.curr_dir)
        self.refresh()

    def rename_folder(self):
        pass


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
        self.header = Sidebar(QHBoxLayout,
        [("Back", self.main_stack.back),
        ("Refresh", self.main_stack.refresh)], max_height=40)
        self.layout.addWidget(self.header, 0, 0, 1, -1, Qt.AlignmentFlag.AlignLeft)

        # Navigation Bar
        self.nav_bar = Sidebar(QVBoxLayout, [
            ("File Management", self.main_stack.openFMS)
            # ("Learning Queue", self.main_stack.openLQ),
            # ("Testing Station", self.main_stack.openTS),
            # ("Settings", self.main_stack.open_ST)
            ], max_width=160)
        self.layout.addWidget(self.nav_bar, 1, 0, -1, 1, Qt.AlignmentFlag.AlignVCenter)


        # the main stack is added to a scroll area, in case it
        # ever gets too large
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.main_stack)

        self.layout.addWidget(self.scrollarea, 1, 1)
