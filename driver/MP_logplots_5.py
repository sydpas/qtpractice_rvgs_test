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
    QMainWindow, QVBoxLayout, QWidget, QApplication, QToolButton
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

        # for the tops button
        self.show_tops = True  # have tops on
        self.tops_lines_list = []  # empty list to fill with tops

        # for the scale button
        self.show_scale_bar = True
        self.horz_lines_list = []
        self.vert_lines_list = []
        self.text_lines_list = []

        # plotting logs and tops
        self.plotting_logs()

        # plotting horizontal well
        self.plot_horizontal_well()

        self.title_func()
        self.scale_bar_md()
        # self.scale_bar()

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
        # subplots: gridbased, good for shared axes

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
                        top_name = ax.text(x=-20, y=y, s=horz, color='red', fontsize=4, ha='center', va='center')
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
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.3, label='GR')
                    ax.fill_betweenx(df['DEPTH'], df[curve], 75, facecolor='yellow', alpha=0.5)
                    ax.fill_betweenx(df['DEPTH'], df[curve], 0, facecolor='white')
                    ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)

                else:

                    shade = shade_list[curve_counter % len(shade_list)]
                    curve_counter += 1
                    print(f'Shade for {curve}: {shade}')

                    next_ax = ax2 if j > 0 and ax2 else ax

                    df.plot(
                        x=curve, y='DEPTH', color=shade, ax=next_ax,
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.3, label=curve)

            # adjusting proper y limits and x limits
            ax.set_ylim(df['DEPTH'].min(), df['DEPTH'].max())
            # print(f"yaxis values (depth): {ax.get_ylim()}")
            ax.set_ylabel('Vertical Depth (m)')
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

    def plot_horizontal_well(self):
        """
        This function creates a horizontal well overlay on top of the previous well logs.
        """
        horz_df = horz_loader()

        # create an overlay axis, will have to fix width and height
        self.horz_well_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=None)  # l b width height
        self.horz_well_axes.set_navigate(False)

        # make transparent background
        self.horz_well_axes.patch.set_alpha(0)

        self.horz_well_axes.set_xlabel('E-W Offset')
        self.horz_well_axes.set_xticks([])
        self.horz_well_axes.set_ylabel('')
        self.horz_well_axes.set_yticks([])

        # now to make sure the well spans the entire plot
        ymin, ymax = horz_df['SS'].min() - 100, horz_df['SS'].max() + 100
        # print(f'yaxis min (ss): {ymin}, max (ss): {ymax}')
        self.horz_well_axes.set_ylim(ymin, ymax)

        xmin, xmax = horz_df['EW'].min() - 100, horz_df['EW'].max() + 100
        # print(f'xmin: {xmin}, xmax: {xmax}')
        self.horz_well_axes.set_xlim(xmin, xmax)

        # get rid of window outline
        for spine in self.horz_well_axes.spines.values():
            spine.set_alpha(0)

        self.horz_well_axes.scatter(
            horz_df['EW'], horz_df['SS'],  # x, y
            color='darkred', marker='.', s=20, label='Horizontal Well')

        self.horz_well_axes.axhline(0, 0, 1, color='darkblue', lw=1.5, ls='--', alpha=0.5, label='Sea Level')

        # find the point in the well that's closest to a chosen MD
        target_md = 2000
        # subtracts target from every MD val, take abs val, find index where val is small, take entire row (iloc)
        closest_point = horz_df.iloc[(horz_df['MD'] - target_md).abs().idxmin()]

        # plotting target point
        self.horz_well_axes.scatter(
            closest_point['EW'], closest_point['SS'],
            color='orange', edgecolors='red', marker='^', s=40, label='Target Point')

        self.horz_well_axes.legend(loc='upper right', fontsize=7)

    def title_func(self):
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
        horz_df = horz_loader()

        uwi_title = horz_df['UWI'][0]
        plt.suptitle(f'Horizontal Well ({uwi_title}) on\n {loc} for {comp}\n +{kb:.2f}m', fontsize=8, fontweight='bold',
                     bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='square,pad=0.6', alpha=0.8))


    def scale_bar_md(self):
        """
        This function creates a scale bar to overlay the plots.
        """
        horz_df = horz_loader()

        # creating a new overlay for the scale bar
        self.scale_bar_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=None)  # l b width height
        # add_axes: good for manual locations
        self.scale_bar_axes.set_navigate(False)

        # make transparent background
        self.scale_bar_axes.patch.set_alpha(0)

        self.scale_bar_axes.set_xlabel('')
        self.scale_bar_axes.set_xticks([])
        self.scale_bar_axes.set_ylabel('')
        self.scale_bar_axes.set_yticks([])

        # get rid of window outline
        for spine in self.scale_bar_axes.spines.values():
            spine.set_alpha(0)

        self.scale_bar_axes.set_xlim(0, horz_df['MD'].max())

        self.horz_lines_list.append(self.scale_bar_axes.axhline(y=0.5, xmin=0, xmax=1, color='black', linewidth = 2))
        self.vert_lines_list.append(self.scale_bar_axes.axvline(0, 0.49, 0.51, color='black', linewidth = 3))

        count = 0
        while count <= horz_df['MD'].max():
            self.vert_lines_list.append(self.scale_bar_axes.axvline(count, 0.49, 0.51, color='purple', linewidth=2))
            self.text_lines_list.append(self.scale_bar_axes.text(count, 0.49, f'{count} m',
                                                        va='top', ha='center', color='purple'))

            count += 500

        self.vert_lines_list.append(self.scale_bar_axes.axvline(horz_df['MD'].max(), 0.49, 0.51,
                                                       color='black', linewidth = 3))
        self.text_lines_list.append(self.scale_bar_axes.text(horz_df['MD'].max() + 10, 0.49, f'{horz_df['MD'].max()} m'))

        self.text_lines_list.append(self.scale_bar_axes.text(horz_df['MD'].max() + 10, 0.53, 'MD'))

    def toggle_scale_bar(self):
        self.show_scale_bar = not self.show_scale_bar
        for i in [self.vert_lines_list, self.horz_lines_list, self.text_lines_list]:
            for j in i:
                j.set_visible(self.show_scale_bar)
        self.draw()

    # def scale_bar(self):
    #     columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
    #     horz_df = horz_loader()
    #
    #     d_ymin, d_ymax = df['DEPTH'].min(), df['DEPTH'].max()
    #     d_diff = d_ymax - d_ymin
    #
    #     s_ymin, s_ymax = horz_df['SS'].min(), horz_df['SS'].max()
    #     s_diff = s_ymax - s_ymin
    #
    #     print(f'yaxis min (depth): {d_ymin}, max (depth): {d_ymax}')
    #     print(f'yaxis min (ss): {s_ymin}, max (ss): {s_ymax}')
    #     print(f'depth difference: {d_diff} meters')
    #     print(f'subsea difference: {s_diff} meters')
    #
    #     # creating a new overlay for the scale bar
    #     self.scale_bar_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey = None)  # l b width height
    #     self.scale_bar_axes.set_navigate(False)
    #
    #     # make transparent background
    #     self.scale_bar_axes.patch.set_alpha(0)
    #
    #     self.scale_bar_axes.set_xlabel('')
    #     self.scale_bar_axes.set_xticks([])
    #     self.scale_bar_axes.set_ylabel('')
    #     self.scale_bar_axes.set_yticks([])
    #
    #     # get rid of window outline
    #     for spine in self.scale_bar_axes.spines.values():
    #         spine.set_alpha(0)
    #
    #     self.scale_bar_axes.set_xlim(0, horz_df['MD'].max())
    #
    #     self.scale_bar_axes.axhline(y=0.5, xmin=0, xmax=1, color='black', linewidth = 2)  # horz line
    #     self.scale_bar_axes.axvline(0, 0.49, 0.51, color='black', linewidth = 3)
    #
    #     ratio_scale = 1
    #     print('beginning while loop...')
    #     while (ratio_scale + 100) <= horz_df['SS'].max():
    #         print(f'ratio scale: {ratio_scale}')
    #
    #         math_d_div_ss = (d_diff * ratio_scale) / s_diff
    #         decimal = math_d_div_ss % 1
    #         scale_length = math_d_div_ss - decimal
    #         print(f'scale length: {scale_length} meters')
    #
    #         print(f'subsea to depth ratio: {ratio_scale}:{scale_length} meters')
    #
    #
    #         # self.scale_bar_axes.axvline(ratio_scale, 0.49, 0.51, color='purple', linewidth = 2)
    #         # self.scale_bar_axes.text(ratio_scale, 0.51, f'{ratio_scale} m', va='bottom', ha='center', color='purple')
    #
    #         self.scale_bar_axes.axvline(scale_length, 0.49, 0.51, color='brown', linewidth = 2)
    #         self.scale_bar_axes.text(scale_length, 0.49, f'{scale_length} m', va='top', ha='center', color='brown')
    #
    #         ratio_scale = ratio_scale + 100
    #         print(f'updated ratio scale: {ratio_scale} meters')
    #
    #     self.scale_bar_axes.axvline(horz_df['SS'].max(), 0.49, 0.51, color='black', linewidth = 3)
    #     self.scale_bar_axes.text(horz_df['SS'].max() + 10, 0.49, f'{horz_df['SS'].max()} m')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.setGeometry(100, 100, 800, 1100)  # width, height

        self.canvas = WellLogPlotter()
        self.toolbar = NavigationToolbar(self.canvas, self)

        # for the tops
        self.toggle_button = QToolButton()
        self.toggle_button.setText('Toggle Tops')
        self.toggle_button.clicked.connect(self.canvas.toggle_tops)
        self.toggle_button.setAutoRaise(False)
        # styling the button
        self.toggle_button.setStyleSheet("""
        QToolButton {background-color: red; color: white; font: bold 12px; border: 2px dark red; border-radius: 4px;
            padding: 4px;
        }

        QToolButton:hover {background-color: black; color: white; font: bold 12px; border: 2px solid red; 
            border-radius: 4px; padding: 4px;
        }
        """)

        # for the scale bar
        self.toggle_button_b = QToolButton()
        self.toggle_button_b.setText('Toggle Scale Bar')
        self.toggle_button_b.clicked.connect(self.canvas.toggle_scale_bar)
        self.toggle_button_b.setAutoRaise(False)
        # styling the button
        self.toggle_button_b.setStyleSheet("""
        QToolButton {background-color: purple; color: white; font: bold 12px; border: 2px dark purple;
            border-radius: 4px; padding: 4px;
        }

        QToolButton:hover {background-color: black; color: white; font: bold 12px; border: 2px solid purple;
            border-radius: 4px;padding: 4px;
        }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        self.toolbar.addWidget(self.toggle_button)  # to put button beside toolbar
        self.toolbar.addWidget(self.toggle_button_b)
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