__author__ = 'kgoel93'

from os import system, mkdir
from time import sleep
import shutil

#To run either Live or Simulated experiments.
LIVEEXPERIMENT = True

#The results will be logged in this folder (including worker responses per ballot, average accuracy and cost.)
if (LIVEEXPERIMENT == True):
    RELATIVEPATH = 'LiveExperiments/'
else:
    RELATIVEPATH = 'Experiments/'
#How many times to repeat one experiment type.
NUMBER_OF_REPETITIONS = 1
SCALE = 100 #The value by which Cost must be scaled.
MODE = 1 #Mode 0 to write simulation parameters, Mode 1 to read them and run the experiments

#THIS FILE ONLY CONTAINS RELATIVE PATHS; NO NEED TO CHANGE PATHS HERE

#READ SIMULATION PARAMETERS from a file
# Format
# <simulation_no>
# -----Information about worker pools to be sampled from-----
# <num_workers_in_pool0>,<mean_gamma>,<std_dev_gamma>
# <num_workers_in_pool1>,<mean_gamma>,<std_dev_gamma>
# -----Information about the experiments-----
# <number_of_simulation_type_1 = c1>
# ----next c1 lines----
# <cost_of_wrong_answer>
# <number_of_simulation_type_2 = c2>
# ----next c2 lines----
# <relative_cost_of_starred_worker_pool>
# ----Repeat-----
# <simulation_no>
#...
#...
#-1 ---> Ends the file with a -1 and no new line carriage

def run(mode):
    if (mode == 0):
        print "Writing SimulationParameters!"
        writeSimulationParameters()
    else:
        print "Reading SimulationParameters and Running Experiments!"
        readAndRun()

def readAndRun():

    f = open(RELATIVEPATH + 'SimulationParameters','r')
    experimentNumber = int(f.readline())
    while (experimentNumber != -1):
        print "Experiment Number %d is starting." % experimentNumber
        print "---------------------------------"
        sleep(3)


        WP0_num,WP0_mean,WP0_stddev = f.readline().rstrip().split(",")
        WP0_num = int(WP0_num)
        WP0_mean = float(WP0_mean)
        WP0_stddev = float(WP0_stddev)

        WP1_num,WP1_mean,WP1_stddev = f.readline().rstrip().split(",")
        WP1_num = int(WP1_num)
        WP1_mean = float(WP1_mean)
        WP1_stddev = float(WP1_stddev)

        numberOfWrongAnswerCosts = int(f.readline())
        wrongAnswerCosts = []
        for _ in xrange(numberOfWrongAnswerCosts):
            wrongAnswerCosts.append(float(f.readline().rstrip()))

        numberOfStarredWorkerPoolCosts = int(f.readline())
        starredWorkerPoolCosts = []
        for _ in xrange(numberOfStarredWorkerPoolCosts):
            starredWorkerPoolCosts.append(float(f.readline().rstrip()))

        print "Read Parameters from SimulationParameters file."

        fw = open('SimulatedData/WorkerPool.info','w')
        fw.write("2\n")
        fw.write("%d\n" % WP0_num)
        fw.write("%f\n" % WP0_mean)
        fw.write("%f\n" % WP0_stddev)
        fw.write("%d\n" % WP1_num)
        fw.write("%f\n" % WP1_mean)
        fw.write("%f" % WP1_stddev)
        fw.close()

        name = "%d,%.2f,%.2f,%d,%.2f,%.2f" % (WP0_num,WP0_mean,WP0_stddev,WP1_num,WP1_mean,WP1_stddev)

        try:
            mkdir(RELATIVEPATH + '%s' % name)
        except OSError:
            pass

        shutil.copy('SimulatedData/WorkerPool.info',RELATIVEPATH + '%s' % name)

        print "Worker Distributions are..."
        print "Worker Pool 0: %d,%f,%f" % (WP0_num,WP0_mean,WP0_stddev)
        print "Worker Pool 1: %d,%f,%f" % (WP1_num,WP1_mean,WP1_stddev)

        sleep(3)

        for repetition in xrange(NUMBER_OF_REPETITIONS):
            print "Repetition %d is starting." % repetition
            sleep(1)

            if (not LIVEEXPERIMENT):
                system("python BallotGenerator.py")
                print "Generated new workers and ballots."
            else:
                system("python LiveBallotReader.py")
                print "Generated new workers and ballots."

            for wrongAnswerCost in wrongAnswerCosts:
                try:
                    mkdir(RELATIVEPATH + '%s/%d' % (name,wrongAnswerCost))
                except OSError:
                    pass
                try:
                    mkdir(RELATIVEPATH + '%s/%d/Unstarred' % (name,wrongAnswerCost))
                except OSError:
                    pass

                for starredWorkerPoolCost in starredWorkerPoolCosts:
                    try:
                        mkdir(RELATIVEPATH + '%s/%d/%.2f' % (name,wrongAnswerCost,starredWorkerPoolCost))
                    except OSError:
                        pass
                    try:
                        mkdir(RELATIVEPATH + '%s/%d/%.2f/Starred' % (name,wrongAnswerCost,starredWorkerPoolCost))
                    except OSError:
                        pass
                    try:
                        mkdir(RELATIVEPATH + '%s/%d/%.2f/Both' % (name,wrongAnswerCost,starredWorkerPoolCost))
                    except OSError:
                        pass
                    #ONLY STARRED WORKER POOL
                    fs = open('simulation.info','w')
                    fs.write("1\n")
                    fs.write("%d\n" % wrongAnswerCost)
                    fs.write("%f\n" % (starredWorkerPoolCost/SCALE))
                    fs.write("%f\n" % (WP1_mean*WP1_stddev))
                    fs.write("%d\n" % SCALE)
                    fs.write("1")
                    fs.close()
                    fp = open('pipe.info','w')
                    fp.write(RELATIVEPATH + "%s/%d/%.2f/Starred/%d\n" % (name,wrongAnswerCost,starredWorkerPoolCost,repetition))
                    fp.write(RELATIVEPATH + "%s/%d/%.2f/Starred/" % (name,wrongAnswerCost,starredWorkerPoolCost))
                    fp.close()
                    sleep(0.1)
                    system("python main.py > uselessLog")
                    print "Starred Worker Pool Complete"
                    #BOTH WORKER POOLS
                    fs = open('simulation.info','w')
                    fs.write("2\n")
                    fs.write("%d\n" % wrongAnswerCost)
                    fs.write("%f,%f\n" % (1.0/SCALE,starredWorkerPoolCost/SCALE))
                    fs.write("%f,%f\n" % ((WP0_mean*WP0_stddev),(WP1_mean*WP1_stddev)))
                    fs.write("%d\n" % SCALE)
                    fs.write("0")
                    fs.close()
                    fp = open('pipe.info','w')
                    fp.write(RELATIVEPATH + "%s/%d/%.2f/Both/%d\n" % (name,wrongAnswerCost,starredWorkerPoolCost,repetition))
                    fp.write(RELATIVEPATH + "%s/%d/%.2f/Both/" % (name,wrongAnswerCost,starredWorkerPoolCost))
                    fp.close()
                    sleep(0.1)
                    system("python main.py > uselessLog")
                    print "Both Worker Pools Complete"

                #ONLY UNSTARRED WORKER POOL
                fs = open('simulation.info','w')
                fs.write("1\n")
                fs.write("%d\n" % wrongAnswerCost)
                fs.write("%f\n" % (1.0/SCALE))
                fs.write("%f\n" % (WP0_mean*WP0_stddev))
                fs.write("%d\n" % SCALE)
                fs.write("0")
                fs.close()
                fp = open('pipe.info','w')
                fp.write(RELATIVEPATH + "%s/%d/Unstarred/%d\n" % (name,wrongAnswerCost,repetition))
                fp.write(RELATIVEPATH + "%s/%d/Unstarred/" % (name,wrongAnswerCost))
                fp.close()
                sleep(0.1)
                system("python main.py > uselessLog")
                print "Unstarred Worker Pool Complete"


        print "Finished all repetitions!"

        if not LIVEEXPERIMENT:


            print "Now pretty printing all the outputs!"
            sleep(3)
            #Repetitions end here
            for wrongAnswerCost in wrongAnswerCosts:
                for starredWorkerPoolCost in starredWorkerPoolCosts:

                    print 'ITS HAPPENING HERE!'
                    print name
                    print wrongAnswerCost
                    print starredWorkerPoolCost

                    fSA = open(RELATIVEPATH + "%s/%d/%.2f/StarredAverages" % (name,wrongAnswerCost,starredWorkerPoolCost),'w')
                    fBA = open(RELATIVEPATH + "%s/%d/%.2f/BothAverages" % (name,wrongAnswerCost,starredWorkerPoolCost),'w')
                    fcS = open(RELATIVEPATH + "%s/%d/%.2f/Starred/costs" % (name,wrongAnswerCost,starredWorkerPoolCost),'r')
                    faS = open(RELATIVEPATH + "%s/%d/%.2f/Starred/accuracies" % (name,wrongAnswerCost,starredWorkerPoolCost),'r')
                    fcB = open(RELATIVEPATH + "%s/%d/%.2f/Both/costs" % (name,wrongAnswerCost,starredWorkerPoolCost),'r')
                    faB = open(RELATIVEPATH + "%s/%d/%.2f/Both/accuracies" % (name,wrongAnswerCost,starredWorkerPoolCost),'r')

                    averageCostsStarred = [0.0]*10
                    averageAccuraciesStarred = [0.0]*10
                    averageCostsBoth = [0.0]*10
                    averageAccuraciesBoth = [0.0]*10
                    for lineNo in xrange(NUMBER_OF_REPETITIONS):
                        averageAccuraciesStarred = map(lambda x,y:x+y,[float(x) for x in faS.readline().rstrip().split(",")],averageAccuraciesStarred)
                        averageCostsStarred = map(lambda x,y:x+y,[float(x) for x in fcS.readline().rstrip().split(",")],averageCostsStarred)
                        averageAccuraciesBoth = map(lambda x,y:x+y,[float(x) for x in faB.readline().rstrip().split(",")],averageAccuraciesBoth)
                        averageCostsBoth = map(lambda x,y:x+y,[float(x) for x in fcB.readline().rstrip().split(",")],averageCostsBoth)
                    averageCostsStarred = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageCostsStarred)
                    averageAccuraciesStarred = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageAccuraciesStarred)
                    averageCostsBoth = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageCostsBoth)
                    averageAccuraciesBoth = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageAccuraciesBoth)
                    overallAverageCostStarred = reduce(lambda x,y: x+y, averageCostsStarred)/10.0
                    overallAverageAccuracyStarred = reduce(lambda x,y: x+y, averageAccuraciesStarred)/10.0
                    overallAverageCostBoth = reduce(lambda x,y: x+y, averageCostsBoth)/10.0
                    overallAverageAccuracyBoth = reduce(lambda x,y: x+y, averageAccuraciesBoth)/10.0

                    fSA.write("Averaged Costs:\n")
                    fSA.write(",".join([str(c) for c in averageCostsStarred]) + "\n")
                    fSA.write("Averaged Accuracies:\n")
                    fSA.write(",".join([str(c) for c in averageAccuraciesStarred]) + "\n")
                    fSA.write("Overall Average Accuracy:\n")
                    fSA.write("%f\n" % overallAverageAccuracyStarred)
                    fSA.write("Overall Average Cost:\n")
                    fSA.write("%f" % overallAverageCostStarred)


                    fBA.write("Averaged Costs:\n")
                    fBA.write(",".join([str(c) for c in averageCostsBoth]) + "\n")
                    fBA.write("Averaged Accuracies:\n")
                    fBA.write(",".join([str(c) for c in averageAccuraciesBoth]) + "\n")
                    fBA.write("Overall Average Accuracy:\n")
                    fBA.write("%f\n" % overallAverageAccuracyBoth)
                    fBA.write("Overall Average Cost:\n")
                    fBA.write("%f" % overallAverageCostBoth)

                    fSA.close()
                    fBA.close()
                    #fcS.close()
                    faS.close()
                    #fcB.close()
                    faB.close()


                fUA = open(RELATIVEPATH + "%s/%d/UnstarredAverages" % (name,wrongAnswerCost),'w')
                fcU = open(RELATIVEPATH + "%s/%d/Unstarred/costs" % (name,wrongAnswerCost),'r')
                faU = open(RELATIVEPATH + "%s/%d/Unstarred/accuracies" % (name,wrongAnswerCost),'r')

                averageCostsUnstarred = [0.0]*10
                averageAccuraciesUnstarred = [0.0]*10
                for lineNo in xrange(NUMBER_OF_REPETITIONS):
                    averageAccuraciesUnstarred = map(lambda x,y:x+y,[float(x) for x in faU.readline().rstrip().split(",")],averageAccuraciesUnstarred)
                    averageCostsUnstarred = map(lambda x,y:x+y,[float(x) for x in fcU.readline().rstrip().split(",")],averageCostsUnstarred)
                averageCostsUnstarred = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageCostsUnstarred)
                averageAccuraciesUnstarred = map(lambda x: (x/NUMBER_OF_REPETITIONS), averageAccuraciesUnstarred)
                overallAverageCostUnstarred = reduce(lambda x,y: x+y, averageCostsUnstarred)/10.0
                overallAverageAccuracyUnstarred = reduce(lambda x,y: x+y, averageAccuraciesUnstarred)/10.0

                fUA.write("Averaged Costs:\n")
                fUA.write(",".join([str(c) for c in averageCostsUnstarred]) + "\n")
                fUA.write("Averaged Accuracies:\n")
                fUA.write(",".join([str(c) for c in averageAccuraciesUnstarred]) + "\n")
                fUA.write("Overall Average Accuracy:\n")
                fUA.write("%f\n" % overallAverageAccuracyUnstarred)
                fUA.write("Overall Average Cost:\n")
                fUA.write("%f" % overallAverageCostUnstarred)

                fUA.close()
                fcU.close()
                faU.close()

            print "Finished pretty printing everything!"
        print "Next experiment (if any) will begin in 10 seconds."
        sleep(10)
        experimentNumber = int(f.readline())
    f.close()



def writeSimulationParameters():
    # List of tuples of Worker Distributions, where each Worker Distribution is a 3-tuple
    # A Worker Pool Distribution Pair would be
    # of the form
    # (WP0 distribution params, WP1 distribution params)
    # EG - ((100,1.0,0.2),(100,0.25,0.05))
    # RUN ON 1 AT A TIME TO MAINTAIN SANITY
    workerDistributionPairs = []
    #Read the parameters for these pairs
    f = open(RELATIVEPATH + 'WorkerDistributionPairs','r')
    for line in f:
        #Write the parameters of interest into this file!
        # WP1_NUM_WRKERS,WP1_MEAN,WP1_STD_DEV|WP2_NUM_WRKERS,WP2_MEAN,WP2_STD_DEV

        (WP0,WP1) = line.rstrip().split("|")

        WP0_num,WP0_mean,WP0_stddev = WP0.split(",")
        WP0_num = int(WP0_num)
        WP0_mean = float(WP0_mean)
        WP0_stddev = float(WP0_stddev)

        WP1_num,WP1_mean,WP1_stddev = WP1.split(",")
        WP1_num = int(WP1_num)
        WP1_mean = float(WP1_mean)
        WP1_stddev = float(WP1_stddev)

        workerDistributionPairs.append(((WP0_num,WP0_mean,WP0_stddev),(WP1_num,WP1_mean,WP1_stddev)))
    f.close()

    wrongAnswerCosts = []
    f = open(RELATIVEPATH + 'WrongAnswerCosts','r')
    # 1 cost per line, integer. NO EXTRA LINES AT THE END.
    # Eg- 100
    for line in f:
        wrongAnswerCosts.append(int(line.rstrip()))
    f.close()

    starredWorkerPoolCosts = []
    f = open(RELATIVEPATH + 'StarredWorkerPoolCosts','r')
    # 1 cost per line, float. NO EXTRA LINES AT THE END.
    # Eg- 1.2
    for line in f:
        starredWorkerPoolCosts.append(float(line.rstrip()))
    f.close()

    f = open(RELATIVEPATH + 'SimulationParameters','w')
    for i in xrange(len(workerDistributionPairs)):
        f.write("%d\n" % i)
        f.write("%d,%f,%f\n" % (workerDistributionPairs[i][0][0],workerDistributionPairs[i][0][1],workerDistributionPairs[i][0][2]))
        f.write("%d,%f,%f\n" % (workerDistributionPairs[i][1][0],workerDistributionPairs[i][1][1],workerDistributionPairs[i][1][2]))
        f.write("%d\n" % len(wrongAnswerCosts))
        for wrongAnswerCost in wrongAnswerCosts:
            f.write("%f\n" % wrongAnswerCost)
        f.write("%d\n" % len(starredWorkerPoolCosts))
        for starredWorkerPoolCost in starredWorkerPoolCosts:
            f.write("%f\n" % starredWorkerPoolCost)
    f.write("-1")
    f.close()

    print "Generated the SimulationParameters file."

run(MODE)