import re
from os import path

class Paths(object):
  data = 'data'
  result = 'result'
  input_file = path.join(data, 'report_20160404.csv')
  output_file = path.join(result, 'report_20160404_preprogressed.csv')
  test_file = path.join(data, 'test_file')
  train_file = path.join(data, 'train_file')
