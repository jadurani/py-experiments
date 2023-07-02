from main import printM, printE

SELF_SENDER = 'unit_converter.py'

# acceleration due to gravity; used for comparison
G_ACC = 9.81

# dictionary of conversion factors with respect to 1 meter
DIST_UNIT_DICT = {
	"millimeter": 0.001,
	"centimeter": 0.01,
	"meter": 1.0
}

DIST_UNIT_ARR = list(DIST_UNIT_DICT.keys())

AXIS_CHANNEL_MAP = {
	'x': 'ENE',
	'y': 'ENN',
	'z': 'ENZ'
}

CHANNEL_DIRECTION_MAP = {
	'ENE': 'East',
	'ENN': 'North',
	'ENZ': 'Up/Down'
}

def is_valid_dist_unit(unit):
	return unit in DIST_UNIT_ARR

def convert_dist_units(value, from_unit, to_unit="meter"):
	'''
	Convert distance units
	'''
	# Handle invalid units
	if not is_valid_dist_unit(from_unit) or not is_valid_dist_unit(to_unit):
		return None

	# Convert to base unit (meter)
	base_value = value * DIST_UNIT_DICT[from_unit]

	# Convert from base unit to target unit
	converted_value = base_value / DIST_UNIT_DICT[to_unit]

	printM('Converted %f %s(s) into %f %s(s)' % (value, from_unit, converted_value, to_unit), SELF_SENDER, color='blue')
	return converted_value

def get_g(acc):
	'''
	Given the acceleration (in meters per second squared), get the g value.
	:param acc: acceleration in m / s**2
	'''
	return acc / G_ACC

def g_to_intensity(g):
		'''
		Get the intensity of the earthquake given the g value. The g value is the ratio of
		the ground acceleration over the acceleration due to gravity. If g is 1, that means
		the acceleration of the ground is as fast as the acceleration due to gravity which
		is... pretty intense 👀 (see intensity scale below)
		'''

		intensity_scale = {
			(0,0.00170): 'I',
			(0.00170,0.01400): 'II-III',
			(0.01400,0.03900): 'IV',
			(0.03900,0.09200): 'V',
			(0.09200,0.18000): 'VI',
			(0.18000,0.34000): 'VII',
			(0.34000,0.65000): 'VIII',
			(0.65000,1.24000): 'IX',
			(1.24000,5): 'X+'
		}

		intensity = 'X+'
		for i in intensity_scale:
			if i[0] < g < i[1]:
					intensity = intensity_scale[i]
		return intensity

def intensity_roman_to_arabic(intensity_roman):
		'''
		Convert string to number equivalent. Useful especially for text-to-speech
		'''

		roman_to_arabic = {
			"I": 1,
			"II-III": 2,
			"IV": 4,
			"V": 5,
			"VI": 6,
			"VII": 7,
			"VIII": 8,
			"IX": 9,
			"X+": 10,
		}

		try:
			intensity_arabic = roman_to_arabic[intensity_roman]
			return intensity_arabic
		except Exception as e:
			printE('Intensity %s not found!' % intensity_roman, SELF_SENDER)
			print(e)
			return 0

# print(G_ACC)
# print(DIST_UNIT_DICT)
# print(DIST_UNIT_ARR)
# print(is_valid_dist_unit("meter"))
# print(is_valid_dist_unit("metersss"))
# print(convert_dist_units(1, "centimeter", "meter"))