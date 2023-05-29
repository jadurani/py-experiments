a = [1,2,3,4,5]
b = [1,2,3,4,5]
c = [6,7,8,9,0]


def find_existing_row(row_in_search=[]):
  values = [b, c]
  # values = [c, c, b]
  # Search for an existing row with the same longitude and latitude
  for index, row in enumerate(values):
    # if len(row_in_search) != len(row):
    # 	continue
    print(row)
    for col_idx, col_value in enumerate(row):
      print(col_idx, col_value, row_in_search[col_idx])
      if col_value != row_in_search[col_idx]:
        break
      if col_idx + 1 == len(row):
        print('index', index)
        return index + 1  # Add 1 to match the 1-based index used in Sheets API

  return None

res = find_existing_row(a)
print(res)