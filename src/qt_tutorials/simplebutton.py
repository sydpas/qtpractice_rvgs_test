from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Slot

@Slot()  # identifies the function as a slot, use to avoid weird behaviour
def say_hello():
    print("Button clicked, Hello!")

# create the Qt application
app = QApplication([])

button = QPushButton("Click me!")

# connect button to function
button.clicked.connect(say_hello)

button.show()
app.exec()