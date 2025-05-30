import sys
from PySide6.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout


class Form(QDialog):

    # parent = None means dialog window can work on its own
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)  # this makes sure the dialog is initialized properly

        self.setWindowTitle("My Form")  # sets the title of the window

        self.edit = QLineEdit("Replace me with your name!")
        self.button = QPushButton("Say hello!")

        # organize the widgets
        layout = QVBoxLayout(self)
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.greetings)

    def greetings(self):
        print(f'Hello {self.edit.text()}!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())