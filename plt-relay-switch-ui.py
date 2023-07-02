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

def _clean_axis(ax):
  ax.xaxis.set_tick_params(labelbottom=False)
  ax.yaxis.set_tick_params(labelleft=False)

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

def show_hide_items(items_to_hide=[], items_to_show=[], event=None):
  print('Event: ', str(event))
  for item in items_to_hide:
    item.set_visible(False)
    item.set_zorder(0) # send backward

  for item in items_to_show:
    item.set_visible(True)
    item.set_zorder(10) # send forward

def create_step_1_elements(fig):
  '''
  Step 1: Inform the instrument operator that the relay status is ON
          - Show a button to turn off the relay module.
          - Note that the button's click handler is NOT in this function.
  '''

  # Create the border (the image)
  border_ax = fig.add_subplot(211)
  border_ax.set_facecolor('#EEEEEE')
  border_ax.set_position([0.25, 0, 0.5, 0.5])
  _clean_axis(border_ax)
  _show_border(border_ax, CLOSED_RED)

  # Section title and subtitle
  section_title = fig.text(0.31, 0.275, 'Relay Status: ON', ha='left', va='center', fontsize=14, color='#B80303', weight="bold")
  section_subtitle = fig.text(0.31, 0.215, 'IoT systems activated.', ha='left', va='center', fontsize=10, color='#000000')

  # Create button axis
  step_1_btn_ax = fig.add_axes([0.575, 0.1875, 0.125, 0.055])  # Adjust the values as per your desired position and size
  _clean_axis(step_1_btn_ax)

  # Create button. Clicking this should show "Step 2"
  step_1_btn = Button(ax=step_1_btn_ax, label='Turn off', color='#B80303', hovercolor='#980505')
  step_1_btn.label.set_color('white')
  step_1_btn.label.set_weight('bold')

  # Compile section elements
  step_1_elements = [border_ax, section_title, section_subtitle, step_1_btn_ax]
  return step_1_elements, step_1_btn

def create_step_2_elements(fig):
  '''
  Step 2: Confirm with the instrument operator that they want to turn off the relay module.
          - Show two button
            - Button A: Yes, turn it off
            - Button B: No, keep it on
          - Note that the buttons' click handlers are NOT in this function.
  '''

  # Create the border (the image)
  step_2_ax = fig.add_subplot(212)
  step_2_ax.set_facecolor('#EEEEEE')
  step_2_ax.set_position([0.25, 0, 0.5, 0.5])
  _clean_axis(step_2_ax)
  _show_border(step_2_ax, CLOSED_RED)

  # Section title (question)
  step_2_text_1 = fig.text(0.31, 0.275, 'Turn off Relay Module?', ha='left', va='center', fontsize=14, color='#B80303', weight="bold")

  # Create Button A axis
  step_2_btn_a_ax = fig.add_axes([0.31, 0.1875, 0.19, 0.055])  # Adjust the values as per your desired position and size
  _clean_axis(step_2_btn_a_ax)

  # Create Button A. Clicking this should show "Step 3" - action not provided in this function
  step_2_btn_a = Button(ax=step_2_btn_a_ax, label='Yes, turn it off', color='#D9D9D9', hovercolor='#C7C7C7')
  step_2_btn_a.label.set_color('#303030')
  step_2_btn_a.label.set_weight('bold')

  step_2_btn_b_ax = fig.add_axes([0.5225, 0.1875, 0.19, 0.055])  # Adjust the values as per your desired position and size
  _clean_axis(step_2_btn_b_ax)

  # Create Button B. Clicking this should show "Step 1" again - - action not provided in this function
  step_2_btn_b = Button(ax=step_2_btn_b_ax, label='No, keep it on', color='#B80303', hovercolor='#980505')
  step_2_btn_b.label.set_color('white')
  step_2_btn_b.label.set_weight('bold')

  # Compile section elements
  step_2_elements = [step_2_ax, step_2_text_1, step_2_btn_a_ax, step_2_btn_b_ax]
  return step_2_elements, step_2_btn_a, step_2_btn_b

def create_step_3_elements(fig):
  '''
  Step 3: Inform the instrument operator that the relay status is OFF
          - In this state, the operator cannot click any button.
          - In order for the relay module to turn on, the STA/LTA Threshold should
            again be breached. Only the turning off action can be done manually.
  '''

  # Create the border (the image)
  step_3_ax = fig.add_subplot(222)
  step_3_ax.set_facecolor('#EEEEEE')
  step_3_ax.set_position([0.26, 0, 0.5, 0.5])
  _clean_axis(step_3_ax)
  _show_border(step_3_ax, OPEN)

  # Section title and subtitle
  # step_3_text_1 = fig.text(0.31, 0.275, 'Relay Status: OFF', ha='left', va='center', fontsize=14, color='#000000', weight="bold")
  # step_3_text_2 = fig.text(0.31, 0.215, 'IoT systems deactivated.', ha='left', va='center', fontsize=10, color='#000000')
  step_3_text_1 = fig.text(0.31, 0.275, 'Relay Status: DISABLED', ha='left', va='center', fontsize=14, color='#000000', weight="bold")
  step_3_text_2 = fig.text(0.31, 0.215, 'Module disabled in your settings file.', ha='left', va='center', fontsize=10, color='#000000')

  # Compile section elements
  step_3_elements = [step_3_ax, step_3_text_1, step_3_text_2]
  return step_3_elements

def show_figure():
  # Create a figure and axes
  fig = plt.figure(facecolor='#EEEEEE')

  # START - STEP 3
  step_3_elements = create_step_3_elements(fig)
  show_hide_items(items_to_hide=step_3_elements)

  # START - STEP 2
  step_2_elements, step_2_btn_a, step_2_btn_b = create_step_2_elements(fig)
  show_hide_items(items_to_hide=step_2_elements)

  # START - STEP 1
  step_1_elements, step_1_btn = create_step_1_elements(fig)
  show_hide_items(items_to_show=step_1_elements) # NOTE: instead of hiding, we're showing, unlike in step 3 and 2

  # START - ACTIONS: Set up lambda functions and pass the required arguments
  step_1_btn.on_clicked(lambda event: show_hide_items(items_to_hide=step_1_elements, items_to_show=step_2_elements, event=event))
  step_2_btn_a.on_clicked(lambda event: show_hide_items(items_to_hide=step_2_elements, items_to_show=step_3_elements, event=event))
  step_2_btn_b.on_clicked(lambda event: show_hide_items(items_to_hide=step_2_elements, items_to_show=step_1_elements, event=event))

  # Show the plot
  fig.canvas.start_event_loop(10)


show_figure()
