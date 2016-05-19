__author__ = 'shreya'

from random import random, gauss, shuffle, gammavariate,betavariate,uniform,seed
from ModelLearning.utils import generateBallot
from time import time,sleep

seed(42)

poolInfo = open('SimulatedData/WorkerPool.info', 'r')

# Vary these parameters during testing
numOfQuestions = 100
numOfWorkerPools = int(poolInfo.readline())

numOfWorkersInEachPool = []
gammaMuPrior = [] #For Gamma-distributions, refers to 'Shape' parameter
gammaSigmaPrior = [] #For Gamma distribution, refers to 'Scale' parameter
difficulties = []

diffFile = open('Experiments/DifficultiesFileBell', 'r')

'''
for i in xrange(10):
    for j in xrange(10):
        diff = uniform(float(i)/10,float((i+1))/10)
        difficulties.append(diff)

shuffle(difficulties)

for i in xrange(100):
        diffFile.write(str(i) + "," + str(difficulties[i]) + '\n')
'''


'''# For Difficulties sampled from a Bell-Curve
for i in xrange(numOfQuestions):
    diff = betavariate(2,2) #Beta distribution with alpha = 2 and beta = 2
    difficulties.append(diff)
    diffFile.write(str(i) + "," + str(difficulties[i]) + '\n')



# For Difficulties sampled from a Bi-modal Distribution
for i in xrange(numOfQuestions):
    diff = betavariate(0.5,0.5) #Beta distribution with alpha = 2 and beta = 2
    difficulties.append(diff)
    diffFile.write(str(i) + "," + str(difficulties[i]) + '\n')


diffFile.close()
sleep(10)
'''

difficulties = [float(line.rstrip().split(",")[1]) for line in diffFile]

for i in xrange(numOfWorkerPools):
    numOfWorkersInEachPool.append(int(poolInfo.readline()))
    gammaMuPrior.append(float(poolInfo.readline())) # When worker gammas are sampled from a Gamma distribution, this refers to 'Shape'
    gammaSigmaPrior.append(float(poolInfo.readline())) # When worker gammas are sampled from a Gamma distribution, this refers to 'Scale'

workerGammas = open('SimulatedData/trueWorkerGammas.txt', 'w')
trueAnswers = open('SimulatedData/trueQuestionAnswers.txt', 'w')

#Counter for worker IDs
wID = -1

GammaSet = {}

for wpool in xrange(numOfWorkerPools):
    for w in xrange(numOfWorkersInEachPool[wpool]):
        gamma = gammavariate(gammaMuPrior[wpool],gammaSigmaPrior[wpool])
        wID += 1
        workerGammas.write(str(wID) + '\t' + str(gamma) + '\n')
        GammaSet[wID] = gamma

# print GammaSet
seed(time())
wID = -1

for q in xrange(numOfQuestions):
    randNumForTrueAns = uniform(0,1)
    v = -1

    if randNumForTrueAns < 0.5:
        v = 0
    else:
        v = 1

    trueAnswers.write(str(q) + '\t' + str(v) + '\n')

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

workerGammas.close()
trueAnswers.close()