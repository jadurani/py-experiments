import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import use
from matplotlib import rcParams
rcParams['toolbar'] = 'None'

use('Qt5Agg')
plt.ion()


def _set_up_axes(ax):
  ax.xaxis.set_tick_params(labelbottom=False)
  ax.yaxis.set_tick_params(labelleft=False)
  # ax.set_position([0, 0.75, 1, 0.5])

  # Hide X and Y axes tick marks
  ax.set_xticks([])
  ax.set_yticks([])

  # hide spines
  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_visible(False)


# Load the SVG image using mpimg
image = mpimg.imread('./images/relay-closed-yellow.png')

# Create a figure and axes
fig = plt.figure(facecolor='#EEEEEE')
ax = fig.add_subplot(212)
ax.set_facecolor('#EEEEEE')
# [left, bottom, width, height]
ax.set_position([0.25, 0, 0.5, 0.5])
_set_up_axes(ax)

# Calculate the desired width and height for resizing
desired_width = 100  # Set your desired width in pixels
aspect_ratio = image.shape[1] / image.shape[0]
desired_height = desired_width / aspect_ratio

# Plot the resized image on the axes
ax.imshow(image, interpolation='bilinear', extent=(0, desired_width, 0, desired_height))

# Show the plot
fig.canvas.start_event_loop(5)