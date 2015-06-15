# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:47:14 2015

@author: end
"""
import csv
import sys
import re
import scipy.stats
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import Counter




def main():
    #file paths
    pathFile = "data/path-words.csv"
    postFile = "data/posts.tsv"

    

    
    #Open file and return content
    wordList = csvReader(pathFile)
    sentenceList = csvReader(postFile,'\t')
    
    #Get specific column
    words = getColumn(wordList, 0)
    words = singleWords(wordList, 0)
    #Remove Duplicates from word path
    words = list(set(words))
    
     #Remove stop words from list of
    stop_words = stopwords.words("english")
    words = stopWordsRemover(words, stop_words)
    
    #Get post from the different users
    sentence = getColumn(sentenceList, 2)
    sentence = stopWordsRemover(sentence, stop_words)
    #sentence = cleanText(sentence)
    
    #Remove Html tags
    cleanSentence = cleanText(sentence)
    
    
    #no stemming
    #Return frequency of path words per user posting
    pathWordsNum = frequentNum(cleanSentence,"p", words)
    #Return freqeuncy of graphics html tags per user posting
    graphicsNum = frequentNum(sentence, "g")
    #Return Frequency of emotican peruser postings
    emoticanNum = frequentNum(cleanSentence, "e")
    #Return Frequency of ellipses
    ellipsesNum = frequentNum(cleanSentence, "l")

    
    #stem word list using lancaster
    stemWordLanc = wordStemmer(words, 'lancaster')
    #Remove Duplicates from word path
    stemWordLanc = list(set(stemWordLanc))
    #Stem user posting
    stemPathLanc = wordStemmer(cleanSentence, 'lancaster')
    #Get list of frequent postings
    pathWordsNumLanc = frequentNum(stemPathLanc, "p", stemWordLanc)
    

    #stem word list using porter
    stemWordPort = wordStemmer(words, 'porter')
    #print(stemWordPort)
    #Remove Duplicates from word path
    stemWordPort = list(set(stemWordPort))
    #stem user posteing using porter
    stemPathPort = wordStemmer(cleanSentence, 'porter')
    #Get list of frequent postings
    pathWordsNumPort = frequentNum(stemPathPort, "p", stemWordPort)
    
    #Result output file
    outputFile = "data/result.csv"
        #Output file write to result.csv
    resultFile = fileOpen(outputFile, "w")
    
    #header information
    writeFile("tag correlation", "stemming tequeniques", "correlation value", "p value", filename = resultFile)
    print(len(pathWordsNum)," ",len(graphicsNum)," ",len(emoticanNum))
    print("none")
    
    #1st data value
    stats = scipy.stats.pearsonr(pathWordsNum,graphicsNum)
    writeFile("tags", "none", stats[0], stats[1], filename = resultFile)
    
    #2nd data value    
    stats = scipy.stats.pearsonr(pathWordsNum,emoticanNum)
    writeFile("emoticons", "none", stats[0], stats[1], filename = resultFile)
    
    #3nd data value    
    stats = scipy.stats.pearsonr(pathWordsNum,ellipsesNum)
    writeFile("ellipses", "none", stats[0], stats[1], filename = resultFile)
    
    
    #4th data value lancaster   
    stats = scipy.stats.pearsonr(pathWordsNumLanc,graphicsNum)
    writeFile("tags", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #5th data value lancaster   
    stats = scipy.stats.pearsonr(pathWordsNumLanc,emoticanNum)
    writeFile("emoticons", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #6th data value lancaster   
    stats = scipy.stats.pearsonr(pathWordsNumLanc,ellipsesNum)
    writeFile("ellipses", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #7th data value Porter   
    stats = scipy.stats.pearsonr(pathWordsNumPort,graphicsNum)
    writeFile("tags", "Porter", stats[0], stats[1], filename = resultFile)
    
    #8th data value Porter   
    stats = scipy.stats.pearsonr(pathWordsNumPort,emoticanNum)
    writeFile("emoticans", "Porter", stats[0], stats[1], filename = resultFile)
    
    #9th data value Porter   
    stats = scipy.stats.pearsonr(pathWordsNumPort,ellipsesNum)
    writeFile("ellipses", "Porter", stats[0], stats[1], filename = resultFile)
    
    
    resultFile.close()
  
    

    
def fileOpen(filename, param = 'r'):
    try:
        fh = open(filename, param, encoding='utf8')
        return fh 
        
    except:
        print("Unable to open file")
        sys.exit()

#open cvs file and and return content
def csvReader(filename, delim = ","):
    try:
        with open(filename, 'rU') as csvfile:
           reader = csv.reader(csvfile, delimiter=delim)
           t = list(reader)
           print(t.pop(0))
           print(len(t))
           return t
    except:
        print("Unable to open file")
        sys.exit()

#Takes a list and returns values in calumn specify
def getColumn(listItem, columnNum):
    return [item[columnNum].lower() for item in listItem]

#Takes a list and returns values in calumn specify
def singleWords(listItem, columnNum):
    return [item[columnNum] for item in listItem if len(str(item[columnNum]).split()) == 1]

#Clean text
def cleanText(listItem):
    return [BeautifulSoup(sentence).get_text() for sentence in listItem]
    
#Applied word stemmer to list. Returns a list
def wordStemmer(listItem, stemType):
    if(stemType == 'porter'):
        ps = PorterStemmer()
        return [ps.stem(item) for item in listItem]
    elif(stemType == 'lancaster'):
        ps = LancasterStemmer()
        return [ps.stem(item) for item in listItem]
        

#Count how often the word appears and returns a dictionary   
def wordFrequency(pathWords, userPost):
    userPost = word_tokenize(userPost)
    userPost = Counter(userPost)
    
    return sum([userPost[word] for word in pathWords if userPost[word]])

    

#Remove stop words from list
def stopWordsRemover(listItem, stopwords):
    return [item for item in listItem if item not in stopwords]    
 
def getGraphics(listItem):
    soup = BeautifulSoup(str(listItem))
    return sum([1 for word in soup.find_all()])
    
def getImotacan(listItem):
    pattern = re.compile(r"([:=]\s*[-っ^oc']?\s*[-j#x$\\ls./bþp*0o@|<c\{\}>3d()\]\[]\s*[|)]?|[8x]\s*[-]?\s*[}d]|[>]\s*[:]\s*[/[()p\\/]|[d]\s*[:]?\s*[']?\s*[<:;=']\s*[:]?|\sx\s*[-]?\s*[p]\s|[0o]\s*[:;]\s*[-]?\s*[)3]|[}3]\s*[:]\s-?[)]|\^<_<|>_>\^|\|[;]?-[o)]|#-\)|%-?\)|:?-?###..|<\s*:\s*-\s*[|]|ಠ\s*_s\*ಠ|<\s*\*\s*\)\s*\)\s*\)\s*-\s*{|>\s*<\s*\(\s*\(\s*\(\s*\*\s*>|><>|\\o/|\*\\0/\*|@}-;-'---|@>-->--|~\(_8^\(I\)|[5~]:-[)\\]|//0-0\\\\\]|\*<\|:-\)|,:-\)|7:^\]|<//*3)", re.I)
    wordSplit = re.split(pattern, listItem)
    
    
    return sum([1 for emot in wordSplit if re.match(pattern, emot)])

def getEllipses(listItem):
    pattern = re.compile(r"\.\.+")
    
    wordPuctTokenize = WordPunctTokenizer()
    words = wordPuctTokenize.tokenize(listItem)
    
    return sum([1 for word in words if re.match(pattern, word)])
    
    
    
    
def frequentNum(listItem, freqType, word = " "):

    if freqType == "p":
        return [wordFrequency(word, sentence) for sentence in listItem]
    elif freqType == "g":
        return [getGraphics(sentence) for sentence in listItem]
    elif freqType == "e":
        return [getImotacan(sentence) for sentence in listItem]
    elif freqType == "l":
        return [getEllipses(sentence) for sentence in listItem]
        
def writeFile(*content, filename):
        outf = csv.writer(filename, delimiter = ',')
        outf.writerow(content)
    
    
    
if __name__ == '__main__':
    main()