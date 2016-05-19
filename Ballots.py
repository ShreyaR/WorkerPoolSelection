import subprocess
import os
from numpy import average
from time import sleep
class Ballots:


    #What are Gamma0, and Gamma1? For different workflows?
    def __init__(self, emp, numberOfWorkerPools, gammaList):
        self.EMPATH = emp
        #Ballots received from each worker pool
        self.ballots = [[] for i in xrange(numberOfWorkerPools)]
        self.numQuestions = 0
        self.numWorkers = 0
        self.numLabels = 0
        self.numPools = numberOfWorkerPools
        self.workersToIntegers = {}
        self.integersToWorkers = {}
        self.workersToPools = {}
        self.defaultGammaList = gammaList
        self.problemsToAnswers = {}
        #Workers are separated by the pools which they belong to and their corresponding gammas are noted
        self.workersToGammas = [{} for i in xrange(numberOfWorkerPools)]
        self.workersToNumberCompleted = {}


    def writeToEMFormat(self):
        outputfile = open('log/em/ballots.eminput', 'w')
        outputfile.write('%d %d %d %d %d %f\n' % (self.numLabels, self.numWorkers, self.numQuestions, 1, self.numPools, 0.5))
        for i in xrange(self.numPools):
            for problem,j in zip(self.ballots[i],range(self.numQuestions)):
                for vote,workerId in problem:
                    if (self.problemsToAnswers[j] == 0):
                        outputfile.write('%d %d %d %d %d %f\n' % (j,self.workersToIntegers[workerId],0,i,vote,0.5))
                    else:
                        outputfile.write('%d %d %d %d %d %f\n' % (j,self.workersToIntegers[workerId],0,i,vote,0.5))
        outputfile.close()

    def runEM(self):
        self.writeToEMFormat()
        #print "I Want to run the EM"
        #os.chdir("/Users/kgoel93/Desktop/Clutter/Semester8/Mausam/AgentHuntUpdatedReleaseLiveExperiments/EM")
        os.chdir("/Users/shreyarajpal/Desktop/MausamOld/AgentHuntUpdatedReleaseLiveExperiments/EM")
        EMDone = False
        while not EMDone:
            outputfile = open('../log/em/emresults', 'w')
            subprocess.call('%s ../log/em/ballots.eminput' % self.EMPATH,stdout=outputfile,shell=True)
            outputfile.close()
            inputfile = open('../log/em/emresults', 'r').read().split("\n")
            inputfile = inputfile[0:len(inputfile) - 1]
            for nextLine in inputfile:
                if 'Beta' in nextLine:
                    EMDone = True
        #os.chdir("/Users/kgoel93/Desktop/Clutter/Semester8/Mausam/AgentHuntUpdatedReleaseLiveExperiments")
        os.chdir("/Users/shreyarajpal/Desktop/MausamOld/AgentHuntUpdatedReleaseLiveExperiments")
        #Now we want to format the output to be nice

        gammaoutputs = open('log/em/gammas.emresults','w')
        diffoutputs = open('log/em/diffs.emresults','w')
        posterioroutputs = open('log/em/posteriors.emresults','w')
        inputfile = open('log/em/emresults', 'r').read().split("\n")
        inputfile = inputfile[0:len(inputfile) - 1]
        for i in range(0, len(inputfile)):
            nextLine = inputfile[i]
            if 'Iteration' in nextLine:
                continue
            #These are problem difficulties
            elif 'Beta' in nextLine:
                d = float(nextLine.split("=")[1].strip())
                diffoutputs.write('%f\n' % d)

            elif 'P' in nextLine:
                p = float(nextLine.split("=")[2].strip())
                posterioroutputs.write('%f\n' % p)
            #These are worker gammas.
            else:
                g = float(nextLine)
                gammaoutputs.write('%f\n' % g)

        gammaoutputs.close()
        diffoutputs.close()
        posterioroutputs.close()

    #diff is the difficulty of the question
    def addQuestionAndRelearn(self, obs, answer, diff, fast = True):
        self.problemsToAnswers[self.numQuestions] = answer
        self.numQuestions += 1

        for i in xrange(self.numPools):
            self.ballots[i].append(obs[i])
            for (vote,workerId) in obs[i]:
                if workerId not in self.workersToIntegers:
                    self.workersToIntegers[workerId] = self.numWorkers
                    self.integersToWorkers[self.numWorkers] = workerId
                    self.workersToPools[workerId] = i
                    self.numWorkers += 1
            self.numLabels += len(obs[i])

        if not fast:
            self.runEM()
            self.readGammaResults()
        else:
            for i in xrange(self.numPools):
                for vote,workerId in obs[i]:
                    if workerId not in self.workersToNumberCompleted:
                        self.workersToNumberCompleted[workerId] = 0
                    if workerId not in self.workersToGammas[i]:
                        self.workersToGammas[i][workerId] = self.defaultGammaList[i]

                    alpha = 0.5 / (self.workersToNumberCompleted[workerId] + 1)

                    if answer == vote:
                        self.workersToGammas[i][workerId] -= (diff * alpha)
                        if self.workersToGammas[i][workerId] < 0.01:
                            self.workersToGammas[i][workerId] = 0.01
                    else:
                        self.workersToGammas[i][workerId] += (1.0-diff) * alpha
                    self.workersToNumberCompleted[workerId] += 1


    def readGammaResults(self):
        infile = open('log/em/gammas.emresults','r')
        infile = infile.read().split("\n")
        infile = infile[0:len(infile) - 1]
        for i in xrange(0,len(infile)):
            self.workersToGammas[self.workersToPools[self.integersToWorkers[i]]][self.integersToWorkers[i]] = float(infile[i])

    #Each worker belongs to exactly one worker pool. Return the pool, gamma value of
    # the worker.
    def getWorkerGamma(self,workerId):
        print self.workersToGammas
        #Check if the worker belongs to any pool
        for i in xrange(self.numPools):
            if workerId in self.workersToGammas[i]:
                return (i,self.workersToGammas[i][workerId])
        print "There's a problem."
        return LookupError #This should never happen


    def getWorkerGammaGivenPool(self,workerId,poolNumber):
        if workerId in self.workersToGammas[poolNumber]:
            return self.workersToGammas[poolNumber][workerId]
        else:
            return self.calcAverageGammas()[poolNumber]


    def calcAverageGammas(self):
        print self.workersToGammas
        averages = []
        for i in xrange(self.numPools):
            gammas = []
            for _,value in self.workersToGammas[i].items():
                gammas.append(value)
            if len(gammas) == 0:
                averages.append(self.defaultGammaList[i])
            else:
                averages.append(average(gammas))
        return tuple(averages)
 
