import pickle

class Data:

    def __init__(self, numberOfProblems, statuses, answers, costs,
                 HITIds, usedWorkers, actions, agentActions, beliefs, ballots):
        self.numberOfProblems = numberOfProblems
        self.statuses = statuses
        self.answers = answers
        self.costs = costs
        self.HITIds = HITIds
        self.usedWorkers = usedWorkers
        self.actions = actions
        self.agentActions = agentActions
        self.beliefs = beliefs
        self.ballots = ballots

def serialize(numberOfProblems, statuses, answers, costs, HITIds, usedWorkers,
              actions, agentActions, beliefs, ballots):
    tempfile = open("experiment.dump", 'w')
    data = Data(numberOfProblems, statuses, answers, costs, HITIds, usedWorkers,
                actions, agentActions, beliefs, ballots)
    pickler = pickle.Pickler(tempfile)
    pickler.dump(data)
    tempfile.close()

def unSerialize():
    tempfile = open("experiment.dump", 'r')
    unpickler = pickle.Unpickler(tempfile)
    data = unpickler.load()
    tempfile.close()
    return (data.numberOfProblems, data.statuses, data.answers, data.costs,
            data.HITIds, data.usedWorkers, data.actions, data.agentActions,
            data.beliefs, data.ballots)
