import sys
from PySide6.QtWidgets import QApplication, QPushButton

def function():
    print("The function has been called!")

app = QApplication([])
button = QPushButton("Click me to call function!")
button.clicked.connect(function)

button.show()
sys.exit(app.exec())

