
def format_number(num, non_zero_decimal_places=2):
	'''
	Formats `num` such that there will only be exactly `non_zero_decimal_places`.
	This specifically helps in the visual representation of the values shown in the pop-up,
	where we do not know for sure up to which decimal place can we round off the number.
	If we round it to the nearest hundredths, we risk showing value such as 0.00.
	If we round it to the nearest millionths, we risk showing 0.0001240

	This function takes care of this issue by allowing a variable number of decimal places and
	rounds it to the nearest nth place occupied by a non-zero number,
	where n = non_zero_decimal_place

	Examples:
		BEFORE: 0.00040567
		AFTER: 0.00041

		BEFORE: 0.53
		AFTER: 0.53

		BEFORE: 2.064
		AFTER: 2.064

		BEFORE: 2.5
		AFTER: 2.5

		BEFORE: 2
		AFTER: 2

		BEFORE: 2.0
		AFTER: 2

		BEFORE: 0.0004567
		AFTER: 0.00046

		BEFORE: 1.0004567
		AFTER: 1
	'''
	num_str = str(num)
	decimal_pt_index = num_str.find('.')

	# the number is already an integer
	if decimal_pt_index == -1:
		return num_str

	[whole, decimals] = num_str.split('.')

	non_zero_index = next((i for i, c in enumerate(decimals) if c != '0'), -1)

	# if there are no non-zero numbers to the right, then it's a whole number
	if non_zero_index == -1:
		return whole

	# If the whole number part is non-zero, no need for
	if int(whole) > 0 and non_zero_index >= non_zero_decimal_places:
		return whole

	# include the places occupied by zero to the right of the decimal point
	precision = non_zero_index + non_zero_decimal_places
	return round(num, precision)
