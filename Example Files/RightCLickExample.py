from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Right-Click Example")
        self.resize(300, 200)
        
        # Enable the custom context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos: QPoint):
        context_menu = QMenu(self)
        
        action1 = QAction("Action 1", self)
        action2 = QAction("Action 2", self)
        
        context_menu.addAction(action1)
        context_menu.addAction(action2)
        
        # Show the context menu at the cursor's position
        context_menu.exec_(self.mapToGlobal(pos))

if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec()
