# from window_types import *
from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtWidgets import QMenu, QWidget
from FMS_Classes import *
from DBI_Class import DBInterface
from Stack_Classes import FileStack


        

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

        for name, function, data in button_data:
            but = ButWithParams(name, function, data)
            self.layout.addWidget(but)




class LQStack(FileStack):
    def __init__(self, db_conn, table_name):
        super().__init__(db_conn, table_name)

    def add_file_screen():
        pass

        
class FMSStack(FileStack):
    def __init__(self, db_conn, db_table):
        super().__init__(db_conn, db_table)

        self.cut_id = None
        self.copy_id = None

        self.folder_actions["Rename Folder"] = self.rename_folder,
        self.folder_actions["Add to Learning Queue"] = self.set_learning,
        self.folder_actions["Copy"] = self.copy,
        self.folder_actions["Cut"] = self.cut,
        self.folder_actions["Delete"] = self.delete,
        self.folder_actions["Set Selected"] = self.set_selected
            
            
        self.file_actions["Add to Learning Queue"] = self.set_learning
        self.file_actions["Copy"] = self.copy
        self.file_actions["Cut"] = self.cut
        self.file_actions["Delete"] = self.delete
        self.file_actions["Set Selected"] = self.set_selected
    


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

    def add_file_screen(self, IDs):
        file_id = IDs[1]
        dir_id = IDs[0]

        filename, contents = self.conn.get_file_contents(file_id)

        file_screen = FileScreen(file_id, filename, contents, self.functions["File Functions"])
        self.push(file_screen)
        self.curr_file_id = file_id
        self.curr_dir = dir_id
    
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
        self.conn.copy(self.copy_id, self.curr_dir)
        self.refresh()

    def rename_folder(self):
        pass

    def set_learning(self):
        self.conn.set_state(self.selected_widget.dir_id, 1)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.db_conn = DBInterface()

        self.showMaximized()
        self.setWindowTitle("Project 1")

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.fms_stack = FMSStack(self.db_conn, "Directory")
        self.lq_stack = LQStack(self.db_conn, "Directory")
        



        # Header
        # self.header = Sidebar(QHBoxLayout, QPushButton,
        # [("Back", self.fms_stack.back),
        # ("Refresh", self.fms_stack.refresh)], max_height=40)
        # self.layout.addWidget(self.header, 0, 0, 1, -1, Qt.AlignmentFlag.AlignLeft)

        self.                                        scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setWidget(self.fms_stack)
      

        # Navigation Bar
        self.nav_bar = Sidebar(QVBoxLayout, 
            [("File Management", self.replacescrollwidget, self.fms_stack),
            ("Learning Queue", self.replacescrollwidget, self.fms_stack),
            ("Testing", self.replacescrollwidget, self.fms_stack)],
            max_width=160)
        self.layout.addWidget(self.nav_bar, 1, 0, -1, 1, Qt.AlignmentFlag.AlignVCenter)


        self.layout.addWidget(self.scrollarea, 1, 1)


    def replacescrollwidget(self, widget):
        self.scrollarea.takeWidget()
        self.scrollarea.setWidget(widget)
