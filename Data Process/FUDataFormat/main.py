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
from os import path

def preprocessing():
    print 'PreProcess'
    start_time = time.time()

    # We have 8 majors -> for in range 1 -> 8, each major have 5 parts

    for i in range(1, 9):
        majorName = Paths.major + "." + str(i)

        for j in range(1, 6):
            data = readFile(majorName, j)
            print(data.columns)
            data.columns = generateColumnName(majorName, j)
            print(data.columns)

            writeFile(data, majorName, j)

    end_time = time.time()
    print '(Time to preprocess: %s)' % (end_time - start_time)

def readFile(majorName, num):
    fileName = getFileName(majorName, num)
    if os.path.exists(fileName):
        data = pd.read_csv(fileName, sep=",", encoding='utf-8', skiprows=2, low_memory=False)
    return data;

def getFileName(majorName, num):
    return (Paths.data + "/" + majorName + "/Y" + str(num) + ".csv")

def getResultName(majorName, num):
    if num == 5:
        return (Paths.result + "/" + majorName + "/Y4Plus_formated.csv")
    return (Paths.result + "/" + majorName + "/Y" + str(num) + "_formated.csv")

def getCourseList(majorName, num):
    courseString = ""
    courses = []

    fileName = getFileName(majorName, num)
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

def generateColumnName(majorName, num):
    courseAttrs = ["Attendance", "Average_Mark", "Has_Passed", "Is_Graded", "Is_Required", "Number_Of_Failures"]
    courses = getCourseList(majorName, num)
    newColumn = []

    if num == 1:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Is_Dropout"]
    elif num == 2:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Total_Year", "Is_Dropout"]
    elif num == 3:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Total_Year", "Is_Dropout"]
    elif num == 4:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Total_Year", "Is_Dropout"]
    else:
        newColumn = ["Roll_Number", "Gender", "Born", "Distance_To_Hanoi", "Entry_Mark", "Total_Year", "Total_Failures", "Is_Dropout"]

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

def writeFile(data, majorName, num):
    if not os.path.exists(Paths.result + "/" + majorName):
        os.makedirs(Paths.result + "/" + majorName)
    outPutFile = getResultName(majorName, num)
    data.to_csv(outPutFile, index=False)
    print('Done with ' + outPutFile)

# Convert number to yes/no
def readFileConvert():
    fileName = Paths.test_path
    if os.path.exists(fileName):
        data = pd.read_csv(fileName, sep=",", encoding='utf-8', low_memory=False)

    d = {1: "yes", 0: 'no'}

    print(d)

    for columnName in data.columns.values:
        if "Is_Dropout" in columnName:
            data[columnName] = data[columnName].map(d)

    print(data["Is_Dropout"])

    if not os.path.exists(Paths.result):
        os.makedirs(Paths.result)
    data.to_csv("Test_formated1.csv", index=False)

def getFileList(isCSV):
    subDirs = ''
    if isCSV:
        subDirs = Paths.csv_input
    else:
        subDirs = Paths.arff_input

    if not os.path.exists(subDirs):
        os.makedirs(subDirs)
        print('Input data not found, please put csv file in data/csv or put arff file in data/arff :)')
        return

    dirs = os.listdir(subDirs)

    # This would print all the files and directories
    for file in dirs:
        print(file)
        if os.path.isdir(subDirs + "/" + file):
            pathName = os.listdir(subDirs + "/" + file)
            for file1 in pathName:
                if os.path.isdir(subDirs + "/" + file + '/' + file1):
                    pathSubName = os.listdir(subDirs + "/" + file + '/' + file1)
                    for file2 in pathSubName:
                        if not checkTempFile(file2):
                            if isCSV and checkCSV(file2):
                                #convert csv to arff here
                                csv2arffConvert(file + '/' + file1 + '/' + file2, file + '/' + file1)
                            elif not isCSV and checkARFF(file2):
                                #convert arff to csv here
                                arff2csvConvert(file + '/' + file1 + '/' + file2, file + '/' + file1)
                elif not checkTempFile(file1):
                    if isCSV and checkCSV(file1):
                        #convert csv to arff here
                        csv2arffConvert(file + '/' + file1, file)
                    elif not isCSV and checkARFF(file1):
                        #convert arff to csv here
                        arff2csvConvert(file + '/' + file1, file)
        else:
            if not checkTempFile(file):
                print(file)

def checkTempFile(temp):
    return temp.startswith(".")

#Check extention
def checkCSV(fileName):
    return os.path.splitext(fileName)[1] == '.csv'

def checkARFF(fileName):
    return os.path.splitext(fileName)[1] == '.arff'

def removeExtention(fileName):
    return os.path.splitext(fileName)[0]

def checkIsDropoutType(data):
    try:
        return data["Is_Dropout"][1] == 1 or data["Is_Dropout"][1] == 0
    except:
        return False


# Convert csv to arff
def csv2arffConvert(fileName, folderName):
    filePath = Paths.csv_input + fileName
    if os.path.exists(filePath):
        try:
            data = pd.read_csv(filePath, sep=",", encoding='utf-8', low_memory=False)
        except:
            return


    if not os.path.exists(Paths.arff_output + folderName):
        os.makedirs(Paths.arff_output + folderName)

    print(Paths.arff_output + removeExtention(fileName))

    new_file = open(Paths.arff_output + removeExtention(fileName) + ".arff", 'w+')
    ##
    #following portions formats and writes to the new ARFF file
    ##

    #write relation
    new_file.write('@relation ' + fileName + '-weka.filters.unsupervised.attribute.Remove-R1\n\n')

    haveRollNumber = False
    #fill attribute type input
    for columnName in data.columns.values:
        # Check if column is_dropout -> nominal {no,yes} {0,1}
        if "Is_Dropout" in columnName:
            if checkIsDropoutType(data):
                attribute_type = '{0,1}'
            else:
                attribute_type = '{no,yes}'
            new_file.write('@attribute ' + columnName + ' ' + attribute_type + '\n')
        elif "Roll_Number" in columnName:
            attribute_type = 'string'
            haveRollNumber = True
        else:
            attribute_type = 'numeric'
            new_file.write('@attribute ' + columnName + ' ' + attribute_type + '\n')

    #write data
    new_file.write('\n@data\n')

    for row in range(0, len(data.index) - 1):
        temp = data.iloc[row].tolist()

        # Remove RollNumber if need
        if haveRollNumber:
            del temp[0]

        temp1 = ','.join(map(str, temp))
        temp1 = temp1.replace("nan", "?")
        if row == len(data.index) - 1:
            new_file.write(temp1)
        else:
            new_file.write(temp1 + '\n')
    new_file.close()

# Convert csv to arff
def arff2csvConvert(fileName, folderName):
    columns = []
    contents = []

    filePath = Paths.arff_input + fileName

    print(Paths.arff_output + removeExtention(fileName))

    if not os.path.exists(filePath):
        print('File Not Found!!!')
        return

    with open(filePath,'r') as arffFile:
        lines = arffFile.readlines()
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                if line.startswith('@attribute'):
                    #column
                    header = line.strip()
                    header = header.replace("@attribute ", "")
                    header = header.replace(" numeric", "")
                    header = header.replace(" string", "")
                    header = header.replace(" {no,yes}", "")
                    columns.append(header)
                elif line.startswith("@relation") or line.startswith("@data"):
                    #no no
                    line.strip()
                else:
                    # content
                    content = line.strip()
                    content = content.replace("?", "")
                    contents.append(content)

    # create file

    if not os.path.exists(Paths.csv_output + folderName):
        os.makedirs(Paths.csv_output + folderName)

    new_file = open(Paths.csv_output + removeExtention(fileName) + ".csv", 'w+')
    # write header
    temp1 = ''
    temp1 += ','.join(columns)
    new_file.write(temp1 + "\n")
    #write content
    for row in contents:
        new_file.write(row + "\n")
    new_file.close()

def main():
    oper = -1
    while int(oper) != 0:
        print('**************************************')
        print('Choose one of the following: ')
        print('1 - Pre Processing')
        print('2 - Convert IS_DROP_OUT to YES/NO')
        print('3 - Convert CSV to ARFF')
        print('4 - Convert ARFF to CSV')
        print('0 - Exit')
        print('**************************************')
        oper = int(input("Enter your options: "))

        if oper == 0:
            exit()
        elif oper == 1:
            preprocessing()
        elif oper == 2:
            readFileConvert()
        elif oper == 3:
            #CSV
            start_time = time.time()
            getFileList(True)
            end_time = time.time()
            print '(Time to convert: %s)' % (end_time - start_time)
        elif oper == 4:
            #ARFF
            start_time = time.time()
            getFileList(False)
            end_time = time.time()
            print '(Time to convert: %s)' % (end_time - start_time)

if __name__ == "__main__":
    main()
