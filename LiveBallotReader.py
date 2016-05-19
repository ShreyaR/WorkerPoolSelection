
from random import random, gauss, shuffle, gammavariate,betavariate,uniform,seed
from ModelLearning.utils import generateBallot
from time import time,sleep

# Vary these parameters during testing
numOfQuestions = 150
numOfWorkerPools = 3

numOfWorkersInEachPool = [35,54,54]

mode = 0

if mode==0:
    pools = [0,1]
elif mode==1:
    pools = [1,2]
else:
    pools = [0,2]

#mode0 = [0,1]
#mode1 = [1,2]
#mode2 = [0,2]

wID = -1

data = []

for i in xrange(numOfWorkerPools):
    data.append([])



for i in pools:
    if i == 0:
        datafile = open("LiveExperiments/MasterPoolResultsCSV",'r')
    elif i == 1:
        datafile = open("LiveExperiments/NormalPoolResultsCSV",'r')
    else:
        datafile = ordinary = open("LiveExperiments/OrdinaryPoolResultsCSV",'r')


    for line in datafile:
        ballots = map(int, line.split(","))
        data[i].append(ballots)

    datafile.close()

"""
tabooFile = open("LiveExperiments/tabooQuestions",'r')
taboo = set()

for line in tabooFile:
    taboo.add(int(line.rstrip()))
"""

#print taboo
#print len(taboo)

counter = -1

#counter

for i in pools:
    counter+=1
    for q in xrange(numOfQuestions):
        #print q
        #if(q not in taboo):
            ballots = []
            #print i
            for workerNumber in xrange(numOfWorkersInEachPool[i]):
                #print workerNumber

                if(mode == 0):
                    if i == 0:
                        wID = workerNumber
                    else:
                        wID = workerNumber + numOfWorkersInEachPool[0]
                elif mode==1:
                    if i==1:
                        wID = workerNumber
                    else:
                        wID = workerNumber + numOfWorkersInEachPool[1]
                else:
                    if i==0:
                        wID = workerNumber
                    else:
                        wID = workerNumber + numOfWorkersInEachPool[0]

                #print workerNumber, i , q

                if data[i][workerNumber][q] != 2:
                    temp = wID,data[i][workerNumber][q]
                    ballots.append(temp)
            shuffle(ballots)


            #f = open('SimulatedData%d/w%dq%d' % (mode,counter, q), 'w')
            f = open('SimulatedData/w%dq%d' % ((counter+1)%2, q), 'w')

            f.write(str(ballots[0][1]) + '\t' + str(ballots[0][0]))
            for x in range(1,len(ballots)):
                f.write('\n' + str(ballots[x][1]) + '\t' + str(ballots[x][0]))
            f.close()





"""
for q in xrange(numOfQuestions):

    for wpool in xrange(numOfWorkerPools):
        f = open('SimulatedData/w%dq%d' % (wpool, q), 'w')
        AnswersForPoolQuestion = []
        for w in xrange(numOfWorkersInEachPool[wpool]):
            wID += 1
            # print(str(wID) + '\n')
            gammaTemp = GammaSet[wID]
            workerAnswer = generateBallot(gammaTemp,difficulties[q],v)
            temp = workerAnswer,wID
            AnswersForPoolQuestion.append(temp)
        shuffle(AnswersForPoolQuestion)
        f.write(str(AnswersForPoolQuestion[0][0]) + '\t' + str(AnswersForPoolQuestion[0][1]))
        for i in range(1,numOfWorkersInEachPool[wpool]):
            f.write('\n' + str(AnswersForPoolQuestion[i][0]) + '\t' + str(AnswersForPoolQuestion[i][1]))
        f.close()
    wID = -1
"""