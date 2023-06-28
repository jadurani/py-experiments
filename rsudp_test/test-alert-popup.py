import os
import pkg_resources as pr
from matplotlib.widgets import Button
import matplotlib.image as mpimg
from main import COLOR, printE
import unit_converter as UC
import helpers

import matplotlib.pyplot as plt
from matplotlib import use
from matplotlib import rcParams
rcParams['toolbar'] = 'None'

use('Qt5Agg')
plt.ion()


PLT = plt

COLOR = {
	'purple': '\033[95m',
	'blue': '\033[94m',
	'green': '\033[92m',
	'yellow': '\033[93m',
	'red': '\033[91m',
	'white': '\033[0m',
	'bold': "\033[1m"
}


YELLOW = '#FFA723'
RED = '#B80303'
GREY = '#EEEEEE'
WHITE = '#FFFFFF'
BLACK = '#000000'

CLOSED_YELLOW = 'closed-yellow'
CLOSED_RED = 'closed-red'
OPEN = 'open'

IMAGE_LOCS = {
  'closed-yellow': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-closed-yellow.png')),
  'closed-red': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-closed-red.png')),
  'open': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-open.png')),
}

TEST_EVENT_VALUES = {
    "floor_num": 1,
    "event_time": "2023-06-28T07:04:14.47Z",
    "axis_with_max_drift": "y",
    "acceleration": {
        "x": 0.159855283840772,
        "y": 0.4507967296739231,
        "z": 0.08673215868875968
    },
    "displacement": {
        "x": 0.0001244788963681682,
        "y": 0.0002997290748692203,
        "z": 1.5592992129726283e-05
    },
    "intensity": {
        "x": "IV",
        "y": "V",
        "z": "II-III"
    },
    "drift": {
        "x": 0.006223944818408409,
        "y": 0.014986453743461015,
        "z": 0.0007796496064863142
    },
    "over_drift_thresh": {
        "x": False,
        "y": False,
        "z": False
    }
}

def _clean_up_axis(ax):
	'''
	Sets up the axes such that it will look like a plain rectangle.
	'''
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


def _should_hide_popup(self, event_values):

	max_pga = max(event_values['acceleration'].values())
	max_pgd = max(event_values['displacement'].values())

	is_not_same = self.prev_pga != max_pga or self.prev_pgd != max_pgd

	# replace current values
	self.prev_pga = max_pga
	self.prev_pgd = max_pgd

	return is_not_same


def _is_warning(over_drift_thresh):
	'''
	If the drift in any direction is equal to or greater than the specified
	drift threshold for that direction, the pop-up will display a WARNING instead of
	an ALERT

	A WARNING is more dire and urgent than an ALERT.
	:param over_drift_thresh: Dictionary of directions mapped to True or False: ``{	'x': False,	'y': False,	'z': False}``
	:type over_drift_thresh: dict

	:rtype: bool
	:return: Returns `True` if a drift in any direction is equal to or exceeds its corresponding drift threshold
	'''
	return any(over_drift_thresh.values())


def _get_table_headers():
	headers=['Direction', 'Displacement', 'Acceleration', '% Drift']
	colColours = [GREY, GREY, GREY, GREY]

	return (headers, colColours)


def _get_disp_text(axis, disp_obj):
	if axis not in disp_obj:
		return '--'

	disp = disp_obj[axis]
	disp_cm = UC.convert_dist_units(disp, 'meter', 'centimeter')
	disp_cm = helpers.format_number(disp_cm)
	disp_cm = '%s cm' % disp_cm
	return disp_cm


def _get_acc_text(axis, acc_obj):
	if axis not in acc_obj:
		return '--'

	acc = acc_obj[axis]
	acc_cm = UC.convert_dist_units(acc, 'meter', 'centimeter')
	acc_cm = helpers.format_number(acc_cm)
	acc_cm = '%s cm/s²' % acc_cm
	return acc_cm


def _get_drift_text(axis, drift_obj):
	if axis not in drift_obj:
		return '--'

	drift = drift_obj[axis] * 100 # multiply by 100 since it's originally in just decimal form
	drift = helpers.format_number(drift)
	drift = '%s%%' % drift
	return drift


def _get_cell_properties(axis, banner_color, over_drift_thresh_obj, axis_with_max_drift):
	# default value
	cell_properties = {
		"fill_color": GREY,
		"text_color": BLACK
	}

	if axis not in over_drift_thresh_obj:
		return cell_properties

	if not over_drift_thresh_obj[axis] and axis_with_max_drift != axis:
		return cell_properties

	# highlight the row
	return {
		"fill_color": banner_color,
		"text_color": WHITE
	}


def _get_table_data(event_values, banner_color):
	data = []
	table_properties = []
	for axis, channel in UC.AXIS_CHANNEL_MAP.items():
		# column 1
		direction = '%s-Axis (%s)' % (axis.upper(), channel)

		# column 2
		disp_cm = _get_disp_text(axis, event_values['displacement'])

		# column 3
		acc_cm = _get_acc_text(axis, event_values['acceleration'])

		# column 4
		drift = _get_drift_text(axis, event_values['drift'])

		# meta
		cell_properties = _get_cell_properties(
			axis,
			banner_color,
			event_values['over_drift_thresh'],
			event_values['axis_with_max_drift']
		)

		row = [direction, disp_cm, acc_cm, drift]
		row_properties = [cell_properties, cell_properties, cell_properties, cell_properties]
		data.append(row)
		table_properties.append(row_properties)

	return (data, table_properties)


def _format_table(table, table_properties):
	for row_idx, row in enumerate(table_properties):
		for col_idx, cell_properties in enumerate(row):
			cell = table[row_idx + 1, col_idx]
			cell.set(facecolor=cell_properties['fill_color'])
			cell.get_text().set_color(color=cell_properties['text_color'])


def _create_banner(fig, is_warning, banner_color):
	# banner values
	banner_text = '!!! EARTHQUAKE WARNING !!!' if is_warning else 'Earthquake Alert'

	# create axes that will serve as the banner
	ax_banner = fig.add_subplot(111)
	_clean_up_axis(ax_banner)
	ax_banner.set_position([0, 0.75, 1, 0.5])

	# set background color
	ax_banner.set_facecolor(banner_color)

	# set banner text (positioned on top of the banner)
	fig.text(
		0.5, 0.865, banner_text,
		ha='center', va='center',
		fontsize=24, color=WHITE,
		weight="bold"
	)


def _is_ground_floor(floor_num):
	return floor_num <= 1


def _create_floor_info(fig, floor_num, intensity):
	if _is_ground_floor(floor_num):
		fig.text(0.5, 0.65, ('Intensity %s') % (intensity), ha='center', va='center', fontsize=24, weight="semibold")
		fig.text(0.5, 0.55, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=18, weight="semibold")
	else:
		fig.text(0.5, 0.625, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=24, weight="semibold")


def _create_table(fig, highlight_color, event_values):
	# Values
	floor_num = event_values['floor_num']

	# Get bbox - Adjust the values to move the table (depends on the elements above and below it)
	bbox = [-0.1, 0.15, 1.175, 1]
	if _is_ground_floor(floor_num):
		bbox = [-0.1, 0.075, 1.175, 1]

	(headers, colColours) = _get_table_headers()
	(data, table_properties) = _get_table_data(event_values, highlight_color)

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
		bbox=bbox
	)

	_format_table(table, table_properties)

	# set fontweight of the table
	for cell in table.get_celld().values():
		cell.set_text_props(fontweight='demi')

	# Set font size
	table.auto_set_font_size(False)
	table.set_fontsize(12)
	table.scale(1.2, 2.5)


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
  _clean_up_axis(border_ax)
  _show_border(border_ax, CLOSED_RED)

  # Section title and subtitle
  section_title = fig.text(0.31, 0.275, 'Relay Status: ON', ha='left', va='center', fontsize=14, color='#B80303', weight="bold")
  section_subtitle = fig.text(0.31, 0.215, 'IoT systems activated.', ha='left', va='center', fontsize=10, color='#000000')

  # Create button axis
  step_1_btn_ax = fig.add_axes([0.575, 0.1875, 0.125, 0.055])  # Adjust the values as per your desired position and size
  _clean_up_axis(step_1_btn_ax)

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
  _clean_up_axis(step_2_ax)
  _show_border(step_2_ax, CLOSED_RED)

  # Section title (question)
  step_2_text_1 = fig.text(0.31, 0.275, 'Turn off Relay Module?', ha='left', va='center', fontsize=14, color='#B80303', weight="bold")

  # Create Button A axis
  step_2_btn_a_ax = fig.add_axes([0.31, 0.1875, 0.19, 0.055])  # Adjust the values as per your desired position and size
  _clean_up_axis(step_2_btn_a_ax)

  # Create Button A. Clicking this should show "Step 3" - action not provided in this function
  step_2_btn_a = Button(ax=step_2_btn_a_ax, label='Yes, turn it off', color='#D9D9D9', hovercolor='#C7C7C7')
  step_2_btn_a.label.set_color('#303030')
  step_2_btn_a.label.set_weight('bold')

  step_2_btn_b_ax = fig.add_axes([0.5225, 0.1875, 0.19, 0.055])  # Adjust the values as per your desired position and size
  _clean_up_axis(step_2_btn_b_ax)

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
  _clean_up_axis(step_3_ax)
  _show_border(step_3_ax, OPEN)

  # Section title and subtitle
  step_3_text_1 = fig.text(0.31, 0.275, 'Relay Status: OFF', ha='left', va='center', fontsize=14, color='#000000', weight="bold")
  step_3_text_2 = fig.text(0.31, 0.215, 'IoT systems deactivated.', ha='left', va='center', fontsize=10, color='#000000')
  # step_3_text_1 = fig.text(0.31, 0.275, 'Relay Status: DISABLED', ha='left', va='center', fontsize=14, color='#000000', weight="bold")
  # step_3_text_2 = fig.text(0.31, 0.215, 'Module disabled in your settings file.', ha='left', va='center', fontsize=10, color='#000000')

  # Compile section elements
  step_3_elements = [step_3_ax, step_3_text_1, step_3_text_2]
  return step_3_elements


def _create_relay_section(fig):
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


def show_multi_dim_popup(self, event_values):
	'''
	Creates a pop-up for showing info regarding the earthquake
	This pop-up has no plots or graphs at all -- it's informational
	This ideally shouldn't reside in c_plot.py but GUIs need to be initialized from with the main thread.
	And c_plot.py is the only module run on the main thread.

	:param dict event_values: Values from the PROCESS event.
		See c_process.py for reference on how it really looks like.
	'''
	try:
		# don't create another alert window if there's an existing one that's already opened
		if self.alert_window is not None:
			return

		axis_with_max_drift = event_values['axis_with_max_drift']
		floor_num = event_values['floor_num']
		intensity = event_values['intensity'][axis_with_max_drift]
		is_warning = _is_warning(over_drift_thresh=event_values['over_drift_thresh'])
		popup_color = RED if is_warning else YELLOW

		# create a new figure
		fig = PLT.figure(facecolor=GREY)
		fig.canvas.mpl_connect('close_event', lambda evt: hide_popup(self, evt))
		window_title = '!!! EARTHQUAKE WARNING !!!' if is_warning else 'Earthquake Alert' # include time?
		fig.canvas.set_window_title(window_title)

		# 1 - set up banner
		_create_banner(fig, is_warning, popup_color)

		# # 2 - set up floor info and intensity
		# _create_floor_info(fig, floor_num, intensity)

		# # 3 - set up table
		# _create_table(fig, highlight_color=popup_color, event_values=event_values)

		# ? set up border?
		# 4 - set up relay switch
		_create_relay_section(fig)

		self.alert_window = fig
		fig.canvas.start_event_loop(10)

	except Exception as e:
		printE('Unable to create pop-up', 'alert_popup.py')
		printE(f"{COLOR['red']} {str(e)} {COLOR['white']}\n", 'alert_popup.py')

def hide_popup(self, evt=None):
	'''
	Hides the popup, if it already exists
	'''
	if self.alert_window is not None:
		PLT.close(self.alert_window)
		self.alert_window = None
		self.prev_pga = None
		self.prev_pgd = None

def prepare_popup(self, plt, autoclose, is_relay_enabled):
	global PLT
	PLT = plt

	self.autoclose = autoclose
	self.is_relay_enabled = is_relay_enabled

	# Default values
	self.can_show_popup = False
	self.alert_window = None
	self.prev_pga = None # in m/s**2
	self.prev_pgd = None # in m

class PopUp:
	def __init__(self):
		self.sender = 'POP UP'
		print('INIT!!')

	def prepare(self):
		print('PREPARE POPUP!')
		prepare_popup(self)

	def prepare(self):
		print('PREPARE POPUP!')
		prepare_popup(self, plt=plt, autoclose=False, is_relay_enabled=True)

	def show_popup(self):
		print('PREPARE POPUP!')
		show_multi_dim_popup(self, TEST_EVENT_VALUES)

POPUP = PopUp()
POPUP.prepare()
POPUP.show_popup()