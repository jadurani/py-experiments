import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import use
from matplotlib import rcParams
rcParams['toolbar'] = 'None'

use('Qt5Agg')
plt.ion()

# border_states
CLOSED_YELLOW = 'closed-yellow'
CLOSED_RED = 'closed-red'
OPEN = 'open'

IMAGE_LOCS = {
  'closed-yellow': './images/relay-closed-yellow.png',
  'closed-red': './images/relay-closed-red.png',
  'open': './images/relay-open.png',
}

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

def _show_border(ax, border_state):
  # Load the SVG image using mpimg
  image_loc = IMAGE_LOCS[border_state]
  image = mpimg.imread(image_loc)

  # Calculate the desired width and height for resizing
  desired_width = 100  # Set your desired width in pixels
  aspect_ratio = image.shape[1] / image.shape[0]
  desired_height = desired_width / aspect_ratio

  # Plot the resized image on the axes
  ax.imshow(image, interpolation='bilinear', extent=(0, desired_width, 0, desired_height))

def on_button_click(event):
  print("Button clicked!")

def show_figure():
  # Create a figure and axes
  fig = plt.figure(facecolor='#EEEEEE')
  ax = fig.add_subplot(212)
  ax.set_facecolor('#EEEEEE')
  # [left, bottom, width, height]
  ax.set_position([0.25, 0, 0.5, 0.5])
  _set_up_axes(ax)
  _show_border(ax, CLOSED_RED)

  # section title
  fig.text(0.465, 0.275, 'Relay Status: ON', ha='center', va='center', fontsize=14, color='#B80303', weight="bold")
  fig.text(0.445, 0.215, 'IoT systems activated.', ha='center', va='center', fontsize=10, color='#000000')

  # Create the button
  button_ax = fig.add_axes([0.5, 0.05, 0.15, 0.075])  # Adjust the values as per your desired position and size
  button_ax.spines['top'].set_visible(False)
  button_ax.spines['right'].set_visible(False)
  button_ax.spines['left'].set_visible(False)
  button_ax.spines['bottom'].set_visible(False)

  button = Button(button_ax, 'Click Me', color='#B80303', hovercolor='#b33434')
  button.label.set_color('white')
  button.label.set_weight('bold')

  button.on_clicked(on_button_click)


  # Show the plot
  fig.canvas.start_event_loop(2)

show_figure()