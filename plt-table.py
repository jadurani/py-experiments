import matplotlib.pyplot as plt
from matplotlib import use, rcParams

rcParams['toolbar'] = 'None'
use('Qt5Agg')
plt.ion()

# data = [['', 'Col1', 'Col2', 'Col3'],
#         ['Row1', 1, 2, 3],
#         ['Row2', 4, 5, 6],
#         ['Row3', 7, 8, 9]]


data = [['', 'Displacement', 'Acceleration', '% of \nAllowable Drift'],
        ['X-Axis (ENE)', 1, 2, 3],
        ['Y-Axis (ENN)', 4, 5, 6],
        ['Z-Axis (ENZ)', 7, 8, 9]]

fig, ax = plt.subplots()

# Hide axes
ax.axis('off')
ax.axis('tight')

# Create table
table = ax.table(cellText=data, loc='center', colWidths=[0.25, 0.25, 0.25, 0.25])

# Set font size
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

# Show table
fig.canvas.start_event_loop(2)
