import os.path
import json
import sys
from copy import deepcopy


class TrainingTokens(object):
    def __init__(self):
        self.words=dict()                    # words("word",{tag,count})    10K * 30 = 300K <word,tag> ?
        self.tags=dict()                     # tags ("tag",{tag,count})     30*30 = 900     <TAG,tagg> ?  <word-tag>, value  Try tuples ()
        self.tagcounts=dict()
        self.wordProbabilities=dict()
        self.uniquetags=[]

class Item(object):
    def __init__(self):
        self.word=dict()
        self.count=0
        self.wordTagProbabilitie=dict()


# global variables
trainingData = TrainingTokens()

# Check if file exists 
def isFileExists(filename):
    if len(filename)!=0:
        file = os.path.isfile(filename)

        if file==None:
            return None
        else:
            return open(filename,"r",encoding="utf8");
    else:
        return None


# adding words to Trainingdata
def addWord(word,tag):
    try:

        global trainingData

        if word in trainingData.words:
            wordtag = trainingData.words[word]

            if tag in wordtag.word:
                wordtag.word[tag] = int(wordtag.word[tag])+1
            else:
                wordtag.word[tag]=1

            wordtag.count=wordtag.count+1
            trainingData.words[word]=wordtag
        else:
            wordtag = Item()
            wordtag.word[tag]=1
            wordtag.count=1
            trainingData.words[word]=wordtag

    except Exception as e:
        print(e)
        print (word+"::"+tag)


# adding tags to Tainingdata
def addTag(currentTag,previousTag):
    try:
        global trainingData

        if previousTag in trainingData.tags:

            tagtag = trainingData.tags[previousTag]

            if currentTag in tagtag.word:
                tagtag.word[currentTag]=int(tagtag.word[currentTag])+1
            else:
                tagtag.word[currentTag]=1

            tagtag.count +=1
            trainingData.tags[previousTag]=tagtag

        else:
            tagtag = Item()
            tagtag.word[currentTag] = 1
            tagtag.count +=1
            trainingData.tags[previousTag]=tagtag
            #trainingData.tags[previousTag]={currentTag:1}

        # updating tag count
        if currentTag in trainingData.tagcounts:
            trainingData.tagcounts[currentTag]=int(trainingData.tagcounts[currentTag])+1
        else:
            trainingData.tagcounts[currentTag]=1

        # udate uniquetag
        if previousTag not in trainingData.uniquetags:
            trainingData.uniquetags.append(previousTag)


    except Exception as e:
        print (e)


# calculating probability of a word given tag
def calculateProbabilities():
    try:
        global trainingData

        # words probability
        for word in trainingData.words:
            if word in {"time", "flies","like","an","arrow"}:
                x=10

            tags = trainingData.tags

            if len(tags)>0:
                for tag in tags:

                    if tag in trainingData.words[word].word:
                        wordTagCount = trainingData.words[word].word[tag]

                        if wordTagCount == 0:
                            xxxx
                    
                        tagcount = trainingData.tagcounts[tag]

                        if tagcount == 0:
                            xxxx
                        trainingData.words[word].wordTagProbabilitie[tag]=wordTagCount/tagcount;

                
            '''
            obj = trainingData.words[word]
            wordcount = obj.count

            for tag in obj.word:
                obj.wordTagProbabilitie[tag] = (obj.word[tag]/wordcount)
                
            trainingData.words[word]=obj

            '''

        # tag tag probability
        for tag in trainingData.tags:
            obj = trainingData.tags[tag]
            tagcount = obj.count

            for tagtag in obj.word:
                obj.wordTagProbabilitie[tagtag] = (obj.word[tagtag]/tagcount)

            trainingData.tags[tag]=obj


    except Exception as e:
        print (e)


# Reading Training data
def readingTrainingData(filepath):
    file = isFileExists(filepath)

    if file!=None:
        with file as f:
            content = f.readlines()

            if len(content)>0:
                for line in content:
                    previousTag="START"
                    if len(line)>0:
                        tokens = line.strip().split(" ")

                        for t in tokens:
                            word = t.split("/",1)[0]
                            #tag = t.split("/",1)[1]
                            tag = t.split("/",t.count('/'))[len(t.split("/",t.count('/')))-1]

                            addWord(word+"",tag)
                            addTag(tag,previousTag)
                            previousTag=tag

    else:
        return None


# writing model to file
def writingModelToFile():

    global trainingData

    _json = json.dumps(trainingData, default=lambda o: o.__dict__)

    if len(_json)>0:
            file = open("hmmmodel.txt","w")
            file.write(_json)
            file.close()



if len(sys.argv)==2:
    filname = sys.argv[1]
    print(sys.argv[1])
    readingTrainingData(filname)
else:
    readingTrainingData("tdata.txt")
    #readingTrainingData("catalan_corpus_dev_tagged.txt")

calculateProbabilities()

writingModelToFile()
