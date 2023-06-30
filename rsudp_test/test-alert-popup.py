import os
import pkg_resources as pr
from matplotlib.widgets import Button
import matplotlib.image as mpimg
from main import COLOR, printE
import unit_converter as UC
import helpers

import time

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

RELAY_STATES = {
	'loading': {
		'is_start': True,
		'is_end': False,
		'before': [],
		'after': ['on', 'processing', 'error']
	},
	'on': {
		'is_start': False,
		'is_end': False,
		'before': ['loading', 'confirm'],
		'after': ['confirm']
	},
	'confirm': {
		'is_start': False,
		'is_end': False,
		'before': ['on'],
		'after': ['processing', 'on']
	},
	'processing': {
		'is_start': False,
		'is_end': False,
		'before': ['confirm'],
		'after': ['off', 'error']
	},
	'off': {
		'is_start': False,
		'is_end': True,
		'before': ['processing'],
		'after': []
	},
	'disabled': {
		'is_start': False,
		'is_end': True,
		'before': ['loading'],
		'after': []
	},
	'error': {
		'is_start': False,
		'is_end': True,
		'before': ['loading', 'processing'],
		'after': []
	},
}

YELLOW = '#FFA723'
RED = '#B80303'
GREY = '#EEEEEE'
WHITE = '#FFFFFF'
BLACK = '#303030'
ACCENT = '#D9D9D9'
ACCENT_HOVER = '#C7C7C7'

RED_HOVER = '#980505'
YELLOW_HOVER = '#DE921F'

CLOSED_YELLOW = 'closed-yellow'
CLOSED_RED = 'closed-red'
OPEN = 'open'
LOADING = 'loading'
ERROR = 'error'

IMAGE_LOCS = {
	'closed-yellow': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-closed-yellow.png')),
	'closed-red': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-closed-red.png')),
	'open': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-open.png')),
	'loading': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-loading.png')),
	'error': pr.resource_filename('rsudp', os.path.join('img', 'alert_popup', 'relay-error.png')),
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
	ax_banner = fig.add_subplot(311)
	_clean_up_axis(ax_banner)
	ax_banner.set_position([0, 0.75, 1, 0.5])

	# set background color
	ax_banner.set_facecolor(banner_color)

	# set banner text (positioned on top of the banner)
	fig.text(
		0.5, 0.865, banner_text,
		ha='center', va='center',
		fontsize=24, color=WHITE,
		weight='bold'
	)


def _is_ground_floor(floor_num):
	return floor_num <= 1


def _create_floor_info(fig, floor_num, intensity):
	if _is_ground_floor(floor_num):
		fig.text(0.5, 0.675, ('Intensity %s') % (intensity), ha='center', va='center', fontsize=24, weight="semibold")
		fig.text(0.5, 0.6, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=18, weight="semibold")
	else:
		fig.text(0.5, 0.625, ('FLOOR %s') % (floor_num), ha='center', va='center', fontsize=24, weight="semibold")


def _create_table(fig, highlight_color, event_values):
	# Values
	floor_num = event_values['floor_num']

	# Get bbox - Adjust the values to move the table (depends on the elements above and below it)
	bbox = [-0.1, -0.5, 1.175, 1.25]
	if _is_ground_floor(floor_num):
		bbox = [-0.1, -0.5, 1.175, 1.25]

	(headers, colColours) = _get_table_headers()
	(data, table_properties) = _get_table_data(event_values, highlight_color)

	# Hide axes
	ax_bottom = fig.add_subplot(312)
	ax_bottom.axis('off')
	ax_bottom.axis('tight')

	# Create table
	table = ax_bottom.table(
		cellText=data,
		loc='top',
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
	if ax.images:
		ax.images[0].remove()

	# Load the SVG image using mpimg
	image_loc = IMAGE_LOCS[border_state]
	image = mpimg.imread(image_loc)

	# Calculate the desired width and height for resizing
	desired_width = 100  # Set your desired width in pixels
	aspect_ratio = image.shape[1] / image.shape[0]
	desired_height = desired_width / aspect_ratio

	# Plot the resized image on the axes
	ax.imshow(image, interpolation='bilinear', extent=(0, desired_width, 0, desired_height))

def _show_border_img(ax, relay_state, is_warning=False):
	if ax.images:
		ax.images[0].remove()



	if relay_state in ['loading', 'processing']:
		image_loc = IMAGE_LOCS['loading']
	elif relay_state in ['off', 'disabled']:
		image_loc = IMAGE_LOCS['open']
	elif relay_state in ['on', 'confirm']:
		border_color = CLOSED_RED if is_warning else CLOSED_YELLOW
		image_loc = IMAGE_LOCS[border_color]
	elif relay_state == 'error':
		image_loc = IMAGE_LOCS['error']
	else:
		raise Exception('Unable to find border image')

	image = mpimg.imread(image_loc)
	ax.set_position([0.25, -0.125, 0.5, 0.5])

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
		item.set_zorder(99) # send forward


def turn_off_relay(params):
	print('TO DO: Do something to turn off the relay')

	show_hide_items(items_to_hide=params['items_to_hide'], items_to_show=params['items_to_show'], event='Turn off relay')

	border_ax = params['border_ax']
	border_ax.set_position([0.26, -0.125, 0.5, 0.5])
	_show_border(border_ax, OPEN)


def switch_off_relay(self, is_warning):
	change_relay_state(self, 'confirm')
	state_action(self, is_warning)


def confirm_off_relay(self, is_warning):
	# TO DO: communicate to relay module
	change_relay_state(self, 'processing')
	state_action(self, is_warning)


def cancel_off_relay(self, is_warning):
	change_relay_state(self, 'on')
	state_action(self, is_warning)


def create_step_1_elements(fig, border_ax=None, is_warning=False):
	'''
	Step 1: Inform the instrument operator that the relay status is ON
					- Show a button to turn off the relay module.
					- Note that the button's click handler is NOT in this function.
	'''

	# Create the border (the image)
	if border_ax is None:
		border_ax = fig.add_subplot(313)
		border_ax.set_facecolor(GREY)
		_clean_up_axis(border_ax)

	border_ax.set_position([0.25, -0.125, 0.5, 0.5])
	border_color = CLOSED_RED if is_warning else CLOSED_YELLOW
	_show_border(border_ax, border_color)

	el_color = RED if is_warning else YELLOW
	el_color_hover = RED_HOVER if is_warning else YELLOW_HOVER

	# Section title and subtitle
	section_title = fig.text(0.31, 0.15, 'Relay Status: ON', ha='left', va='center', fontsize=14, color=el_color, weight='bold')
	section_subtitle = fig.text(0.31, 0.095, 'IoT systems activated.', ha='left', va='center', fontsize=10, color=BLACK)

	# Create button axis
	step_1_btn_ax = fig.add_axes([0.575, 0.07, 0.125, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(step_1_btn_ax)

	# Create button. Clicking this should show "Step 2"
	step_1_btn = Button(ax=step_1_btn_ax, label='Turn off', color=el_color, hovercolor=el_color_hover)
	step_1_btn.label.set_color(WHITE)
	step_1_btn.label.set_weight('bold')

	# Compile section elements
	step_1_elements = [section_title, section_subtitle, step_1_btn_ax]
	return step_1_elements, step_1_btn, border_ax


def create_step_2_elements(fig, border_ax=None, is_warning=False):
	'''
	Step 2: Confirm with the instrument operator that they want to turn off the relay module.
					- Show two button
						- Button A: Yes, turn it off
						- Button B: No, keep it on
					- Note that the buttons' click handlers are NOT in this function.
	'''

	# Create the border (the image)
	if border_ax is None:
		border_ax = fig.add_subplot(313)
		border_ax.set_facecolor(GREY)
		_clean_up_axis(border_ax)

	border_ax.set_position([0.26, -0.125, 0.5, 0.5])
	border_color = CLOSED_RED if is_warning else CLOSED_YELLOW
	_show_border(border_ax, border_color)

	el_color = RED if is_warning else YELLOW
	el_color_hover = RED_HOVER if is_warning else YELLOW_HOVER


	# Section title (question)
	step_2_text_1 = fig.text(0.31, 0.15, 'Turn off Relay Module?', ha='left', va='center', fontsize=14, color=el_color, weight='bold')

	# Create Button A axis
	step_2_btn_a_ax = fig.add_axes([0.31, 0.07, 0.2, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(step_2_btn_a_ax)

	# Create Button A. Clicking this should show "Step 3" - action not provided in this function
	step_2_btn_a = Button(ax=step_2_btn_a_ax, label='Yes, turn it off', color=ACCENT, hovercolor=ACCENT_HOVER)
	step_2_btn_a.label.set_color(BLACK)
	step_2_btn_a.label.set_weight('bold')

	step_2_btn_b_ax = fig.add_axes([0.5225, 0.07, 0.2, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(step_2_btn_b_ax)

	# Create Button B. Clicking this should show "Step 1" again - - action not provided in this function
	step_2_btn_b = Button(ax=step_2_btn_b_ax, label='No, keep it on', color=el_color, hovercolor=el_color_hover)
	step_2_btn_b.label.set_color(WHITE)
	step_2_btn_b.label.set_weight('bold')

	# Compile section elements
	step_2_elements = [step_2_text_1, step_2_btn_a_ax, step_2_btn_b_ax]
	return step_2_elements, step_2_btn_a, step_2_btn_b, border_ax


def create_step_3_elements(fig, border_ax=None):
	'''
	Step 3: Inform the instrument operator that the relay status is OFF
					- In this state, the operator cannot click any button.
					- In order for the relay module to turn on, the STA/LTA Threshold should
						again be breached. Only the turning off action can be done manually.
	'''

	# Create the border (the image)
	if border_ax is None:
		border_ax = fig.add_subplot(313)
		border_ax.set_facecolor(GREY)
		_clean_up_axis(border_ax)

	# Section title and subtitle
	step_3_text_1 = fig.text(0.31, 0.15, 'Relay Status: OFF', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	step_3_text_2 = fig.text(0.31, 0.095, 'IoT systems deactivated.', ha='left', va='center', fontsize=10, color=BLACK)
	# step_3_text_1 = fig.text(0.31, 0.275, 'Relay Status: DISABLED', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	# step_3_text_2 = fig.text(0.31, 0.215, 'Module disabled in your settings file.', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	step_3_elements = [step_3_text_1, step_3_text_2]
	return step_3_elements, border_ax


def create_loading_elements(fig):
	'''
	LOADING Screen: Show screen while confirming an active connection to the Arduino unit.
	- In this state, the operator cannot click any button.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''

	# Section title and subtitle
	loading_text_1 = fig.text(0.31, 0.15, 'Loading...', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	loading_text_2 = fig.text(0.31, 0.095, 'Contacting your Arduino unit...', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	loading_elements = [loading_text_1, loading_text_2]
	return loading_elements


def create_on_elements(fig, is_warning=False):
	'''
	ON Screen: Inform the instrument operator that the relay status is ON
	- Show a button to turn off the relay module.
	- Note that the button's click handler is NOT in this function.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array, button element
	:return: Returns an array containing the elements of this screen and the button element
	'''
	el_color = RED if is_warning else YELLOW
	el_color_hover = RED_HOVER if is_warning else YELLOW_HOVER

	# Section title and subtitle
	section_title = fig.text(0.31, 0.15, 'Relay Status: ON', ha='left', va='center', fontsize=14, color=el_color, weight='bold')
	section_subtitle = fig.text(0.31, 0.095, 'IoT systems activated.', ha='left', va='center', fontsize=10, color=BLACK)

	# Create button axis
	turn_off_btn_ax = fig.add_axes([0.575, 0.07, 0.125, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(turn_off_btn_ax)

	# Create button. Clicking this should show "Step 2"
	turn_off_btn = Button(ax=turn_off_btn_ax, label='Turn off', color=el_color, hovercolor=el_color_hover)
	turn_off_btn.label.set_color(WHITE)
	turn_off_btn.label.set_weight('bold')

	# Compile section elements
	turn_off_elements = [section_title, section_subtitle, turn_off_btn_ax]
	return turn_off_elements, turn_off_btn


def create_confirm_elements(fig, is_warning=False):
	'''
	CONFIRM Screen: Confirm with the instrument operator that they want to turn off the relay module.
	- Show two button
		- Button A: Yes, turn it off
		- Button B: No, keep it on
	- Note that the buttons' click handlers are NOT in this function.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''

	el_color = RED if is_warning else YELLOW
	el_color_hover = RED_HOVER if is_warning else YELLOW_HOVER

	# Section title (question)
	section_title = fig.text(0.31, 0.15, 'Turn off Relay Module?', ha='left', va='center', fontsize=14, color=el_color, weight='bold')

	# Confirm turn off axis
	turn_off_btn_ax = fig.add_axes([0.31, 0.07, 0.2, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(turn_off_btn_ax)

	# Create Confirm Turn Off Button. Clicking this should show "Processing" Screen - action not provided in this function
	turn_off_btn = Button(ax=turn_off_btn_ax, label='Yes, turn it off', color=ACCENT, hovercolor=ACCENT_HOVER)
	turn_off_btn.label.set_color(BLACK)
	turn_off_btn.label.set_weight('bold')

	# Cancel turn off axis
	cancel_btn_ax = fig.add_axes([0.5225, 0.07, 0.2, 0.055])  # Adjust the values as per your desired position and size
	_clean_up_axis(cancel_btn_ax)

	# Create Cancel Turn Off Button. Clicking this should show "On" Screen - action not provided in this function
	cancel_btn = Button(ax=cancel_btn_ax, label='No, keep it on', color=el_color, hovercolor=el_color_hover)
	cancel_btn.label.set_color(WHITE)
	cancel_btn.label.set_weight('bold')

	# Compile section elements
	step_2_elements = [section_title, turn_off_btn_ax, cancel_btn_ax]
	return step_2_elements, turn_off_btn, cancel_btn


def create_processing_elements(fig):
	'''
	PROCESSING Screen: Show screen while communicating with the Arduino unit.
	- In this state, the operator cannot click any button.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''
	# Section title and subtitle
	processing_text_1 = fig.text(0.31, 0.15, 'Processing...', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	processing_text_2 = fig.text(0.31, 0.095, 'Sending message to Arduino...', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	processing_elements = [processing_text_1, processing_text_2]
	return processing_elements


def create_off_elements(fig):
	'''
	OFF Screen: Inform the instrument operator that the relay status is OFF
	- In this state, the operator cannot click any button.
	- In order for the relay module to turn on, the STA/LTA Threshold should
		again be breached. Only the turning off action can be done manually.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''
	# Section title and subtitle
	off_text_1 = fig.text(0.31, 0.15, 'Relay Status: OFF', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	off_text_2 = fig.text(0.31, 0.095, 'IoT systems deactivated.', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	off_elements = [off_text_1, off_text_2]
	return off_elements


def create_disabled_elements(fig):
	'''
	DISABLED Screen: The relay module is disabled.
	- In this state, the operator cannot click any button.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''
	# Section title and subtitle
	disabled_text_1 = fig.text(0.31, 0.15, 'Relay Status: DISABLED', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	disabled_text_2 = fig.text(0.31, 0.095, 'Disabled in your settings file.', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	disabled_elements = [disabled_text_1, disabled_text_2]
	return disabled_elements


def create_error_elements(fig):
	'''
	ERROR Screen: Failed to contact the relay module.
	- In this state, the operator cannot click any button.
	- In order for the relay module to turn on, the STA/LTA Threshold should
		again be breached. Only the turning off action can be done manually.

	:param fig: The matplotlib figure where the popup elements are displayed on
	:rtype: Array
	:return: Returns an array containing the elements of this screen
	'''
	# Section title and subtitle
	error_text_1 = fig.text(0.31, 0.15, 'Relay Status: ERROR', ha='left', va='center', fontsize=14, color=BLACK, weight='bold')
	error_text_2 = fig.text(0.31, 0.095, 'Unable to contact Arduino unit.', ha='left', va='center', fontsize=10, color=BLACK)

	# Compile section elements
	error_elements = [error_text_1, error_text_2]
	return error_elements


def change_relay_state(self, next_state):
	'''
	Manage the state of the relay section
	'''
	try:
		print(f'Changing state from "{self.relay_state}" to "{next_state}".')

		current_state_obj = RELAY_STATES[self.relay_state]
		next_state_obj = RELAY_STATES[next_state]

		if self.relay_state not in next_state_obj['before']:
			exception_msg = f'Invalid state transition from "{self.relay_state}" to "{next_state}"'
			valid_values_msg = f'Valid previous states for "{next_state}": {str(next_state_obj["before"])}'
			raise Exception(f'{exception_msg}\n{valid_values_msg}')

		elif next_state not in current_state_obj['after']:
			exception_msg = f'Invalid state transition from "{self.relay_state}" to "{next_state}"'
			valid_values_msg = f'Valid next states for "{self.relay_state}" are: {str(current_state_obj["after"])}'
			raise Exception(f'{exception_msg}\n{valid_values_msg}')

		self.relay_state = next_state
	except Exception as e:
		print(e)


def state_action(self, is_warning=False):
	'''
	React to the state action.
	Should be called after change_relay_state
	'''
	show_hide_items(items_to_hide=self.all_elements)

	if self.relay_state == 'loading':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.loading_elements)

	elif self.relay_state == 'on':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.on_elements)

	elif self.relay_state == 'confirm':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.confirm_elements)

	elif self.relay_state == 'processing':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.processing_elements)

	elif self.relay_state == 'off':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.off_elements)

	elif self.relay_state == 'disabled':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.disabled_elements)

	elif self.relay_state == 'error':
		print(self.relay_state)
		_show_border_img(self.border_ax, self.relay_state, is_warning)
		show_hide_items(items_to_show=self.error_elements)


def _create_relay_section(self, fig, is_warning):
	pass
	border_ax = fig.add_subplot(313)
	border_ax.set_facecolor(GREY)
	_clean_up_axis(border_ax)

	loading_elements = create_loading_elements(fig)
	on_elements, turn_off_btn = create_on_elements(fig, is_warning)
	confirm_elements, confirm_off_btn, cancel_btn = create_confirm_elements(fig, is_warning=is_warning)
	processing_elements = create_processing_elements(fig)
	off_elements =  create_off_elements(fig)
	disabled_elements = create_disabled_elements(fig)
	error_elements = create_error_elements(fig)

	self.turn_off_btn = turn_off_btn
	self.confirm_off_btn = confirm_off_btn
	self.cancel_btn = cancel_btn
	self.border_ax = border_ax

	self.loading_elements = loading_elements
	self.on_elements = on_elements
	self.confirm_elements = confirm_elements
	self.processing_elements = processing_elements
	self.off_elements = off_elements
	self.disabled_elements = disabled_elements
	self.error_elements = error_elements

	self.all_elements = loading_elements + \
		on_elements + \
		confirm_elements + \
		processing_elements + \
		off_elements + \
		disabled_elements + \
		error_elements

	turn_off_btn.on_clicked(lambda event: switch_off_relay(self, is_warning))
	cancel_btn.on_clicked(lambda event: cancel_off_relay(self, is_warning))
	confirm_off_btn.on_clicked(lambda event: confirm_off_relay(self, is_warning))


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
		fig.set_size_inches(6.5, 5.5)

		# 1 - set up banner
		_create_banner(fig, is_warning, popup_color)

		# 2 - set up floor info and intensity
		_create_floor_info(fig, floor_num, intensity)

		# 3 - set up table
		_create_table(fig, highlight_color=popup_color, event_values=event_values)

		# 4 - set up relay switch
		_create_relay_section(self, fig, is_warning)

		# Test only
		self.relay_state = 'loading'
		change_relay_state(self, 'on')
		state_action(self, is_warning)

		# Also keep a reference to the figure
		self.alert_window = fig

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

	self.relay_state = 'loading' # initial state

	self.turn_off_btn = None
	self.confirm_off_btn = None
	self.cancel_btn = None
	self.border_ax = None
	self.loading_elements = None
	self.on_elements = None
	self.confirm_elements = None
	self.processing_elements = None
	self.off_elements = None
	self.disabled_elements = None
	self.error_elements = None
	self.all_elements = []

class PopUp:
	def __init__(self):
		self.sender = 'POP UP'
		print('INIT!!')

	def prepare(self):
		print('PREPARE POPUP!')
		prepare_popup(self, plt=plt, autoclose=False, is_relay_enabled=True)

	def show_popup(self):
		print('SHOW POPUP!')
		show_multi_dim_popup(self, TEST_EVENT_VALUES)

		self.alert_window.canvas.start_event_loop(5)
		# self.alert_window.canvas.start_event_loop(10)

POPUP = PopUp()
POPUP.prepare()
POPUP.show_popup()