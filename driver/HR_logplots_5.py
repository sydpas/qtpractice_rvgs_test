import sys

from highres_code.hr_logloader_1 import (highres_well)
from wellylassioqt.topsloader_2 import (top_load)
from highres_code.hr_assembly_3 import (organize_curves)
from wellylassioqt.wellinfo_4 import (horz_loader)

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

        self.plotting_logs()

        horz_df = horz_loader()
        self.plot_horizontal_well(horz_df)


    def plotting_logs(self):
        """
        This function plots the logs.
        """
        global current_ax
        columns, non_depth_curves, curve_unit_list, df, loc, comp = highres_well()
        well_tops_list = top_load()
        ax_list, col_list = organize_curves()

        self.fig.clear()
        self.axes = self.fig.subplots(1, len(ax_list), sharey = True, gridspec_kw={'width_ratios': [1, 2, 1, 2, 2]})

        # pos = self.axes[0].get_position()
        # print(f"for first axis, x0: {pos.x0}, y0: {pos.y0}, width: {pos.width}, height: {pos.height}")
        # pos = self.axes[1].get_position()
        # print(f"for second axis, x0: {pos.x0}, y0: {pos.y0}, width: {pos.width}, height: {pos.height}")
        # pos = self.axes[2].get_position()
        # print(f"for third axis, x0: {pos.x0}, y0: {pos.y0}, width: {pos.width}, height: {pos.height}")
        # pos = self.axes[3].get_position()
        # print(f"for fourth axis, x0: {pos.x0}, y0: {pos.y0}, width: {pos.width}, height: {pos.height}")
        # pos = self.axes[4].get_position()
        # print(f"for fifth axis, x0: {pos.x0}, y0: {pos.y0}, width: {pos.width}, height: {pos.height}")

        shade_list = ['blue', 'green', 'orange']
        curve_counter = 0

        for i, (curves, ax) in enumerate(zip(ax_list, self.axes)):  # zip pairs up elements from 2 lists and brings them together
            ax = self.axes[i]
            top = well_tops_list[0]

            print(f'Plotting curve: {curves}...')

            for horz, depth in top.items():
                if pd.notna(depth):
                    y = float(depth)
                    ax.axhline(y=y, color='red', lw=1.5, ls='-')  # tops
                    if i == 0:
                        ax.text(x=-20, y=y, s=horz, color='red', fontsize=8, ha='center', va='center')  # top names

            ax2 = ax.twiny()
            ax2.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)

            for j, curve in enumerate(curves):

                ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False, labeltop=False)
                if i != 0:
                    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
                    ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)

                if curve == 'GR':
                    df.plot(
                        x=curve, y='DEPTH', color='black', ax=ax,
                        linewidth=0.5, marker='o', markersize=0.2, alpha=0.5, label='GR')
                    ax.fill_betweenx(df['DEPTH'], df[curve], 75, facecolor='yellow', alpha=0.5)
                    ax.fill_betweenx(df['DEPTH'], df[curve], 0, facecolor='white')
                    ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)

                else:

                    shade = shade_list[curve_counter % len(shade_list)]
                    curve_counter += 1
                    print(f'Shade for {curve}: {shade}')

                    next_ax = ax2 if j > 0 and ax2 else ax

                    df.plot(
                        x=curve, y='DEPTH', color=shade, ax=next_ax, label=curve,
                        linewidth=0.5, marker='o', markersize=0.2, alpha=0.5)

            # adjusting proper y limits and x limits
            ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())
            ax.set_ylabel('Depth (m) for the Well Logs')
            ax.invert_yaxis()

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

            ax.grid(True, linestyle='-', alpha=0.4, linewidth=0.5)
            ax.set_title(' and '.join(curves), fontsize=10)

        plt.suptitle(f'{loc}, {comp}', fontsize=16, fontweight='bold',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.8', alpha=0.8))

    def plot_horizontal_well(self, horz_df):
        """
        This function creates a horizontal well overlay on top of the previous well logs.
        """
        # create an overlay axis, will have to fix height + width
        self.overlay_ax = self.fig.add_axes([0.125, 0.109, 0.774, 0.77], sharey=None)  # l b width height

        # make transparent background
        self.overlay_ax.patch.set_alpha(0)

        self.overlay_ax.set_xlabel('E-W Offset')
        # self.overlay_ax.set_xticks([])
        self.overlay_ax.set_ylabel('')
        self.overlay_ax.set_yticks([])

        # now to make sure the well spans the entire plot
        ymin, ymax = horz_df['TVD'].min(), horz_df['TVD'].max() + 100
        self.overlay_ax.set_ylim(ymin, ymax)
        self.overlay_ax.invert_yaxis()

        xmin, xmax = horz_df['EW'].min() - 50, horz_df['EW'].max()
        # print(f'xmin: {xmin}, xmax: {xmax}')
        self.overlay_ax.set_xlim(xmin, xmax)

        # get rid of window outline
        for spine in self.overlay_ax.spines.values():
            spine.set_alpha(0)

        self.overlay_ax.scatter(
            horz_df['EW'], horz_df['TVD'],  # x, y
            color='darkred', marker='.', s=20)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.setGeometry(100, 100, 800, 1100)  # width, height

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