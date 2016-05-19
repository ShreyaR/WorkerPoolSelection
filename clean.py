from os.path import exists
from os import mkdir, rmdir, remove, chmod
from shutil import rmtree
from boto.mturk.connection import MTurkConnection
##############################
#Configuration
##############################
#AWS Access Key ID
AWSAKID = '<YOURAWSACCESSKEYIDHERE>'

#AWS Secret Access Key
AWSSAK = '<YOURAWSSECRETACCESSKEYHERE>'

#Simulation?
SIMULATION = True

#Sandbox
SANDBOX = True

NUMBEROFWORKERPOOLS = 2
###############################
#End Configuration
###############################

if exists('log'):
    rmtree('log')
if exists('locks'):
    rmtree('locks')
mkdir('log')
mkdir('log/results')
mkdir('log/em')
mkdir('log/pomdp')
mkdir('locks')
chmod('log', 0o777)
chmod('locks', 0o777)

for i in xrange(NUMBEROFWORKERPOOLS):
    f = open('log/aql' + str(i),'w')
    f.write('')
    f.close()
    chmod('log/aql' +str(i),0o777)


# f = open('log/aql0', 'w')
# f.write('')
# f.close()
# chmod('log/aql0', 0o777)
#
# f = open('log/aql1', 'w')
# f.write('')
# f.close()
# chmod('log/aql1', 0o777)


if not SIMULATION:
    if SANDBOX:
        mturk = MTurkConnection(AWSAKID,
                                AWSSAK,
                                host='mechanicalturk.sandbox.amazonaws.com')
    else:
        mturk = MTurkConnection(AWSAKID,
                                AWSSAK,
                                host='mechanicalturk.amazonaws.com')

    for hit in mturk.get_all_hits():
        mturk.disable_hit(hit.HITId)
