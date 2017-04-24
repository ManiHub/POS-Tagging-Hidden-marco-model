import os.path
import json
import sys
import operator

class TrainingTokens(object):
    def __init__(self):
        self.words=dict()                    # words("word",{tag,count})    10K * 30 = 300K <word,tag> ?
        self.tags=dict()                     # tags ("tag",{tag,count})     30*30 = 900     <TAG,tagg> ?  <word-tag>, value  Try tuples ()
        self.tagcounts=dict()
        self.wordProbabilities=dict()

class Item(object):
    def __init__(self):
        self.word=dict()
        self.count=0
        self.wordTagProbabilitie=dict()

class HMM(object):
    def __init__(self):
        self.preiousStates=dict()
        self.nextStates=dict()
        self.paths=[]
        self.pathCount=0

class Paths(object):
    def __init__(self, **kwargs):
        self.pathId=0
        self.path=dict()

class Node(object):
    def __init__(self, **kwargs):
        self.value=None
        self.prob=0


# global variables
trainingData = TrainingTokens()
previousStates = dict()
nextStates=dict()
hmm=HMM()


def readingModelfile():
    try:
        file = open("hmmmodel.txt","r")
        _json = file.readlines()

        if len(_json)>0:
            global trainingData
            trainingData = TrainingTokens()
            trainingData = json.loads(_json[0],TrainingTokens)
            
    except Exception as e:
        print (e)

def getNextStates(currentTag):
    if len(currentTag)>0:
        global trainingData
        return trainingData["tags"][currentTag]["wordTagProbabilitie"]

# get Emission probability of a given tag wrt to the token 
def getEMissionProbability(tag,token):
    if len(tag) > 0 and len(token)>0:
        try:
            global trainingData

            if token in trainingData["words"]:
                tags = trainingData["words"]

                if token in tags:
                    temp = tags[token]["wordTagProbabilitie"]

                    if tag in temp:
                        return tags[token]["wordTagProbabilitie"][tag]
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            print(e)
            return 0

def getTransitionProbability(previousTag,currentTag):
    try:
        if len(previousTag) > 0 and len(currentTag)>0:
            global trainingData

            i=10

            if previousTag in trainingData["tags"]:
                tags = trainingData["tags"][previousTag]

                if currentTag in tags["word"]:
                    return tags["wordTagProbabilitie"][currentTag]
                else:
                    return 0
            else:
                return 0

    except Exception as e:
        print("Error in getTransitionProbability : ",e)
        return 0

def getPreviousProbability(tag):
    try:
        global hmm
        previousStates = hmm.preiousStates
        max = 0

        if len(previousStates) == 0:
            return 1

        if tag in previousStates:
            for t in previousStates[tag]:
                if max < previousStates[tag][t]:
                    max = previousStates[tag][t]
        return max       
    except Exception as e:
        print("Error in getPreviousProbability : ",e)


def calculateBackPointers():
    try:
        global hmm

        if len(hmm.preiousStates)>0:

            if hmm.pathCount==0:
                for state in hmm.preiousStates:

                    if len(hmm.preiousStates[state])>0:
                        d = hmm.preiousStates[state]
                        fromstate = max(d,key=d.get)
                        node=Node()
                        node.value=fromstate
                        node.prob=hmm.preiousStates[state][fromstate]

                        if hmm.pathCount==0:
                            path=Paths()
                            hmm.pathCount+=1
                            path.path[hmm.pathCount]=node
                            hmm.paths.append(path)
                        else:
                            paths = hmm.paths               # hmm.paths[0].path[1].value

                            for i in range(0,len(paths)):
                                nodes = hmm.paths[i].path[len(hmm.paths[i].path)].value

                                


            for state in hmm.preiousStates:
                state = hmm.preiousStates[state]
                x = max(state, key=state.get)
                




    except Exception as e:
        print ("Error in calculateBackPointers : ",e)

def Stage(token):
    try:
        i =10
        _Pstates=dict()
        if len(hmm.preiousStates)==0:
            prevstates = {"START"}
        else:
            prevstates = hmm.preiousStates

        for pstate in prevstates:
            nextstates = getNextStates(pstate)

            for nstate in nextstates:
                ep = getEMissionProbability(nstate,token)
                if ep>0:
                    tp=getTransitionProbability(pstate,nstate)

                    if tp>0:
                        pp=getPreviousProbability(pstate)

                        prob = pp*tp*ep

                        if prob>0:
                            
                            if nstate in _Pstates:
                                temp = _Pstates[nstate]
                                temp[pstate]=prob
                            else:
                                temp = dict()
                                temp[pstate]=prob

                            _Pstates[nstate]=temp
        hmm.preiousStates.clear()
        hmm.preiousStates=_Pstates
        calculateBackPointers()

                    

        x=10
                        


    except Exception as e:
        print("Error in Stage : ",e)

def constructModel(line):
    try:
        if line != None:
            tokens = line.strip().split(" ")
            for token in tokens:
               #currentTags = buildStageX(token,)   
               Stage(token)
               x=10          

    except Exception as e:
        print(e)



if len(sys.argv) == 2:
    testfilename = sys.argv[1]

readingModelfile()

testphrase="time flies like an arrow"
constructModel(testphrase)