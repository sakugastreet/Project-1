from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamic Grid Layout Example")
        self.setGeometry(100, 100, 600, 400)
        
        # Create a grid layout
        grid_layout = QGridLayout()
        
        # Add some buttons with different row/column spans
        button1 = QPushButton("Folder 1")
        button2 = QPushButton("Folder 2")
        button3 = QPushButton("File 1")
        button4 = QPushButton("File 2")
        button5 = QPushButton("File 3")
        button6 = QPushButton("File 4")
        
        grid_layout.addWidget(button1, 0, 0, 1, 2)  # Span 1 row, 2 columns
        grid_layout.addWidget(button2, 0, 2, 1, 1)
        grid_layout.addWidget(button3, 1, 0)
        grid_layout.addWidget(button4, 1, 1)
        grid_layout.addWidget(button5, 1, 2)
        grid_layout.addWidget(button6, 2, 0, 1, 3)  # Span 1 row, 3 columns
        
        # Set stretch factors for rows and columns
        for i in range(3):
            grid_layout.setRowStretch(i, 1)
            grid_layout.setColumnStretch(i, 1)
        
        self.setLayout(grid_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
