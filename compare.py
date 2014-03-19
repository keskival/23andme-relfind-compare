#!/usr/bin/python

import csv
import re
import sys

if len(sys.argv) != 3:
    print "This utility is for comparing 23andme.com relative finder CSV export files between two persons."
    print "Usage:"
    print "./compare.py relative_finder_First_Last_date1.csv relative_finder_First_Last_date2.csv"
    print "The output is the map of shared relatives with the respective shared DNA percentages for file1 and file2 respectively."
    exit(0)

# For example: "relative_finder_First_Last_20131105.csv"
file1 = sys.argv[1]
file2 = sys.argv[2]

file1People = dict()
file2People = dict()

def readFile(file, people):
    with open(file, 'rb') as csvfile:
        relativereader = csv.reader(csvfile, delimiter=',')
        for row in relativereader:
            name = row[0]
            percent = row[6]
            if name:
                if "%" in percent:
                    percentre = re.search('(\d*\.\d*)%', percent)
                    percentvalue = percentre.group(1)
                    people[name] = percentvalue
readFile(file1, file1People)
readFile(file2, file2People)

common = dict()
for (person, value) in file1People.items():
    if person in file2People:
        common[person] = (value, file2People[person])
print common
