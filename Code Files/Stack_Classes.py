from PySide6.QtGui import QContextMenuEvent, QAction
from PySide6.QtWidgets import QMenu, QWidget, QStackedWidget
from abc import abstractmethod
from FMS_Classes import FolderScreen

class FileStack(QStackedWidget):
    def __init__(self, db_conn, table_name):
        super().__init__()
        self.conn = db_conn
        self.table_name = table_name
        self.selected_widget = None

        self.root_dir = 1
        self.curr_dir = self.root_dir
        self.curr_file_id = None

        self.folder_actions = {
            "Open":self.add_folder_screen,
            # "Rename Folder":self.rename_folder,
            # "Add to Learning Queue":self.set_learning,
            # "Copy":self.copy,
            # "Cut":self.cut,
            # "Delete":self.delete,
            # "Set Selected":self.set_selected
        }
        self.file_actions = {
            "Open":self.add_file_screen,
            # "Add to Learning Queue":self.set_learning,
            # "Copy":self.copy,
            # "Cut":self.cut,
            # "Delete":self.delete,
            # "Set Selected":self.set_selected

        }
        self.file_functions = {
            "back":self.back,
            "add_file_to_DB":self.add_file_to_DB,
            "update_file":self.update_file
            }

        self.functions = {
            "Folder Actions":self.folder_actions,
            "File Actions":self.file_actions,
            "File Functions":self.file_functions
        }

        self.add_folder_screen(1)

    def set_selected(self, widget):
        self.selected_widget = widget

    def back(self):
        if self.count() > 1:
            self.removeWidget(self.currentWidget())
            # if at the root file, then we fault out, so Im adding an if
            # statment to protect from that
            self.curr_dir = self.conn.get_par_id(self.curr_dir)
            self.refresh()
            self.curr_file_id = None

            self.add_folder_screen(1)
            
    def push(self, widget):
        self.setCurrentIndex(self.addWidget(widget))

    def refresh(self):
            self.removeWidget(self.currentWidget())
            
            if self.conn.is_folder(self.curr_dir):
                self.add_folder_screen(self.curr_dir)

            else:
                self.add_file_screen((self.curr_dir, self.curr_file_id))
    
    def add_folder_screen(self, dir_id):
        
        contents = self.conn.get_folder_contents(dir_id, self.table_name)
        folder = FolderScreen(contents, self.functions, dir_id)
        self.push(folder)
        self.curr_dir = dir_id

    @abstractmethod
    def add_file_screen(self, file_id):
        pass

    def add_file_to_DB(self, filename:str, contents:str):
    
        """Given a filename and a string, it creates a new row in the Files table
        and returns the ID of said new row."""
        
        file_id = self.conn.add_file(self.curr_dir, filename, contents)
        self.curr_file_id = file_id
        return file_id
    
    def update_file(self, file_id, filename, contents):
        self.conn.update_file(filename, contents, file_id)