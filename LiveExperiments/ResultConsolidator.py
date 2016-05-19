__author__ = 'shreya'

#Makes the output of the MTurk Experiments compatible with our system.




rawResults = open("MasterPoolResultsFinal", "r")

mode = 0 #Depicts which data format the line from rawData is in. 0 for format with Assignment ID; 1 for without.

dataArray = [] #2D arrray that stores all the data, each row being a worker; and each column being a task. Value is 1 if worker answered 1, 0 is worker answered 0, blank otherwise.

workersAnsweredYet = {}
counter = 0

questiionsDiscoveredYet = {}
qCount = 0

for line in rawResults:
    answers = (line.rstrip()).split('|')
    if len(answers)==1:
        if answers[0] == "-":
            mode = 1
        continue

    wID = answers[0]
    if wID not in workersAnsweredYet:
        workersAnsweredYet[wID] = counter
        counter += 1
        dataArray.append(["2"]*150)

    rowNumber = workersAnsweredYet[wID]

    if mode==0:
        answers = answers[2:]
    else:
        answers = answers[1:]

    for ans in answers:
        [qNo, ballot] = (ans.rstrip()).split(',')
        if(qNo not in questiionsDiscoveredYet):
            questiionsDiscoveredYet[qNo] = qCount
            qCount += 1

        dataArray[rowNumber][questiionsDiscoveredYet[qNo]] = ballot


rawResults.close()

print "Total number of workers are " + str(counter)

resultsFile = open("MasterPoolResultsCSV",'w')

realQuestionsLookUp = open("questionsLookUp",'w')

for x in questiionsDiscoveredYet.keys():
    realQuestionsLookUp.write(x + "\t" + str(questiionsDiscoveredYet[x]) + "\n")


for i in xrange(len(dataArray)):
    resultsFile.write(dataArray[i][0])
    for j in range(1,len(questiionsDiscoveredYet)):
        resultsFile.write("," + dataArray[i][j])
    resultsFile.write("\n")


"""
taboo = open("tabooQuestions",'w')

for j in xrange(201):
    flag = True
    for i in xrange(counter):
        if dataArray[i][j]=="1" or dataArray[i][j]=="0":
            flag=False
            break
    if(flag):
        taboo.write(str(j) + "\n")
resultsFile.close()
"""




