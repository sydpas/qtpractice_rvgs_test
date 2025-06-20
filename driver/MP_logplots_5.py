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
    QMainWindow, QVBoxLayout, QWidget, QApplication, QToolButton, QLabel
)

from PySide6.QtCore import Qt



class TitleBox(QLabel):
    def __init__(self,):
        super().__init__()

        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
        horz_df = horz_loader()

        uwi_title = horz_df['UWI'][0]
        title_text = f'Horizontal Well ({uwi_title}) on {loc} for {comp}  |  +{kb:.2f} m'

        self.setText(title_text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {background-color: #9ad1d4; color: black; font-weight: bold; font-size: 14px; padding: 2px;
                border: 2px solid #80ced7; border-radius: 4px;
            }""")
        self.setFixedHeight(30)  # or adjust to your liking


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

    def plotting_logs(self):
        """
        This function plots the logs.
        """
        global current_ax
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
        well_tops_list = top_load()
        ax_list, col_list = organize_curves()

        self.fig.clear()
        self.axes = self.fig.subplots(1, len(ax_list), sharey = True,
                                      gridspec_kw={'width_ratios': [1, 2, 1, 2, 2]})
        # subplots: gridbased, good for shared axes

        shade_list = ['#0c63e7', '#4c956c', '#f77f00']
        curve_counter = 0

        for i, (curves, ax) in enumerate(zip(ax_list, self.axes)):  # zip pairs up elements from 2 lists and brings them together
            ax = self.axes[i]
            top = well_tops_list[0]

            print(f'Plotting curve: {curves}...')

            for horz, depth in top.items():
                if pd.notna(depth):
                    y = float(depth)
                    line = ax.axhline(y=y, color='red', lw=1, ls='-')  # tops
                    self.tops_lines_list.append(line) # add lines to the list
                    if i == 0:
                        top_name = ax.text(x=0, y=y - 5, s=horz, color='red', fontsize=5, ha='right', va='center')
                        self.tops_lines_list.append(top_name)  # add top names to the list

            ax2 = ax.twiny()
            ax2.tick_params(axis='x', which='both', bottom=False, top=True, labelbottom=False, labeltop=True,
                            labelsize=6)

            for j, curve in enumerate(curves):
                unit = curve_unit_list.get(curve, '')
                print(f'unit for {curve} is {unit}')
                # unit labels
                ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=True, labeltop=False,
                               labelsize=6)

                if i != 0:
                    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)
                    ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False, labelright=False)

                if curve == 'GR':
                    df.plot(
                        x=curve, y='SUBSEA', color='black', ax=ax,
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.3, label='GR')
                    ax.fill_betweenx(df['SUBSEA'], df[curve], 75, facecolor='#ffc300', alpha=0.5)
                    ax.fill_betweenx(df['SUBSEA'], df[curve], 0, facecolor='white')
                    ax.axvline(75, color='black', linewidth=0.5, alpha=0.5)

                else:
                    shade = shade_list[curve_counter % len(shade_list)]
                    curve_counter += 1
                    # print(f'Shade for {curve}: {shade}')

                    next_ax = ax2 if j > 0 and ax2 else ax

                    df.plot(
                        x=curve, y='SUBSEA', color=shade, ax=next_ax,
                        linewidth=0.5, marker='o', markersize=0.1, alpha=0.3, label=curve)

                if j == 0:
                    ax.set_xlabel(f"{curve} ({unit})", fontsize=5, labelpad=5)
                else:
                    ax2.set_xlabel(f"{curve} ({unit})", fontsize=5, labelpad=5)


            if ax2:
                ax2.set_ylabel('Subsea for Logs (m)', color='darkred')
                ax2.tick_params(axis='y', colors='darkred')
            else:
                ax.set_ylabel('Subsea for Logs (m)', color='darkred')
                ax.tick_params(axis='y', colors='darkred')

            # adjusting proper y limits
            ax.set_ylim(df['SUBSEA'].min(), df['SUBSEA'].max())

            # ... and x limits
            ax.set_xlim(df[curves[0]].min(), df[curves[0]].max())
            if ax2:
                ax2.set_xlim(df[curves[-1]].min(), df[curves[-1]].max())

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
        columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
        horz_df = horz_loader()

        # create an overlay axis, will have to fix width and height
        self.horz_well_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=self.axes[0])  # l b width height
        self.horz_well_axes.set_navigate(False)

        # make transparent background
        self.horz_well_axes.patch.set_alpha(0)

        # get rid of window outline
        for spine in self.horz_well_axes.spines.values():
            spine.set_alpha(0)

        # x axis
        self.horz_well_axes.set_xlabel('E-W Offset')
        self.horz_well_axes.set_xticks([])

        # y axis label
        self.horz_well_axes.set_ylabel('Subsea for Horz Well (m)', color='darkblue')
        self.horz_well_axes.yaxis.set_label_position('right')
        self.horz_well_axes.yaxis.label.set_rotation(270)

        # y axis ticks
        self.horz_well_axes.yaxis.set_ticks_position('right')
        self.horz_well_axes.tick_params(axis='y', colors='darkblue')

        xmin, xmax = horz_df['EW'].min(), horz_df['EW'].max()
        # print(f'xmin for EW: {xmin}, xmax for EW: {xmax}')
        self.horz_well_axes.set_xlim(xmin, xmax)

        # sea level line
        self.horz_well_axes.axhline(0, 0, 1, color='#3a506b', lw=1.5, ls='--', alpha=0.6,
                                    label='Sea Level')

        for i in range(1, len(horz_df['SS'].values)):
            if horz_df['SS'].values[i] == horz_df['SS'].values[i - 1]:
                constant = horz_df['SS'].values[i]
                self.horz_well_axes.axhline(constant, 0, 1, color='#4A3728', lw=1.5, ls='-', alpha=0.8,
                                            label='Constant')
                break

        self.horz_well_axes.scatter(
                horz_df['EW'], horz_df['SS'],  # x, y
                color='#371D10', marker='.', s=20, label='Horizontal Well')

        self.horz_well_axes.legend(loc='upper right', fontsize=7)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Well Log Plotter")
        self.setGeometry(100, 100, 800, 1100)  # width, height

        self.well_plot = WellLogPlotter()
        self.title_box = TitleBox()
        self.toolbar = NavigationToolbar(self.well_plot, self)

        # for the tops
        self.toggle_button = QToolButton()
        self.toggle_button.setText('Toggle Tops')
        self.toggle_button.clicked.connect(self.well_plot.toggle_tops)
        self.toggle_button.setAutoRaise(False)
        # styling the button
        self.toggle_button.setStyleSheet("""
        QToolButton {background-color: #d00000; color: white; font: bold 12px; border: 2px white; border-radius: 4px;
            padding: 4px;
        }

        QToolButton:hover {background-color: #9d0208; color: white; font: bold 12px; border: 2px white; 
            border-radius: 4px; padding: 4px;
        }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        self.toolbar.addWidget(self.toggle_button)  # to put button beside toolbar
        layout.addWidget(self.title_box)
        layout.addWidget(self.well_plot)

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