import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem

colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF")]

def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i + 2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])

app = QApplication([])
table = QTableWidget()

#initialize table
table.setRowCount(len(colors))
table.setColumnCount(len(colors[0]) + 1)
table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])

# fill in table
for i, (name, code) in enumerate(colors):
    item_name = QTableWidgetItem(name)
    item_code = QTableWidgetItem(code)
    item_color = QTableWidgetItem()  # empty because will be filled with colour
    item_color.setBackground(get_rgb_from_hex(code))
    # add all items to right row and column
    table.setItem(i, 0, item_name)
    table.setItem(i, 1, item_code)
    table.setItem(i, 2, item_color)

table.show()
sys.exit(app.exec())
