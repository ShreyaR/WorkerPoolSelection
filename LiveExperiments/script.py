__author__ = 'kgoel93'

import os
from numpy import average
directories = ['100','500','1000']
subdirectories = ['1.50','2.00','2.50','3.00','4.00','5.00','Unstarred']
subsubdirectories = ['Both','Starred']

for directory in directories:
    os.chdir(directory)
    fu = open('UnstarredAverages','w')
    for subdirectory in subdirectories:
        os.chdir(subdirectory)
        if (subdirectory == 'Unstarred'):
            costs = []
            accuracies = []
            for i in xrange(20):
                f = open(str(i),'r')
                for line in f:
                    if (line.rstrip().split(":")[0] == "Average Cost"):
                        costs.append(float(line.rstrip().split(":")[1].strip()))
                    elif (line.rstrip().split(":")[0] == "Accuracy"):
                        accuracies.append(float(line.rstrip().split(":")[1].strip()))
                f.close()
            fu.write("%f\n%f" % (average(costs),average(accuracies)))
        else:
            f1 = open('BothAverages','w')
            f2 = open('StarredAverages','w')
            for subsubdirectory in subsubdirectories:
                os.chdir(subsubdirectory)
                costs = []
                accuracies = []
                for i in xrange(20):
                    f = open(str(i),'r')
                    for line in f:
                        if (line.rstrip().split(":")[0] == "Average Cost"):
                            costs.append(float(line.rstrip().split(":")[1].strip()))
                        elif (line.rstrip().split(":")[0] == "Accuracy"):
                            accuracies.append(float(line.rstrip().split(":")[1].strip()))
                    f.close()
                if (subsubdirectory == "Both"):
                    f1.write("%f\n%f" % (average(costs),average(accuracies)))
                else:
                    f2.write("%f\n%f" % (average(costs),average(accuracies)))
                os.chdir("..")
            f1.close()
            f2.close()
        os.chdir("..")
    fu.close()
    os.chdir("..")