import sys

from wellylassioqt.logloader_1 import (highres_well)
from wellylassioqt.topsloader_2 import (top_load)

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
    )

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QApplication
    )

# create the plot widget
class WellPlotCanvas(FigureCanvas):
    def __init__(self, parent=None):  # constructor
        self.fig, self.axes = plt.subplots(1,1, figsize=(10,14))
        self.fig.subplots_adjust(
            left=0.043,
            right=0.987,
            top=0.941,
            bottom=0.089,
            hspace=0.2, wspace=0.267,
        )  # values based on tight layout
        super().__init__(self.fig)  # initialize as a widget

    # plotting the logs function
    def plot_logs(self):
        columns, non_depth_curves, curve_unit_list, df = highres_well()
        well_tops_list = top_load()

        self.fig.clear()
        self.axes = self.fig.subplots(1, columns, sharey=True)


        for i, curve in enumerate(non_depth_curves):
            ax = self.axes[i]
            unit = curve_unit_list[i + 1]
            top = well_tops_list[0]

            # plot tops
            for horz, depth in top.items():
                if pd.notna(depth):
                    y = float(depth)
                    ax.axhline(y=y, color='red', lw=1.5, ls='-')

            if curve != 'GR' and curve != 'PE':
                # plotting curves
                df.plot(
                    x=curve, y='DEPTH', color='black', title=curve, ax=ax, xlabel=unit,
                    linewidth=0.5, marker='o', markersize='0.2', alpha=0.5, legend=False)
                ax.set_title(curve, fontweight='bold', fontsize=14)
                ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())  # ensures the curves have the right limits

            elif curve == 'GR':
                df.plot(
                    x='GR', y='DEPTH', color='black', title=curve, ax=ax, xlabel=unit,
                    linewidth=0.5, marker='o', markersize='0.2', alpha=0.5, legend=False)
                ax.fill_betweenx(df['DEPTH'], df['GR'], 75, facecolor='yellow', alpha=0.8)
                ax.fill_betweenx(df['DEPTH'], df['GR'], 0, facecolor='white')
                ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)
                ax.set_title(curve, fontweight='bold', fontsize=14)
                ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())

            elif curve == 'PE':
                df.plot(
                    x='PE', y='DEPTH', color='black', title=curve, ax=ax, xlabel=unit,
                    linewidth=0.5, marker='o', markersize='0.2', alpha=0.5, legend=False)
                ax.set_title(curve, fontweight='bold', fontsize=14)
                ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())

# making the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.resize(1250, 700)

        # create the plot area and a toolbar
        self.canvas = WellPlotCanvas(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # create layout for the plot area and toolbar
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        # 'wrap' everything
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # trigger plot
        self.canvas.plot_logs()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()