# def scale_bar_md(self):
#     """
#     This function creates a scale bar to overlay the plots.
#     """
#     columns, non_depth_curves, curve_unit_list, df, loc, comp, kb = mainpass_well()
#     horz_df = horz_loader()
#
#     self.scale_bar_axes = self.fig.add_axes((0.125, 0.109, 0.774, 0.77), sharey=self.axes[0])  # l b width height
#
#     # add_axes: good for manual locations
#     self.scale_bar_axes.set_navigate(True)
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
#     midpoint = (df['DEPTH'].max() - df['DEPTH'].min()) /2
#     mp_pos_1 = midpoint + 1
#     mp_neg_1 = midpoint - 1
#
#     self.horz_lines_list.append(self.scale_bar_axes.axhline(y=midpoint, xmin=0, xmax=1, color='black', linewidth = 2))
#     self.vert_lines_list.append(self.scale_bar_axes.axvline(0, mp_neg_1, mp_pos_1, color='black', linewidth = 3))
#
#     count = 0
#     while count <= horz_df['MD'].max():
#         self.vert_lines_list.append(self.scale_bar_axes.axvline(count, 0.49, 0.51, color='purple',
#                                                                 linewidth=2))
#         self.text_lines_list.append(self.scale_bar_axes.text(count, (midpoint + 30), f'{count} m',
#                                                     va='top', ha='center', color='purple'))
#
#         count += 500
#
#     self.vert_lines_list.append(self.scale_bar_axes.axvline(horz_df['MD'].max(), 0.49, 0.51,
#                                                    color='black', linewidth = 3))
#
#     self.text_lines_list.append(self.scale_bar_axes.text(horz_df['MD'].max() + 10, (midpoint + 20),
#                                                          f'{horz_df['MD'].max()} m'))
#     self.text_lines_list.append(self.scale_bar_axes.text(horz_df['MD'].max() + 10, (midpoint - 30), 'MD'))
#
# def toggle_scale_bar(self):
#     self.show_scale_bar = not self.show_scale_bar
#     for i in [self.vert_lines_list, self.horz_lines_list, self.text_lines_list]:
#         for j in i:
#             j.set_visible(self.show_scale_bar)
#     self.draw()

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


# # for the scale bar
# self.toggle_button_b = QToolButton()
# self.toggle_button_b.setText('Toggle Scale Bar')
# self.toggle_button_b.clicked.connect(self.canvas.toggle_scale_bar)
# self.toggle_button_b.setAutoRaise(False)
# # styling the button
# self.toggle_button_b.setStyleSheet("""
# QToolButton {background-color: purple; color: white; font: bold 12px; border: 2px dark purple;
#     border-radius: 4px; padding: 4px;
# }
#
# QToolButton:hover {background-color: black; color: white; font: bold 12px; border: 2px solid purple;
#     border-radius: 4px;padding: 4px;
# }
# """)