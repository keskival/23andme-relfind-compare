#!/usr/bin/python

import csv
import re
import sys
import codecs

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import matplotlib.transforms as mtransforms
import matplotlib.text as mtext

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

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def readFile(file, people):
    with codecs.open(file, mode='rb', encoding='utf-8') as csvfile:
        relativereader = unicode_csv_reader(csvfile, delimiter=',')
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

fig, ax = plt.subplots(figsize=(5.5,5.5))

# Note: distance1 + distance2 >= 2
# [-1, 0]->[x,y]->[1,0]

# dx1^2+y^2 = distance1^2
# dx2^2+y^2 = distance2^2
# dx1+dx2 = 2
# => dx2 = 2 - dx1
# => (2 - dx1)^2+y^2 = distance2^2
# x = dx1-1 => dx1 = x + 1
# (2 - (x + 1))^2 + y^2 = distance2^2
# => (1 - x)^2 + y^2 = distance2^2

# (x+1)^2+y^2 = distance1^2
# (x-1)^2+y^2 = distance2^2
# => y^2 = distance1^2 - (x+1)^2 = distance2^2 - (x-1)^2
# => (x+1)^2 - (x-1)^2 = distance1^2 - distance2^2
# => x^2 + 2x + 1 - (x^2 - 2x + 1) = distance1^2 - distance2^2
# => x = (distance1^2 - distance2^2) / 4
# => y = distance1^2 - (x + 1)^2

xs = []
ys = []

# Closeness values are between 0 and 100, but most typically something below 1.
# We use the maximum value to scale the graphic to sane distances.
maxCloseness = 0

for (person, (closeness1, closeness2)) in common.items():
    if float(closeness1) > maxCloseness:
        maxCloseness = float(closeness1)
    if float(closeness2) > maxCloseness:
        maxCloseness = float(closeness2)

for (person, (closeness1, closeness2)) in common.items():
    # Scaling between 2 and 2 + maxCloseness * 5
    # The distance between the persons to compare is set at 2.
    distance1 = (maxCloseness - float(closeness1)) / maxCloseness + 1.0
    distance2 = (maxCloseness - float(closeness2)) / maxCloseness + 1.0
    x = (distance1 ** 2.0 - distance2 ** 2.0) / 4.0
    y = distance1 ** 2.0 - (x + 1) ** 2.0
    xs.append(x)
    ys.append(y)
    ax.text(x, y, person)
    

# The scatter plot.

ax.scatter(xs, ys)
ax.set_aspect(1.)

plt.xlim((-1.0,1.0))
plt.show()

