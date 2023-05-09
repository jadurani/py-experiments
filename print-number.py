def format_number(num):
    # num_str = f"{num:.2f}".rstrip("0").rstrip(".")
    num_str = str(num)
    decimal_pt_index = num_str.find('.')
    if decimal_pt_index == -1:
      return num_str

    [whole, decimals] = num_str.split('.')
    print('BEFORE >>>', whole, decimals)
    non_zero_index = -1
    for i, c in enumerate(decimals):
      #  print(i, c)
       if c != '0':
          non_zero_index = i
          break
    a = ['a', 'b']
    decimals = decimals[:non_zero_index+2]
    num_str = '.'.join([whole, decimals])
    print('AFTER >>>', whole, decimals, num_str)
    return num_str
    # if num_str[0] == "0":
    #     non_zero_index = next((i for i, ch in enumerate(num_str) if ch != "0" and ch != "."), -1)
    #     if non_zero_index >= 0:
    #         num_str = num_str[:non_zero_index-1]
    return num_str


num1 = 0.0004567
num2 = 0.53
num3 = 2.064
num4 = 2.5
num5 = 2

print(format_number(num1))  # Output: 0.00045
print(format_number(num2))  # Output: 0.53
print(format_number(num3))  # Output: 2.064
print(format_number(num4))  # Output: 2.50
print(format_number(num5))  # Output: 2