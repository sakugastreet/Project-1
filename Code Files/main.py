from MW_Classes import *
# DB files really doesn't have anyhting yet, and may
# not depending on whether i switch from MySQL to SQLlite
import sys

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

main()