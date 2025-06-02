import sys

from highres_code.hr_logloader_1 import (highres_well)
from wellylassioqt.topsloader_2 import (top_load)
from highres_code.hr_assembly_3 import (organize_curves)

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
    )

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QApplication
    )

class WellLogPlotter(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.axes = plt.subplots(1, 1)
        super().__init__(self.fig)

        # loading data
        self.df = None
        self.well_tops_list = None
        self.ax_list = None
        self.col_list = None

        self.load_data()
        self.plotting_logs()

    def load_data(self):
        _, _, _, self.df, loc, comp = highres_well()
        self.well_tops_list = top_load()
        self.ax_list, self.col_list = organize_curves()

    def plotting_logs(self):
        """
        This function plots the logs.
        """
        global current_ax
        columns, non_depth_curves, curve_unit_list, df, loc, comp = highres_well()
        well_tops_list = top_load()
        ax_list, col_list = organize_curves()

        self.fig.clear()
        self.axes = self.fig.subplots(1, len(ax_list), sharey = True, gridspec_kw={'width_ratios': [len(ax_list[0]), len(ax_list[1]), len(ax_list[2]),
                                                               len(ax_list[3]), len(ax_list[4])]})


        for i, (curves, ax) in enumerate(zip(ax_list, self.axes)):  # zip pairs up elements from 2 lists and brings them together
            ax = self.axes[i]
            unit = curve_unit_list[i+1]
            top = well_tops_list[0]

            for horz, depth in top.items():
                if pd.notna(depth):
                    y = float(depth)
                    ax.axhline(y=y, color='red', lw=1.5, ls='-')  # tops
                    if i == 0:
                        ax.text(x=-20, y=y, s=horz, color='red', fontsize=8, ha='center', va='center')  # top names

            if i == 3 and len(curves) == 3:  # handling the fourth group
                ax2 = ax.twiny()
                ax3 = ax.twiny()

                for j, curve in enumerate(curves):
                    print(f'Plotting curve: {curve}...')
                    if curve == 'PE':
                        current_ax = ax
                    elif curve == 'RHOB':
                        current_ax = ax2
                    elif curve == 'GR':
                        current_ax = ax3

                    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
                    ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
                    ax3.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
                    ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False, labelright=False)
                    ax2.tick_params(axis='y', which='both', right=False, left=False, labelleft=False, labelright=False)
                    ax3.tick_params(axis='y', which='both', right=False, left=False, labelleft=False, labelright=False)

                    if curve == 'GR':
                        df.plot(
                            x='GR', y='DEPTH', color='black', ax=current_ax,
                            linewidth=0.5, marker='o', markersize=0.2, alpha=0.5, label='GR')

                        gr_min = df[curve].min()
                        gr_max = df[curve].max()

                        current_ax.fill_betweenx(df['DEPTH'], df[curve], 75,
                                                 where=(df[curve] <= 75),
                                                 facecolor='yellow', alpha=0.5)

                        current_ax.fill_betweenx(df['DEPTH'], df[curve], gr_max,
                                                 where=(df[curve] > 75),
                                                 facecolor='white', alpha=0.5)

                        current_ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)
                        current_ax.set_xlim(gr_min, gr_max)

                        current_ax.set_xlabel('')  # removing x label

                    elif current_ax == ax:
                        df.plot(
                            x=curve, y='DEPTH', color='blue', ax=current_ax, label=curve,
                            linewidth=0.5, marker='o', markersize=0.2, alpha=0.5)

                        current_ax.set_xlabel('')  # removing x label

                    elif current_ax == ax2:
                        df.plot(
                            x=curve, y='DEPTH', color='green', ax=current_ax, label=curve,
                            linewidth=0.5, marker='o', markersize=0.2, alpha=0.5)

                        current_ax.set_xlabel('')  # removing x label


                # adjusting proper y limits
                ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())

                # x axis limits
                ax.set_xlim(df[curves[0]].min(), df[curves[0]].max())
                ax2.set_xlim(df[curves[1]].min(), df[curves[1]].max())
                ax3.set_xlim(df[curves[2]].min(), df[curves[2]].max())

                # combining the legends and putting bottom left
                lines_1, labels_1 = ax.get_legend_handles_labels()
                lines_2, labels_2 = ax2.get_legend_handles_labels()
                lines_3, labels_3 = ax3.get_legend_handles_labels()
                ax.legend(lines_1 + lines_2 + lines_3, labels_1 + labels_2 + labels_3, loc='lower left', fontsize=6)
                ax2.get_legend().remove() if ax2.get_legend() else None
                ax3.get_legend().remove() if ax3.get_legend() else None

                ax.grid(True, linestyle='-', alpha=0.3, linewidth=0.5)
                ax.set_title(' and '.join(curves), fontsize=10)

                continue

            ax2 = ax.twiny()
            ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)

            for j, curve in enumerate(curves):
                print(f'Plotting group: {curves}...')

                ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
                if i != 0:
                    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)

                if curve == 'GR':
                    df.plot(
                        x=curve, y='DEPTH', color='black', ax=ax,
                        linewidth=0.5, marker='o', markersize=0.2, alpha=0.5, label='GR')
                    ax.fill_betweenx(df['DEPTH'], df[curve], 75, facecolor='yellow', alpha=0.5)
                    ax.fill_betweenx(df['DEPTH'], df[curve], 0, facecolor='white')
                    ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)

                else:
                    next_ax = ax2 if j > 0 and ax2 else ax
                    df.plot(
                        x=curve, y='DEPTH', color='blue', ax=next_ax, label=curve,
                        linewidth=0.5, marker='o', markersize=0.2, alpha=0.5)

            # adjusting proper y limits and x limits
            ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())
            ax.set_xlim(df[curves[0]].min(), df[curves[0]].max())
            if ax2:
                ax2.set_xlim(df[curves[-1]].min(), df[curves[-1]].max())

            # removing x axis
            ax.set_xlabel('')
            if ax2:
                ax2.set_xlabel('')

            # combining the legends and putting bottom left
            if ax2:
                lines_1, labels_1 = ax.get_legend_handles_labels()
                lines_2, labels_2 = ax2.get_legend_handles_labels()
                ax.legend(lines_1 + lines_2, labels_1 + labels_2, loc='lower left', fontsize=6)
                ax2.get_legend().remove() if ax2.get_legend() else None

            ax.grid(True, linestyle='-', alpha=0.3, linewidth=0.5)
            ax.set_title(' and '.join(curves), fontsize=10)

        plt.suptitle(f'{loc}, {comp}', fontsize=16, fontweight='bold',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.8', alpha=0.8))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.setGeometry(100, 100, 700, 1200)

        self.canvas = WellLogPlotter(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)


        # 'wrap' everything
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()