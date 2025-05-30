import sys
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Well Tops")

        # the menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(exit_action)

        # status bar
        self.status = self.statusBar()
        self.status.showMessage("Data plotted...")

        # window dim
        geometry = self.screen().availableGeometry()
        self.setFixedSize(int(geometry.width() * 0.8), int(geometry.height() * 0.7))

app = QApplication([])
window = MainWindow()
window.show()
sys.exit(app.exec())
