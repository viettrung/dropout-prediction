import re
from os import path

class Paths(object):
  data = 'data'
  result = 'result'
  input_path = path.join(data, 'Year')
  output_path = path.join(result, 'Year')
