import random
import os
import pickle
import pandas as pd
import numpy as np
import os
import logging
from utils import Paths
import time
import collections
import encodings
import re

def preprocessing():
    print 'PreProcess'
    start_time = time.time()

    data = readFile()

    print (data.columns)

    data.columns = generateColumnName()

    writeFile(data)

    end_time = time.time()
    print '(Time to preprocess: %s)' % (end_time - start_time)

def readFile():
    if os.path.exists(Paths.input_file):
        data = pd.read_csv(Paths.input_file, sep=",", encoding='utf-8', skiprows=2, low_memory=False)
    return data;

def getCourseList():
    courseString = ""
    courses = []

    with open(Paths.input_file) as input_file:
        courseString = input_file.readlines()[1]

    coursesTemp = courseString.split(",,,,,,")
    for course in coursesTemp:
        course = course.replace(",", "")
        course = course.replace("_", "")
        if len(course) > 0 :
            courses.append(course)
            print(course)

    print(len(courses))
    return courses

def generateColumnName():
    courseAttrs = ["Attendance", "Average_Mark", "Has_Passed", "Is_Graded", "Is_Required", "Number_Of_Failures"]
    courses = getCourseList()
    newColumn = ["Roll_Number", "Gender", "Distance_To_Hanoi", "Major", "Total_Years", "Is_Graduated", "Is_Dropout"]

    print(len(newColumn))
    for course in courses:
        for attr in courseAttrs:
            columnTemp = attr + "_" + course
            newColumn.append(columnTemp)
            print(columnTemp)
    print(len(newColumn))
    return newColumn

def writeFile(data):
    if not os.path.exists(Paths.result):
        os.makedirs(Paths.result)

    data.to_csv(Paths.output_file, index=False)
    print('Done')

def main():
    oper = -1
    while int(oper) != 0:
        print('**************************************')
        print('Choose one of the following: ')
        print('1 - Pre Processing')
        print('0 - Exit')
        print('**************************************')
        oper = int(input("Enter your options: "))

        if oper == 0:
            exit()
        elif oper == 1:
            preprocessing()

if __name__ == "__main__":
    main()
