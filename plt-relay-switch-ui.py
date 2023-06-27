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

def show_hide_items(items_to_hide=[], items_to_show=[]):
  print("Button clicked!")
  for item in items_to_hide:
    item.set_visible(False)

  for item in items_to_show:
    item.set_visible(True)


def show_figure():
  # Create a figure and axes
  fig = plt.figure(facecolor='#EEEEEE')

  #################################### START - STEP 1
  # step_1_ax = fig.add_subplot(212)
  # step_1_ax.set_facecolor('#EEEEEE')
  # # [left, bottom, width, height]
  # step_1_ax.set_position([0.25, 0, 0.5, 0.5])
  # _set_up_axes(step_1_ax)
  # _show_border(step_1_ax, CLOSED_RED)

  # # section title
  # text_1 = fig.text(0.465, 0.275, 'Relay Status: ON', ha='center', va='center', fontsize=14, color='#B80303', weight="bold")
  # text_2 = fig.text(0.445, 0.215, 'IoT systems activated.', ha='center', va='center', fontsize=10, color='#000000')

  # # Create the button
  # step_1_btn_ax = fig.add_axes([0.575, 0.1875, 0.125, 0.055])  # Adjust the values as per your desired position and size
  # step_1_btn_ax.spines['top'].set_visible(False)
  # step_1_btn_ax.spines['right'].set_visible(False)
  # step_1_btn_ax.spines['left'].set_visible(False)
  # step_1_btn_ax.spines['bottom'].set_visible(False)

  # step_1_btn = Button(step_1_btn_ax, 'Turn off', color='#B80303', hovercolor='#b33434')
  # step_1_btn.label.set_color('white')
  # step_1_btn.label.set_weight('bold')

  # Set up the lambda function to pass the required arguments
  # step_1_items_to_hide = [step_1_ax, step_1_btn_ax, text_1, text_2]
  # step_1_btn.on_clicked(lambda event: show_hide_items(step_1_items_to_hide))


  #################################### START - STEP 2
  step_2_ax = fig.add_subplot(212)
  step_2_ax.set_facecolor('#EEEEEE')
  # [left, bottom, width, height]
  step_2_ax.set_position([0.25, 0, 0.5, 0.5])
  _set_up_axes(step_2_ax)
  _show_border(step_2_ax, CLOSED_RED)

  # section title
  text_1 = fig.text(0.5, 0.275, 'Turn off Relay Module?', ha='center', va='center', fontsize=14, color='#B80303', weight="bold")

  step_2_btn_a_ax = fig.add_axes([0.3, 0.1875, 0.2, 0.055])  # Adjust the values as per your desired position and size
  step_2_btn_a_ax.spines['top'].set_visible(False)
  step_2_btn_a_ax.spines['right'].set_visible(False)
  step_2_btn_a_ax.spines['left'].set_visible(False)
  step_2_btn_a_ax.spines['bottom'].set_visible(False)

  step_2_btn_a = Button(step_2_btn_a_ax, 'Yes, turn it off', color='#D9D9D9', hovercolor='#b33434')
  step_2_btn_a.label.set_color('grey')
  step_2_btn_a.label.set_weight('bold')

  # Create the button
  step_2_btn_b_ax = fig.add_axes([0.5225, 0.1875, 0.2, 0.055])  # Adjust the values as per your desired position and size
  step_2_btn_b_ax.spines['top'].set_visible(False)
  step_2_btn_b_ax.spines['right'].set_visible(False)
  step_2_btn_b_ax.spines['left'].set_visible(False)
  step_2_btn_b_ax.spines['bottom'].set_visible(False)

  step_2_btn_b = Button(step_2_btn_b_ax, 'No, keep it on', color='#B80303', hovercolor='#b33434')
  step_2_btn_b.label.set_color('white')
  step_2_btn_b.label.set_weight('bold')

  #################################### START - STEP 3


  # Show the plot
  fig.canvas.start_event_loop(3)


show_figure()
