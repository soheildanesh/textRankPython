"""
From this paper: http://acl.ldc.upenn.edu/acl2004/emnlp/pdf/Mihalcea.pdf 

I used python with nltk, and pygraph to do an implmentation of of textrank.

for questions: http://twitter.com/voidfiles

"""
import nltk
import itertools
from operator import itemgetter

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.pagerank import pagerank
from pygraph.classes.exceptions import AdditionError

import glob

from os.path import expanduser
home = expanduser("~")

text = u"""In the Valley, we have lots of euphemisms for changing your business until you find a way to make money: You might throw things at the wall and see what sticks, or go where the money is, or pivot. Whatever you call it, it boils down to a basic animal instinct-the killer instinct. You need to look at the whole picture and attack an area that is vulnerable, and then keep attacking until you have won, or until you find an even more vulnerable spot. Rinse, then repeat.

I have yet to run my own company, but that doesn't stop me from evaluating the ability of a business to harness its killer instinct and fuel its own expansion. I have worked for companies with and without this instinct. I like working for companies with a keen killer instinct.

This killer instinct directly relates to last month's Google Reader debacle. I would often deride Google for changing Reader, but at the same time, I knew from the beginning that it was the right move on the part of Google.

Google has amassed their resources to support Google+. They have gone so far as to tie employees' salaries and bonuses to how well Google+ does. They then rolled out integrations across the company. The company uses anything that could possibly prop up Google+ to drive the success of the project. This is the killer instinct in action. Google knows that if they don't combat Facebook, they are going to forfeit a significant market in the future. They aren't going to lose this battle without a fight.

As an outsider, and as a former Yahoo employee, I applaud Google's determination. Yahoo had been trying to start a social networking service for as long as I worked there. The problem with the Yahoo social networking plan is that they have tried five5 different things in five5 years. Apparently Google+ wasn't all that welcome at Google in it's internal beta, and there have even been some very public rants from Googlers about the faults of Google+,the project- but Google is still pushing it hard. If Yahoo ran had run into this much resistance, they would have shut it down.

Now that I work for a small company, I have had the chance to see killer instinct in the flesh. I know how much focus it gives a company, and that it drives the development of a strong plan. It gives you a roadmap, even when you don't always know what the future looks like. I can only hope that when I run my own company, I'll have that same killer instinct."""



def list_files_in_foler(folderPath  = "/Users/soheildanesh/projects/cam/data/datasets/Hulth2003/Test/" , fileExtension = "*.abstr"):
    #from http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
    print glob.glob(folderPath+fileExtension)
    return glob.glob(folderPath+fileExtension)

    #folderPath = "/Users/soheildanesh/GitHub/cam"
    #f = []
    
    #from http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
    #for (dirpath, dirnames, filenames) in walk(folderPath):
     #   print("dirpath, dirnames, filenames = %s, %s, %s" %  (dirpath, dirnames, filenames)  ) 
     #   f.extend(filenames)
     #   break
    #return f

def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP']):
    return [item for item in tagged if item[1] in tags]


def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def textrankFilesInFolder(folderPath):
    files = list_files_in_foler(folderPath)
    for file in files:
        text = open(file)
        print(text)
        
#given a list of words (topWordList) and toneized text (textWordList)  (ie list of words in order as they appear in the original text), combine the words that occur adjacent to each other in the text into multi-word phrases, checks for inclusion in text before including candidates in the returned ones to avoid those candidates saparated by punctuation marks.        
def combineAdjacentWords(topWordList, textWordList, text):
    
    phraseOrWord = ""
    ouputPhrasesAndWords = [] 
    for word in textWordList:
        #word = wordWeight[0]
        word = word.lower()
        print("word = %s" % (word))
        if word in topWordList:
            print("word in topWordList = %s" % (word))
            if not phraseOrWord: #if phraseOrWord is not nil
                phraseOrWord = word
            else:
                phraseOrWord = phraseOrWord + " " + word
                #strip phraseOrWord: looks like python already strips, not seeing any leading/trailing spaces
        else:
            #print("phraseOrWord geting added to outputPhrasesAndWords %s" % (phraseOrWord))
            if phraseOrWord and phraseOrWord not in ouputPhrasesAndWords and phraseOrWord in text:
                #if wordOrPhrase is not already in outputPhrasesAndWords list
                ouputPhrasesAndWords.append(phraseOrWord)
                print("ouputPhrasesAndWords = %s" % (ouputPhrasesAndWords))
            phraseOrWord = ""
                
    return ouputPhrasesAndWords

def runtextrankOnFilesInFoler(folderPath  = "/Users/soheildanesh/projects/cam/data/datasets/Hulth2003/Test/" , fileExtension = "*.abstr"):
    textFiles = list_files_in_foler(folderPath, fileExtension)
    for fileName in textFiles:
        print("filefile = %s" % fileName) #<< now read each file and call textrank(text) then take the result and put it in a file like  url : keyphrase, keyphrase, ... then load this to semeval and measure precision recall, with textrank style
        file = open(fileName, 'r')
        text = file.read()
        print("text = %s" % text)

def runtextrank(text):
    textWordList = nltk.word_tokenize(text)

    tagged = nltk.pos_tag(textWordList)
    tagged = filter_for_tags(tagged)
    tagged = normalize(tagged)

    unique_word_set = unique_everseen([x[0] for x in tagged])

    gr = digraph()
    gr.add_nodes(list(unique_word_set))

    window_start = 0
    window_end = 2

    while 1:
        window_words = tagged[window_start:window_end]
        if len(window_words) == 2:
            print window_words
            try:
                gr.add_edge((window_words[0][0], window_words[1][0]))
            except AdditionError, e:
                print 'already added %s, %s' % ((window_words[0][0], window_words[1][0]))
        else:
            break

        window_start += 1
        window_end += 1

    calculated_page_rank = pagerank(gr)
    di = sorted(calculated_page_rank.iteritems(), key=itemgetter(1), reverse=True)
    
    ### TAKE TOP 3rd WORDS AND COMBINE THEM ###
    thirdOfVertices = len(di) / 3
    topWrodWeights = di[:thirdOfVertices]
    topWords = []
    for wordWeight in topWrodWeights:
        topWords.append(wordWeight[0])
    
    phrasesAndWords = combineAdjacentWords(topWords, textWordList, text)
    print("phrasesAndWords = %s" % phrasesAndWords)
    ### TAKE TOP 3rd WORDS AND COMBINE THEM ###    


    print 'di = %s' % (di)
    for k, g in itertools.groupby(di, key=itemgetter(1)):
        print k, map(itemgetter(0), g)

    return di