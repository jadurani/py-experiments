def format_number(num, non_zero_decimal_places=2):
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
	print(non_zero_index)
	if int(whole) > 0 and non_zero_index >= non_zero_decimal_places:
		return whole

	# include the places occupied by zero to the right of the decimal point
	precision = non_zero_index + non_zero_decimal_places
	return round(num, precision)


num1 = 0.00040567
num2 = 0.53
num3 = 2.064
num4 = 2.5
num5 = 2
num6 = 2.0
num7 = 0.0004567
num8 = 1.0004567

print('BEFORE: %s \n AFTER: %s \n' % (num1, format_number(num1)))  # Output: 0.00041
print('BEFORE: %s \n AFTER: %s \n' % (num2, format_number(num2)))  # Output: 0.53
print('BEFORE: %s \n AFTER: %s \n' % (num3, format_number(num3)))  # Output: 2.064
print('BEFORE: %s \n AFTER: %s \n' % (num4, format_number(num4)))  # Output: 2.50
print('BEFORE: %s \n AFTER: %s \n' % (num5, format_number(num5)))  # Output: 2
print('BEFORE: %s \n AFTER: %s \n' % (num6, format_number(num6)))  # Output: 2
print('BEFORE: %s \n AFTER: %s \n' % (num7, format_number(num7)))  # Output: 0.00046
print('BEFORE: %s \n AFTER: %s \n' % (num8, format_number(num8)))  # Output: 0.00046