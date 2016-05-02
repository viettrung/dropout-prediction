import re
from os import path

class Paths(object):
  data = 'data'
  result = 'result'
  major = 'major'
  input_path = path.join(data, 'Y')
  output_path = path.join(result, 'Y')
  test_path = path.join(data, 'Test1.csv')
  arff_path = path.join(data, 'Test1.arff')
  arff_input = './data/arff/'
  csv_input = './data/csv/'
  arff_output = './result/arff/'
  csv_output = './result/csv/'
