from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])
label = QLabel("<font color=blue size=40>Hello World!</font>")
label.show()
app.exec()  # executing the code

