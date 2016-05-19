from ModelLearning.utils import *
from ModelLearning.genPOMDP import *
from Data import *
from Ballots import *

import time
import subprocess
from random import random
from os import mkdir, rmdir
from copy import deepcopy
from math import floor

#Statuses
DONE = 2
WAITING_FOR_TURKER = 1
READY_FOR_ACTION = 0

#costList = [1.0,3.0]
#gammaList = [1.0,0.5]

def numberLeft(statuses):
    count = 0
    for status in statuses:
        if status != DONE:
            count += 1
    return count

def solve(mt, numStates, numberOfProblems, numberOfWorkerPools, nameOfTask, value, priceList, gammaList, scaleFactor,
          ZMDPPATH, URL, EMPATH, fastLearning, timeLearning, 
          taskDuration, debug = False):

    costList = map(lambda x: scaleFactor*x, priceList)
    #Initialize array of difficulties
    difficulties = getDifficulties(0.1)

    WORKERPOOLACTIONS = range(numberOfWorkerPools)
    SUBMITZERO = numberOfWorkerPools
    SUBMITONE = numberOfWorkerPools+1

    choices = [{'0':0,'1':1} for i in range(0, numberOfProblems)]
    inversechoices = [{0:'0',1:'1'} for i in range(0, numberOfProblems)]
    choicesindex = [0 for i in range(0, numberOfProblems)]

    print "Initializing World State"

    #Initialize status, answers, costs, HITIds, userWorkers, available actions,
    #actions that the agent took
    statuses = [READY_FOR_ACTION for i in range(0, numberOfProblems)]
    answers = [-1 for i in range(0, numberOfProblems)]
    costs = [0 for i in range(0, numberOfProblems)]
    HITIds = []
    usedWorkers = [[] for i in range(0, numberOfProblems)] #Should be a set
    actions = range(0, numberOfWorkerPools+2)
    agentActions = [-1 for i in range(0, numberOfProblems)]    
    ballots = Ballots(EMPATH,numberOfWorkerPools,gammaList)

    #We should start out with uniform beliefs
    belief = [1 for i in range(numStates)]
    belief[numStates-1] = 0
    belief = normalize(belief)
    beliefs = [deepcopy(belief) for i in range(numberOfProblems)]
    #print beliefs[0]

    serialize(numberOfProblems, statuses, answers, costs,
              HITIds, usedWorkers, actions, agentActions,
              beliefs, ballots)

    #We keep the observations around for RL purposes
    #observations0 = [[] for i in range(0, numberOfProblems)]
    #observations1 = [[] for i in range(0, numberOfProblems)]

    #What is this for?
    observations = []
    for i in xrange(numberOfProblems):
        observations.append([])
        for j in xrange(numberOfWorkerPools):
            observations[i].append([])

    gammas = ballots.calcAverageGammas() #Gammas contains number of worker pool averages

    print "Reading Policy"

    ###########################################################
    #Read the policy that we will begin with
    #You can choose a policy that's already been learned or learn
    #a new one
    ###########################################################
    #genPOMDP(filename,reward,costList,gammaList,numberofWorkerpools)
    fpipe = open('pipe.info','r')
    fpipe.readline()
    pathForPolicy = fpipe.readline().rstrip()
    fpipe.close()

    try:
        policy = readPolicy(pathForPolicy + "out.policy", numStates)
    except IOError:
        genPOMDP('log/pomdp/rl.pomdp', value * -1,costList, gammaList, numberOfWorkerPools)
        #Solve the POMDP

        zmdpDumpfile = open('log/pomdp/zmdpDump', 'w')
        subprocess.call('%s solve %s -o %s -t %d' % (
                ZMDPPATH,
                'log/pomdp/rl.pomdp',
                pathForPolicy + 'out.policy',
                timeLearning),
                        stdout=zmdpDumpfile,
                        shell=True,
                        executable="/bin/bash")
        zmdpDumpfile.close()

                        #Read the policy that we will begin with
        policy = readPolicy(pathForPolicy + 'out.policy', numStates)
        print policy.keys()

    print "POMDP Generated, POMDP Solved, Policy read"
    print "Initialization Complete"
    
    #Begin the experiment
    iterationNumber = -1
    while numberLeft(statuses) != 0:
        iterationNumber += 1
        # availableQuestions0 = []
        # availableQuestions1 = []
        availableQuestions = [[] for _ in xrange(numberOfWorkerPools)]
        if debug:
            print "Waiting 1 seconds"
        #time.sleep(1)
        print "Beginning iteration %d with %d questions remaining" % (iterationNumber, numberLeft(statuses))
        #First we read from file all our data.
        (nop, statuses, answers, costs, HITIds, usedWorkers, actions, agentActions, beliefs, ballots) = unSerialize()
        #Loop through all the problems regardless of the ones left. Can maintain a set of problems left to speed up
        for i in range(0, numberOfProblems):
            if debug:
                print "Starting Problem %d:" % i
            if statuses[i] == DONE:
                if debug:
                    print "Problem %d is done" % i
                continue
            elif statuses[i] == READY_FOR_ACTION:
                beliefState = beliefs[i]
                bestAction = findBestAction(actions, policy, beliefState)
                #agentActions[i] = bestAction
                #Exploration versus exploitation
                #Explore
                #Don't activate RL until there is uncertainty about average worker gammas on each pool
                #For the purpose of initial simulation, we will push gamma average to be the original of the generated
                '''
                if random() <= 0.1:
                    if bestAction < numberOfWorkerPools:
                        bestAction = (bestAction + 1) % numberOfWorkerPools
                    else:
                        bestAction = floor(random()*numberOfWorkerPools)
                '''
                bestAction = int(bestAction)
                agentActions[i] = bestAction
                #Depending on the ballot0/ballot1, push to one or the other workflow
                if bestAction < numberOfWorkerPools:
                    if debug:
                        print "Problem %d requested to Worker Pool %d" % (i, bestAction)
                        availableQuestions[int(bestAction)].append(i)

                    costs[i] += costList[bestAction]
                    statuses[i] = WAITING_FOR_TURKER

                elif bestAction == SUBMITZERO or bestAction == SUBMITONE:
                    ballots.addQuestionAndRelearn(
                        observations[i],
                        bestAction - numberOfWorkerPools,
                        getMostLikelyDifficulty(beliefs[i], difficulties),
                        fastLearning)

                    gammas = ballots.calcAverageGammas()
                    '''
                    if not fastLearning:
                        print "Problem %d complete: Relearning." % i
                        #Generate the POMDP

                        genPOMDP('log/pomdp/rl.pomdp', value * -1, costList, gammas, numberOfWorkerPools)
                        #Solve the POMDP
                        zmdpDumpfile = open('log/pomdp/zmdpDump', 'w')

                        subprocess.call('%s solve %s -o %s -t %d' % (
                                ZMDPPATH,
                                'log/pomdp/rl.pomdp',
                                'log/pomdp/out.policy',
                                timeLearning),
                                        stdout=zmdpDumpfile,
                                        shell=True,
                                        executable="/bin/bash")
                        zmdpDumpfile.close()

                        #Read the policy that we will begin with 
                        policy = readPolicy("log/pomdp/out.policy", 
                                            numStates)
                        print policy.keys()
                        print "POMDP Generated, POMDP Solved, Policy read"
                    '''
                    if bestAction == SUBMITZERO:
                        if debug:
                            print "Problem %d submitted answer 0" % i 
                        answers[i] = 0
                    else:
                        if debug:
                            print "Problem %d submitted answer 1" % i
                        answers[i] = 1
                    statuses[i] = DONE
            elif statuses[i] == WAITING_FOR_TURKER:
                continue

        for i in xrange(numberOfWorkerPools):
            while True:
                try:
                    mkdir('locks/aql' + str(i) + 'lock')
                    break
                except OSError:
                    pass

        #We only append to these files.
        aql = [open('log/aql'+str(i),'a') for i in xrange(numberOfWorkerPools)]

        for i in xrange(numberOfWorkerPools):
            for aq in availableQuestions[i]:
                aql[i].write('%d' % aq)
                HITIds.append(mt.createHIT(i,URL,nameOfTask,priceList[i],taskDuration,31536000,1,aq))

        #Close files and release locks
        for i in xrange(numberOfWorkerPools):
            aql[i].close()
            rmdir('locks/aql' + str(i) + 'lock')

        #Now we go through all the hits and get observations
        nextHITIds = []
        for HITId in HITIds: 
            hits = mt.getHIT(HITId)
            observation = ''
            for hit in hits: #there really should only be one
                if hit.HITStatus == 'Reviewable':
                    print HITId
                    assignments = mt.getAssignments(HITId, 
                                                    page_size=100,
                                                    page_number=1)
                    for assignment in assignments: #there should only be one

                        print assignment #Observation,workerId,AssignmentId,pn

                        observation = mt.getObservation(assignment)
                        pn = mt.getProblemNumber(assignment)
                        print "THE OBSERVATION"
                        print observation

                        if observation in choices[pn]:
                            observation = choices[pn][observation]

                        else:
                            print "Never go here!"
                            inversechoices[pn][choicesindex[pn]] = observation
                            choices[pn][observation] = choicesindex[pn]
                            choicesindex[pn] += 1
                            observation = choices[pn][observation]
                        
                        workerId = mt.getWorker(assignment)
                        mt.approveAssignment(assignment)

                        if debug:
                            print "Problem %d received observation %d" % (pn, observation)
                        #Now that we have an observation, we need to update our belief
                    beliefs[pn] = updateBelief(beliefs[pn], #agentActions[pn],
                                              observation, difficulties,
                                              ballots.getWorkerGammaGivenPool(workerId,agentActions[pn]))

                    f = open('log/results/observations%dw%d' % (pn,agentActions[pn]),'a+')
                    observations[pn][agentActions[pn]].append((observation,workerId))
                    f.write('%s\t%s\n' % (inversechoices[pn][observation],workerId))
                    f.close()
                                                  
                    mt.disposeHIT(HITId) 
                    statuses[pn] = READY_FOR_ACTION
                else:
                    nextHITIds.append(HITId)
        HITIds = nextHITIds

        #Write our world state to file in case something crashes and burns
        serialize(numberOfProblems, statuses, answers, 
                  costs, HITIds, usedWorkers,
                  actions, agentActions, beliefs, ballots)

    fp = open('pipe.info','r')
    pathToLog = fp.readline().rstrip()
    path = fp.readline().rstrip()
    fp.close()

    '''
    f = open('log/results/answers', 'w') 
    for i in range(numberOfProblems):
        f.write('%s\n' % inversechoices[i][answers[i]])
    f.close()
    '''
    '''
    fDiff = open('SimulatedData/DifficultiesFileBell','r')
    trueDifficulties = [float(line.rstrip().split(",")[1]) for line in fDiff][0:numberOfProblems]
    fDiff.close()

    fAns = open('SimulatedData/trueQuestionAnswers.txt','r')
    trueAnswers = [int(line.rstrip().split("\t")[1]) for line in fAns][0:numberOfProblems]
    fAns.close()

    fSim = open('SimulatedData/WorkerPool.info','r')
    linesInSim = [line.rstrip() for line in fSim]
    totalWorkersOriginal = int(linesInSim[1]) + int(linesInSim[4])
    fSim.close()

    fGammas = open('SimulatedData/trueWorkerGammas.txt','r')
    trueGammas = [float(line.rstrip().split("\t")[1]) for line in fGammas][0:totalWorkersOriginal]
    fGammas.close()

    answers = map(lambda x: int(x),answers)
    accuracy = float((numberOfProblems - reduce(lambda x,y: x+y,map(lambda x,y: abs(x-y),answers,trueAnswers)))*100.0)/numberOfProblems

    f = open(pathToLog,'w')
    fc = open(path + "costs",'a')
    fa = open(path + "accuracies",'a')

    f.write('Number of Worker Pools: %d\n'% numberOfWorkerPools)
    f.write('Number of Workers in Pool 1: %d\n' %int(linesInSim[1]))
    f.write('Original mean,standardDev for Pool 1: %f,%f\n'%(float(linesInSim[2]),float(linesInSim[3])))
    f.write('Number of Workers in Pool 2: %d\n'%int(linesInSim[4]))
    f.write('Original mean,standardDev for Pool 2: %f,%f\n'%(float(linesInSim[5]),float(linesInSim[6])))
    f.write('Number of Problems: %d\n'%numberOfProblems)
    f.write('ProblemNo,Answer,TrueAnswer,Cost,Difficulty,TrueDifficulty\n')
    for i in xrange(numberOfProblems):
        f.write('%d,%d,%d,%f,%f,%f\n' % (i,int(answers[i]),trueAnswers[i],costs[i],float(getMostLikelyDifficulty(beliefs[i], difficulties)),trueDifficulties[i]))
    f.write('WorkerID,Gamma,TrueGamma\n')
    for workerPool in ballots.workersToGammas:
        for workerId in workerPool:
            f.write('%d,%f,%f\n' % (int(workerId),workerPool[workerId],trueGammas[int(workerId)]))
    f.write('Average Cost: %f\n' % average(costs))
    f.write('Accuracy: %f\n' % accuracy)
    zipDiff = sorted(zip(trueDifficulties,map(lambda x,y: abs(x-y),answers,trueAnswers)))
    zipCost = sorted(zip(trueDifficulties,costs))
    for i in xrange(10):
        tempZipDiff = [term[1] for term in zipDiff[i*10:(i+1)*10]]
        tempZipCost = [term[1] for term in zipCost[i*10:(i+1)*10]]
        accuracyTerm = reduce(lambda x,y:x+y,tempZipDiff)
        partialAccuracy = float((10 - accuracyTerm)*100.0)/10
        f.write('Accuracy %d: %f\n' %(i,partialAccuracy))
        f.write('Cost %d: %f\n' %(i,average(tempZipCost)))
        if (i == 9):
            fc.write('%f\n' % average(tempZipCost))
            fa.write('%f\n' % partialAccuracy)
        else:
            fc.write('%f,' % average(tempZipCost))
            fa.write('%f,' % partialAccuracy)
    f.close()
    fc.close()
    fa.close()'''


    fAns = open('client/groundTruths','r')
    fpp = open('questionsLookUp','r')
    mapping = {}
    imapping = {}
    for line in fpp:
        l = map(int,line.rstrip().split("\t"))
        mapping[l[0]] = l[1]
        imapping[l[1]] = l[0]

    trueAnswersTemp = [int(line.rstrip().split(" ")[1]) for line in fAns]#[0:numberOfProblems]
    trueAnswers = 150*[-1]
    for prob in xrange(numberOfProblems):
        trueAnswers[prob] = trueAnswersTemp[imapping[prob]]
    fAns.close()
    fpp.close()
    answers = map(lambda x: int(x),answers)
    accuracy = float((numberOfProblems - reduce(lambda x,y: x+y,map(lambda x,y: abs(x-y),answers,trueAnswers)))*100.0)/numberOfProblems
    f = open(pathToLog,'w')
    f.write('ProblemNo,Answer,TrueAnswer,Cost,Difficulty\n')
    for i in xrange(numberOfProblems):
        f.write('%d,%d,%d,%f,%f\n' % (i,int(answers[i]),trueAnswers[i],costs[i],float(getMostLikelyDifficulty(beliefs[i], difficulties))))
    f.write('WorkerID,Gamma\n')
    for workerPool in ballots.workersToGammas:
        for workerId in workerPool:
            f.write('%d,%f\n' % (int(workerId),workerPool[workerId]))
    f.write('Average Cost: %f\n' % average(costs))
    f.write('Accuracy: %f\n' % accuracy)
    f.close()

    return (costs, answers)
