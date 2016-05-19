from boto.mturk.connection import MTurkConnection
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import Qualifications
from boto.mturk.qualification import PercentAssignmentsApprovedRequirement
from boto.mturk.qualification import Requirement
from boto.mturk.price import Price
from MT import MT

#################################
#################################
#Modifications to do in this file:
# Constructor: Change the qualification requirements by shifting this component
# to the createHIT function.
#
#
#
#################################
#################################


class RealMT(MT):
    def __init__(self, numberOfProblems, AWSAKID, AWSSAK, sandbox=True):
        self.mturk = MTurkConnection(AWSAKID, AWSSAK,
                                     host='mechanicalturk.sandbox.amazonaws.com')
        if not sandbox:
            self.mturk = MTurkConnection(AWSAKID,
                                         AWSSAK,
                                         host='mechanicalturk.amazonaws.com')

        self.quals = []
        self.numberOfProblem = numberOfProblems
        self.isSandbox = sandbox

        ######Relocate the logic of this code to the time of creation of the HIT
        #for i in range(0, numberOfProblems):
        #    qual = Qualifications()
        #    qual.add(PercentAssignmentsApprovedRequirement('GreaterThan',95))
        #    self.quals.append(qual)
        ######


    def createHIT(self, workflow, URL, title, rwd, duration, lifetime,
                  max_assignments, problemNumber):
        #workflow = 0, normal pool
        #workflow = 1, master pool
        qual = Qualifications()
        if (self.isSandbox):
            SandboxMastersQualID = '2ARFPLSP75KLA8M8DH1HTEQVJT3SY6'
            qual.add(Requirement(SandboxMastersQualID,'DoesNotExist'))
            if (workflow == 1):
                qual.add(Requirement(SandboxMastersQualID,'Exists'))
        else:
            MastersQualID = '2F1QJWKUDD8XADTFD2Q0G6UTO95ALH'
            qual.add(Requirement(MastersQualID,'DoesNotExist'))
            if (workflow == 1):
                qual.add(Requirement(MastersQualID,'Exists'))


        hits = self.mturk.create_hit(question = ExternalQuestion(URL, 800),
                                     title = title,
                                     reward = Price(rwd),
                                     duration = duration,
                                     lifetime = lifetime,
                                     max_assignments = max_assignments,
                                     qualifications=self.quals[problemNumber])
        for hit in hits: #There should only be one
            return hit.HITId

    def getHIT(self, HITId):
        return self.mturk.get_hit(HITId)
    
    def getAssignments(self, HITId, page_size, page_number):
        return self.mturk.get_assignments(HITId, 
                                          page_size=page_size,
                                          page_number=page_number)
    
    def getObservation(self, assignment):
        observation = assignment.answers[0][0].fields[0]
        observation = observation.encode("ascii")
        return observation

    def getProblemNumber(self, assignment):
        problemNumber = assignment.answers[0][1].fields[0]
        problemNumber = int(problemNumber.encode("ascii"))
        return problemNumber

    def getWorker(self, assignment):
        return assignment.WorkerId

    def approveAssignment(self, assignment):
        self.mturk.approve_assignment(assignment.AssignmentId)

    def disposeHIT(self,HITId):
        self.mturk.dispose_hit(HITId)