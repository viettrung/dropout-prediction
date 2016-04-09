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

    for i in range(1, 5):
        data = readFile(i)
        print(data.columns)
        data.columns = generateColumnName(i)
        print(data.columns)

        writeFile(data, i)

    end_time = time.time()
    print '(Time to preprocess: %s)' % (end_time - start_time)

def readFile(num):
    fileName = getFileName(num)
    if os.path.exists(fileName):
        data = pd.read_csv(fileName, sep=",", encoding='utf-8', skiprows=2, low_memory=False)
    return data;

def getFileName(num):
    return (Paths.input_path + str(num) + ".csv")

def getResultName(num):
    return (Paths.output_path + str(num) + "_formated.csv")

def getCourseList(num):
    courseString = ""
    courses = []

    fileName = getFileName(num)
    with open(fileName) as input_file:
        courseString = input_file.readlines()[1]

    coursesTemp = courseString.split(",,,,,,")
    for course in coursesTemp:
        course = course.replace(",", "")
        course = course.replace("_", "")
        course = course.replace("\r", "")
        course = course.replace("\n", "")
        if len(course) > 0 :
            courses.append(course)
            print(course)

    print(len(courses))
    return courses

def generateColumnName(num):
    courseAttrs = ["Attendance", "Average_Mark", "Has_Passed", "Is_Graded", "Is_Required", "Number_Of_Failures"]
    courses = getCourseList(num)
    newColumn = []
    if num == 4:
        newColumn =  ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Total_Year", "Is_Graduated", "Is_Dropout"]
    else:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Is_Dropout"]

    print(len(newColumn))
    for course in courses:
        for attr in courseAttrs:
            columnTemp = attr + "_" + course
            columnTemp = columnTemp.replace("\n", "")
            columnTemp = columnTemp.replace("\r", "")
            newColumn.append(columnTemp)
            print(columnTemp)
    print(len(newColumn))
    return newColumn

def writeFile(data, num):
    if not os.path.exists(Paths.result):
        os.makedirs(Paths.result)
    outPutFile = getResultName(num)
    data.to_csv(outPutFile, index=False)
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
