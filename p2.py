# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:47:14 2015

@author: end
"""
import csv
import sys
import pickle
import re
import scipy.stats
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


lcf = open("lancater.txt", "w")
psf = open("porter.txt", "wb")

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
    
    #Return frequency of path words per user posting
    pathWordsNum = frequentNum(cleanSentence,"p", words)
    #Return freqeuncy of graphics html tags per user posting
    graphicsNum = frequentNum(sentence, "g")
    #Return Frequency of emotican peruser postings
    emoticanNum = frequentNum(cleanSentence, "e")

    
    stemStopWordLanc = wordStemmer(words, 'lancaster')
    stemPathLanc = wordStemmer(cleanSentence, 'lancaster')
    pathWordsNumLanc = frequentNum(stemPathLanc, "p", stemStopWordLanc)
    
    stemStopWordPort = wordStemmer(words, 'porter')
    stemPathPort = wordStemmer(cleanSentence, 'porter')
    pathWordsNumPort = frequentNum(stemPathPort, "p", stemStopWordPort)
    
    
    lcf.close()
    psf.close()
    
    print(len(pathWordsNum)," ",len(graphicsNum)," ",len(emoticanNum))
    print("none")
    print(scipy.stats.pearsonr(pathWordsNum,graphicsNum))
    print(scipy.stats.pearsonr(pathWordsNum,emoticanNum))
    print("lanc")
    print(scipy.stats.pearsonr(pathWordsNumLanc,graphicsNum))
    print(scipy.stats.pearsonr(pathWordsNumLanc,emoticanNum))
    print("port")
    print(scipy.stats.pearsonr(pathWordsNumPort,graphicsNum))
    print(scipy.stats.pearsonr(pathWordsNumPort,emoticanNum))
  
    

    
def fileOpen(filename, param = 'r'):
    try:
        fh = open(filename, param)
        return fh 
    except:
        print("Unable to open file")
        sys.exit()

#open cvs file and and return content
def csvReader(filename, delim = ","):
    try:
        with open(filename, 'rU') as csvfile:
           reader = csv.reader(csvfile, delimiter=delim)
           return list(reader)
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
    userPost = userPost.split("\n")
    return sum([1 for word in pathWords for sentence in userPost if word in sentence])
    

#Remove stop words from list
def stopWordsRemover(listItem, stopwords):
    return [item for item in listItem if item not in stopwords]    
 
def getGraphics(listItem):
    soup = BeautifulSoup(str(listItem))
    #espression = re.compile()
    count = 0
    return sum([(count + 1) for word in soup.find_all()])
    
def getImotacan(listItem):
    #print(len(listItem))
    #soup = BeautifulSoup(str(listItem))
    #print(len(soup.getText()))
    pattern = re.compile(r"([:=]\s*[-っ^oc']?\s*[-j#x$\\ls./bþp*0o@|<c\{\}>3d()\]\[]\s*[|)]?|[8x]\s*[-]?\s*[}d]|[>]\s*[:]\s*[/[()p\\/]|[d]\s*[:]?\s*[']?\s*[<:;=']\s*[:]?|\sx\s*[-]?\s*[p]\s|[0o]\s*[:;]\s*[-]?\s*[)3]|[}3]\s*[:]\s-?[)]|\^<_<|>_>\^|\|[;]?-[o)]|#-\)|%-?\)|:?-?###..|<\s*:\s*-\s*[|]|ಠ\s*_s\*ಠ|<\s*\*\s*\)\s*\)\s*\)\s*-\s*{|>\s*<\s*\(\s*\(\s*\(\s*\*\s*>|><>|\\o/|\*\\0/\*|@}-;-'---|@>-->--|~\(_8^\(I\)|[5~]:-[)\\]|//0-0\\\\\]|\*<\|:-\)|,:-\)|7:^\]|<//*3|\.\.\.)", re.I)
     #wordSplit = " ".join(listItem)
    #wordSplit = wordSplit.replace(" ","")
    wordSplit = re.split(pattern, listItem)
    #print(l)
    pickle.dump(wordSplit, psf)
    
    return sum([1 for emot in wordSplit if re.match(pattern, emot)])
    
def frequentNum(listItem, freqType, word = " "):

    if freqType == "p":
        return [wordFrequency(word, sentence) for sentence in listItem]
    elif freqType == "g":
        return [getGraphics(sentence) for sentence in listItem]
    elif freqType == "e":
        return [getImotacan(sentence) for sentence in listItem]
    
    #print(wordSplit)
    return sum([1 for emot in l if re.match(pattern, emot)])
if __name__ == '__main__':
    main()