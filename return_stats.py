def return_stats(input_string, search_pattern):
  if search_pattern.search(input_string) == None:
    return '0'
  else:
    return search_pattern.search(input_string).group(1)