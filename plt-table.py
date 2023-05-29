import matplotlib.pyplot as plt
from matplotlib import use, rcParams

rcParams['toolbar'] = 'None'
use('Qt5Agg')
plt.ion()

YELLOW = '#FFA723'
RED = '#B80303'
BG_COLOR = '#EEEEEE'
WHITE = '#FFFFFF'

data = [['X-Axis (ENE)', '1 m', '2 m/s²', '3%'],
        ['Y-Axis (ENN)', '4 m', '5 m/s²', '6%'],
        ['Z-Axis (ENZ)', '7 m', '8 m/s²', '9%']]

cellColours =  [ \
  [BG_COLOR, BG_COLOR, BG_COLOR, BG_COLOR],
  [RED, RED, RED, RED],
  [BG_COLOR, BG_COLOR, BG_COLOR, BG_COLOR]
]

headers=['', 'Displacement', 'Acceleration', '% Drift']

fig, ax = plt.subplots()

# Hide axes
ax.axis('off')
ax.axis('tight')

# Create table
table = ax.table(
    cellText=data,
    loc='center',
    cellLoc='center',
    colLabels=headers,
    colColours=[BG_COLOR, BG_COLOR, BG_COLOR, BG_COLOR],
    cellColours=cellColours,
    colWidths=[0.25, 0.25, 0.25, 0.25]
  )

for cell in table.get_celld().values():
    cell.set_text_props(fontweight='demi')

# set color
table[2,0].set_text_props(color=WHITE)
table[2,1].set_text_props(color=WHITE)
table[2,2].set_text_props(color=WHITE)
table[2,3].set_text_props(color=WHITE)

# Set font size
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 2.5)

# Show table
fig.canvas.start_event_loop(5)
