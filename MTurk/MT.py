class MT:
    def __init__(self):
        pass
    def createHIT(self, question, title, reward, duration,
                  max_assignments, qualifications):
        pass
    def getHIT(self, HITId):
        pass
    def getAssignments(self, HITId, page_size, page_number):
        pass
    def getObservation(self, assignment):
        pass
    def getWorker(self, assignment):
        pass
    def approveAssignment(self, assignemntId):
        pass
    def disposeHIT(self, HITId):
        pass
    def cleanUp(self):
        pass
    def blockWorker(self, problemNumber, workerId):
        pass
