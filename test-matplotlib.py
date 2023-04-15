import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import use
from matplotlib import rcParams
rcParams['toolbar'] = 'None'
import time

use('Qt5Agg')
plt.ion()

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

def init_alert_window(floorNum=1, bldgThresh=5, disp=2, intensity=2, driftThresh=.7, acc=0.5):
  drift = disp/bldgThresh
  (banner_color, banner_text) = ('#FFA723', 'Earthquake Alert') if drift < driftThresh else ('#B80303', '!!! EARTHQUAKE WARNING !!!')

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

  if floorNum > 1:
    fig.text(0.5, 0.55, drift_info, ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.45, ('FLOOR %s') % (floorNum), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.35, ('Displacement %.2f m') % (disp), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.25, ('Acceleration %.2f m/s2') % (acc), ha='center', va='center', fontsize=18, weight="semibold")
  else:
    fig.text(0.5, 0.625, ('Intensity %d') % (intensity), ha='center', va='center', fontsize=24, weight="semibold")
    fig.text(0.5, 0.475, drift_info, ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.375, ('FLOOR %s') % (floorNum), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.275, ('Displacement %.2f m') % (disp), ha='center', va='center', fontsize=18, weight="semibold")
    fig.text(0.5, 0.175, ('Acceleration %.2f m/s2') % (acc), ha='center', va='center', fontsize=18, weight="semibold")

  fig.canvas.start_event_loop(1)


# Floor is 1, drift is below drift threshold of 0.5
init_alert_window(floorNum=1, bldgThresh=5, disp=2, intensity=2, driftThresh=0.5, acc=0.5)

# Floor is 1, drift is above drift threshold of 0.5
init_alert_window(floorNum=1, bldgThresh=5, disp=2.67, intensity=2, driftThresh=0.5, acc=0.5)

# Floor is above 1, drift is below drift threshold of 0.5
init_alert_window(floorNum=8, bldgThresh=5, disp=2, intensity=2, driftThresh=0.5, acc=0.5)

# Floor is above 1, drift is above drift threshold of 0.5
init_alert_window(floorNum=8, bldgThresh=5, disp=3, intensity=2, driftThresh=0.5, acc=0.5)