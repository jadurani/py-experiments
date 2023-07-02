import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import use
from matplotlib import rcParams
rcParams['toolbar'] = 'None'
import time

use('Qt5Agg')
plt.ion()

YELLOW = '#FFA723'
RED = '#B80303'
GREY = '#EEEEEE'
WHITE = '#FFFFFF'

def _set_up_axes(ax):
  ax.xaxis.set_tick_params(labelbottom=False)
  ax.yaxis.set_tick_params(labelleft=False)
  ax.set_position([0, 0.75, 1, 0.5])

  # Hide X and Y axes tick marks
  ax.set_xticks([])
  ax.set_yticks([])

  # hide spines
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_visible(False)

def init_alert_window(floor_num=1, disp_thresh=5, disp=2, intensity=2, drift_thresh=.7, acc=0.5):
  drift = disp/disp_thresh
  (banner_color, banner_text) = ('#FFA723', 'Earthquake Alert') if drift < drift_thresh else ('#B80303', '!!! EARTHQUAKE WARNING !!!')

  # Create a new figure
  fig = plt.figure(facecolor='#EEEEEE')
  fig.canvas.set_window_title(banner_text)

  ax = fig.add_subplot(111)
  _set_up_axes(ax)

  # set background color
  ax.set_facecolor(banner_color)
  # set banner text
  fig.text(0.5, 0.865, banner_text, ha='center', va='center', fontsize=24, color='#ffffff', weight="bold")

  drift_perc = drift * 100
  drift_info = ('Drift is %.2f%% of the threshold') % (drift_perc)

  if drift_perc.is_integer():
    drift_info = ('Drift is %d%% of the threshold') % (drift_perc)

  if floor_num > 1:
    fig.text(0.5, 0.55, drift_info, ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.45, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.35, ('Displacement %.2f m') % (disp), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.25, ('Acceleration %.2f m/s2') % (acc), ha='center', va='center', fontsize=18, weight="semibold")
  else:
    fig.text(0.5, 0.625, ('Intensity %d') % (intensity), ha='center', va='center', fontsize=24, weight="semibold")
    fig.text(0.5, 0.475, drift_info, ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.375, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.275, ('Displacement %.2f m') % (disp), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.175, ('Acceleration %.2f m/s2') % (acc), ha='center', va='center', fontsize=18, weight="semibold")

  fig.canvas.start_event_loop(1)

def init_table_window(floor_num=1, disp_thresh=5, disp=2, intensity=2, drift_thresh=.7, acc=0.5):
  drift = disp/disp_thresh
  (banner_color, banner_text) = ('#FFA723', 'Earthquake Alert') if drift < drift_thresh else ('#B80303', '!!! EARTHQUAKE WARNING !!!')

  # Create a new figure
  fig = plt.figure(facecolor='#EEEEEE')
  fig.set_size_inches(6, 5.5)
  fig.canvas.set_window_title(banner_text)

  ax = fig.add_subplot(211)
  _set_up_axes(ax)

  # set background color
  ax.set_facecolor(banner_color)
  # set banner text
  fig.text(0.5, 0.865, banner_text, ha='center', va='center', fontsize=24, color='#ffffff', weight="bold")

  bbox=None  # Adjust the values to move the table
  if floor_num > 1:
    fig.text(0.5, 0.625, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=24, weight="semibold")
    bbox=[-0.1, 0.15, 1.175, 1]  # Adjust the values to move the table
  else:
    fig.text(0.5, 0.65, ('Intensity %d') % (intensity), ha='center', va='center', fontsize=24, weight="semibold")
    fig.text(0.5, 0.55, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=18, weight="semibold")
    bbox=[-0.1, 0.075, 1.175, 1]  # Adjust the values to move the table

  # add details here
  data = [['X-Axis (ENE)', '1 m', '2 m/s²', '3%'],
          ['Y-Axis (ENN)', '4 m', '5 m/s²', '6%'],
          ['Z-Axis (ENZ)', '7 m', '8 m/s²', '9%']]

  cellColours =  [ \
    [GREY, GREY, GREY, GREY],
    [RED, RED, RED, RED],
    [GREY, GREY, GREY, GREY]
  ]

  headers=['', 'Displacement', 'Acceleration', '% Drift']
  colColours = [GREY, GREY, GREY, GREY]

  # Hide axes
  ax_bottom = fig.add_subplot(212)
  ax_bottom.axis('off')
  ax_bottom.axis('tight')

  # Create table
  table = ax_bottom.table(
      cellText=data,
      loc='center',
      cellLoc='center',
      colLabels=headers,
      colColours=colColours,
      cellColours=cellColours,
      bbox=bbox
    )

  for cell in table.get_celld().values():
      cell.set_text_props(fontweight='demi')

  # set color
  table[2,0].set_text_props(color=WHITE)
  table[2,1].set_text_props(color=WHITE)
  table[2,2].set_text_props(color=WHITE)
  table[2,3].set(facecolor='YELLOW')
  table[2,3].get_text().set_color(color=WHITE)

  # Set font size
  table.auto_set_font_size(False)
  table.set_fontsize(12)
  table.scale(1.2, 2.5)

  fig.canvas.start_event_loop(2)

# # Floor is 1, drift is below drift threshold of 0.5
# init_alert_window(floor_num=1, disp_thresh=5, disp=2, intensity=2, drift_thresh=0.5, acc=0.5)

# # Floor is 1, drift is above drift threshold of 0.5
# init_alert_window(floor_num=1, disp_thresh=5, disp=2.67, intensity=2, drift_thresh=0.5, acc=0.5)

# # Floor is above 1, drift is below drift threshold of 0.5
# init_alert_window(floor_num=8, disp_thresh=5, disp=2, intensity=2, drift_thresh=0.5, acc=0.5)

# # Floor is above 1, drift is above drift threshold of 0.5
# init_alert_window(floor_num=8, disp_thresh=5, disp=3, intensity=2, drift_thresh=0.5, acc=0.5)

# init_table_window(floor_num=1, disp_thresh=5, disp=3, intensity=2, drift_thresh=0.5, acc=0.5)
init_table_window(floor_num=8, disp_thresh=5, disp=3, intensity=2, drift_thresh=0.5, acc=0.5)