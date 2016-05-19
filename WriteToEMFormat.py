__author__ = 'shreya'

#RAWDATABase = "LiveExperiments/OrdinaryPoolResultsCSV"
RAWDATAMid = "LiveExperiments/NormalPoolResultsCSV"
RAWDATAStarred = "LiveExperiments/MasterPoolResultsCSV"
NUMOFLABELLERSBase = 54
#NUMOFLABELLERSMid = 54
NUMOFLABELLERSStarred = 35
TOTALLABELS = 6075
NUMOFTASKS = 150

#inputfile1 = open(RAWDATABase,'r')
inputfile2 = open(RAWDATAStarred,'r')
inputfile3 = open(RAWDATAMid,'r')

outputfile = open("EM/emdata",'w')
outputfile2 = open("OptimalLabelingRelease1.0.3/emoriginal",'w')

inputfile = []

#inputfile.append(inputfile1)
inputfile.append(inputfile2)
inputfile.append(inputfile3)

NumOfLabellers = []
NumOfLabellers.append(NUMOFLABELLERSBase)
NumOfLabellers.append(NUMOFLABELLERSStarred)

outputfile.write("%d %d %d %d %d %f" % (TOTALLABELS, NUMOFLABELLERSBase + NUMOFLABELLERSStarred, NUMOFTASKS, 1, 2, 0.5000))
outputfile2.write(("%d %d %d %f") % (TOTALLABELS, NUMOFLABELLERSBase + NUMOFLABELLERSStarred, NUMOFTASKS, 0.5))

count = 0
labeller = -1

for x in xrange(2):
    for line in inputfile[x]:
        labeller += 1
        temp = (line.rstrip()).split(',')
        temp = map(int,temp)
        for q in xrange(len(temp)):
            if(temp[q]!=2):
                count += 1
                outputfile.write("\n%d %d %d %d %d %f" % (q, labeller, 0, 0, temp[q], 0.5000))
                outputfile2.write("\n%d %d %d" % (q, labeller,temp[q]))

print count




