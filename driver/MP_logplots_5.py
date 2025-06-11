import sys

from mainpass_code.mp_logloader_1 import (mainpass_well)
from wellylassioqt.topsloader_2 import (top_load)
from mainpass_code.mp_assembly_3 import (organize_curves)
from wellylassioqt.wellinfo_4 import (horz_loader)

import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
    )

from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QApplication, QPushButton
    )


class WellLogPlotter(FigureCanvas):
    def __init__(self):
        self.fig, self.axes = plt.subplots(1, 1)
        super().__init__(self.fig)

        # loading data
        self.df = None
        self.well_tops_list = None
        self.ax_list = None
        self.col_list = None

        # calling functions...

        # for the tops
        self.show_tops = True  # have tops on
        self.tops_lines_list = []  # empty list to fill with tops

        # plotting logs and tops
        self.plotting_logs()

        # plotting horizontal well
        horz_df = horz_loader()
        self.plot_horizontal_well(horz_df)
        self.title_func()


    def plotting_logs(self):
        """
        This function plots the logs.
        """
        global current_ax
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
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
                    line = ax.axhline(y=y, color='red', lw=1.5, ls='-')  # tops
                    self.tops_lines_list.append(line) # add lines to the list
                    if i == 0:
                        top_name = ax.text(x=-20, y=y, s=horz, color='red', fontsize=8, ha='center', va='center')
                        self.tops_lines_list.append(top_name)  # add top names to the list

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
            # removing x-axis
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


    def toggle_tops(self):
        self.show_tops = not self.show_tops
        for pair in self.tops_lines_list:
            pair.set_visible(self.show_tops)
        self.draw()

    def plot_horizontal_well(self, horz_df):
        """
        This function creates a horizontal well overlay on top of the previous well logs.
        """
        # create an overlay axis, will have to fix width and height
        self.overlay_ax = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=None)  # l b width height
        self.overlay_ax.set_navigate(False)

        # make transparent background
        self.overlay_ax.patch.set_alpha(0)

        self.overlay_ax.set_xlabel('E-W Offset')
        # self.overlay_ax.set_xticks([])
        # self.overlay_ax.set_ylabel('')
        # self.overlay_ax.set_yticks([])

        # now to make sure the well spans the entire plot
        ymin, ymax = horz_df['SS'].min() - 100, horz_df['SS'].max() + 100
        # print(f'ymin: {ymin}, ymax: {ymax}')
        self.overlay_ax.set_ylim(ymin, ymax)

        xmin, xmax = horz_df['EW'].min() - 100, horz_df['EW'].max() + 100
        # print(f'xmin: {xmin}, xmax: {xmax}')
        self.overlay_ax.set_xlim(xmin, xmax)

        # get rid of window outline
        for spine in self.overlay_ax.spines.values():
            spine.set_alpha(0)

        self.overlay_ax.scatter(
            horz_df['EW'], horz_df['SS'],  # x, y
            color='darkred', marker='.', s=20, label='Horizontal Well')

        self.overlay_ax.axhline(0, 0, 1, color='darkblue', lw=1.5, ls='--', alpha=0.5, label='Sea Level')

        # find the point in the well that's closest to a chosen MD
        target_md = 910
        # subtracts target from every MD val, take abs val, find index where val is small, take entire row (iloc)
        closest_point = horz_df.iloc[(horz_df['MD'] - target_md).abs().idxmin()]

        # plotting target point
        self.overlay_ax.scatter(
            closest_point['EW'], closest_point['SS'],
            color='orange', edgecolors='red', marker='^', s=40, label='Target Point')

        self.overlay_ax.legend(loc='upper right', fontsize=7)

    def title_func(self):
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
        horz_df = horz_loader()

        uwi_title = horz_df['UWI'][0]
        plt.suptitle(f'Horizontal Well ({uwi_title}) on\n {loc} for {comp}', fontsize=10, fontweight='bold',
                     bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.6', alpha=0.8))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.setGeometry(100, 100, 800, 1100)  # width, height

        self.canvas = WellLogPlotter()
        self.toolbar = NavigationToolbar(self.canvas, self)
        # for the tops
        self.toggle_button = QPushButton('Toggle Tops')
        self.toggle_button.clicked.connect(self.canvas.toggle_tops)

        # styling the button
        self.toggle_button.setStyleSheet("""QPushButton {background-color: green;
        color: white;
        font: bold 12px;
        }""")

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.toggle_button)

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