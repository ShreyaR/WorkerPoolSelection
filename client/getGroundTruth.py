
def getQuestions(fileName):
    QuestionTopics = {}
    Questions = {}
    QuestionChoices = {}
    LinksForChoice0 = {}
    LinksForChoice1 = {}
    GroundTruths = {}
    QuestionDifficulty = {}

    questionFile = open(fileName,'r')
    #Every 5 lines correspond to a question
    Counter = 0
    for line in questionFile:
        QuestionNumber = Counter/5
        if (Counter%5 == 1):
            #line corresponds to question
            splitLine = line.rstrip().split("\t")
            startIndexForTopic = int(splitLine[0])
            endIndexForTopic = int(splitLine[1])
            question = splitLine[2]
            choice0 = splitLine[3]
            choice1 = splitLine[4]

            QuestionTopics[QuestionNumber] = question[startIndexForTopic:endIndexForTopic]
            Questions[QuestionNumber] = question
            QuestionChoices[QuestionNumber] = (choice0,choice1)

        elif (Counter%5 == 2):
            #line corresponds to links for choice 0
            LinksForChoice0[QuestionNumber] = tuple(line.rstrip().strip(","))

        elif (Counter%5 == 3):
            #line corresponds to links for choice 1
            LinksForChoice1[QuestionNumber] = tuple(line.rstrip().strip(","))

        elif (Counter%5 == 4):
            #line corresponds to ground truth
            GroundTruths[QuestionNumber] = int(line.rstrip())
        elif (Counter%5 == 0):
            #line corresponds to question difficulty (E,M,H)
            QuestionDifficulty[QuestionNumber] = line.rstrip()
        Counter += 1

    print "Questions have been loaded."
    questionFile.close()
    return QuestionTopics, Questions, QuestionChoices, LinksForChoice0, LinksForChoice1, GroundTruths, QuestionDifficulty

for element in getQuestions("questionsEMD")[5].items():
    print element[0],element[1]