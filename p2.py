# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:47:14 2015
Created on Tue Jun  2 19:33:23 2015
File name: p2.py
Author: Yussel Rosario, Muath Alqurashi

Description: This program takes a set of data from two files related to the Self-Harm Study 
Project. Those files are Path-words.csv, and post.tsv. The file Path-Words.csv contains three
columns (word, Weight, and Modularity Class) but for the purpose of this project only the 
content of the word file will be extracted. More precisely only the words that have a length 
of one word. From the 2nd file (post.tsv), the data from the body column will be extracted. 
All other columns such as user, and posted will be disregarded. The purpose of this project 
is to find a correlation between the frequencies of Patheligical words, html graphics tags, 
emoticons, and ellipses using different stemming techniques as Porter Stemming, Lancasting 
Stemming, and no stemming.

@author: end
"""
import csv
import sys
import re
import scipy.stats
import os
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import WordPunctTokenizer
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
    #Remove Duplicates from word path
    stemWordPort = list(set(stemWordPort))
    #stem user posteing using porter
    stemPathPort = wordStemmer(cleanSentence, 'porter')
    #Get list of frequent postings
    pathWordsNumPort = frequentNum(stemPathPort, "p", stemWordPort)
    
    #Result output file
    outputFile = "data/result/result.csv"
        #Output file write to result.csv
    resultFile = fileOpen(outputFile, "w")
    
    #header information
    writeFile("tag correlation", "stemming techniques", "correlation value", "p value", filename = resultFile)
    

    
    #Data Normalization
    commonDivisorNone = sum(pathWordsNum) + sum(graphicsNum) + sum(emoticanNum) + sum(ellipsesNum)
    commonDivisorLanc = commonDivisorNone - sum(pathWordsNum) + sum(pathWordsNumLanc)
    commonDivisorPort = commonDivisorNone - sum(pathWordsNum) + sum(pathWordsNumPort)
    
    #1st data value
    pathWordsNum = normalize(pathWordsNum,commonDivisorNone)
    stats = scipy.stats.pearsonr(pathWordsNum,normalize(graphicsNum,commonDivisorNone))
    writeFile("tags", "none", stats[0], stats[1], filename = resultFile)
    
    #2nd data value    
    stats = scipy.stats.pearsonr(pathWordsNum,normalize(emoticanNum,commonDivisorNone))
    writeFile("emoticons", "none", stats[0], stats[1], filename = resultFile)
    
    #3nd data value   
    stats = scipy.stats.pearsonr(pathWordsNum,normalize(ellipsesNum,commonDivisorNone))
    writeFile("ellipses", "none", stats[0], stats[1], filename = resultFile)
        
    
    #4th data value lancaster 
    pathWordsNumLanc = normalize(pathWordsNumLanc,commonDivisorLanc)      
    stats = scipy.stats.pearsonr(pathWordsNumLanc,normalize(graphicsNum,commonDivisorLanc))
    writeFile("tags", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #5th data value lancaster
    stats = scipy.stats.pearsonr(pathWordsNumLanc,normalize(emoticanNum,commonDivisorLanc))
    writeFile("emoticons", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #6th data value lancaster   
    stats = scipy.stats.pearsonr(pathWordsNumLanc,normalize(ellipsesNum,commonDivisorLanc))
    writeFile("ellipses", "Lancaster", stats[0], stats[1], filename = resultFile)
    
    #7th data value Porter 
    pathWordsNumPort = normalize(pathWordsNumPort,commonDivisorPort) 
    stats = scipy.stats.pearsonr(pathWordsNumPort,normalize(graphicsNum,commonDivisorPort))
    writeFile("tags", "Porter", stats[0], stats[1], filename = resultFile)
    
    #8th data value Porter   
    stats = scipy.stats.pearsonr(pathWordsNumPort,normalize(emoticanNum,commonDivisorPort))
    writeFile("emoticans", "Porter", stats[0], stats[1], filename = resultFile)
    
    #9th data value Porter   
    stats = scipy.stats.pearsonr(pathWordsNumPort,normalize(ellipsesNum,commonDivisorPort))
    writeFile("ellipses", "Porter", stats[0], stats[1], filename = resultFile)
    
    
    resultFile.close()
  
    

#Open file and create directory if it does not exist  
def fileOpen(filename, param = 'r'):
    if(os.path.isdir("data/result") == False):
        os.makedirs("data/result")
    try:
        return open(filename, param, encoding='utf8')
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
    return [BeautifulSoup(sentence).get_text().replace("\\n","\n") for sentence in listItem]
    
#Applied word stemmer to list. Returns a list of stem words using either Porter or Lancaster
def wordStemmer(listItem, stemType):
    if(stemType == 'porter'):
        ps = PorterStemmer()
        return [ps.stem(item) for item in listItem]
    elif(stemType == 'lancaster'):
        ps = LancasterStemmer()
        return [ps.stem(item) for item in listItem]
        

#Locates the pathwords in the text and counts there frequency. Function returns a floating point
#value   
def wordFrequency(pathWords, userPost):
    userPost = Counter(userPost)
    return sum([userPost[word] for word in pathWords if userPost[word]])

 #Remove stop words from list
def stopWordsRemover(listItem, stopwords):
    return [item for item in listItem if item not in stopwords]    

#Function locates graphical html tags and counts there frequency
#Fucntion retruns a floating point value
def getGraphics(listItem):
    soup = BeautifulSoup(str(listItem))
    pattern = re.compile("[biu]|em|strong|strike|font|pre|tt|code|img", re.I)

    return len(soup.findAll(pattern))

    
#Function locates emoticons in the text and counts there frequency
#The function returns a floating point value
def getEmotican(listItem):
    pattern = re.compile(r"([:=][-っ^oc']?[-j#x$\\ls.þp*0o@|\
                         <c\{\}>3d()\]\[][|)]?|[8x][-]?[}d]|\
                         [>][:][/[()p\\/]|[d][:]?[']?[<:;='][:]?\s+|x[-]?[p]\s|\
                         [0o][:;][-]?[)3]|[}3][:]-?[)]|\^<_<|>_>\^|\|[;]?-[o)]|\
                         #-\)|%-?\)|:?-?###..|\
                         <:-[|]|ಠ_ಠ|<\s*\*\s*\)\s*\)\s*\)\s*-\s*{|>\s*<\s*\(\s*\(\s*\(\s*\*\s*>|\
                         ><>|\\o/|\*\\0/\*|@}-;-'---|@>-->--|~\(_8^\(I\)|[5~]:-[)\\]|\
                         //0-0\\\\\]|\*<\|:-\)|,:-\)|7:^\]|<//*3|[:=][-っ^oc']?[b]\s+|\
                          [<>][:;=8][\-o\*\']?[\)\]\(\[dDpP/\:\}\{@\|\\]|\
                         [\)\]\(\[dDpP/\:\}\{@\|\\][\-o\*\']?[:;=8][<>]?)", re.I)
    wordSplit = re.split(pattern, listItem)

    return sum([1 for emot in wordSplit if re.match(pattern, emot)])
        

def getEllipses(listItem):
    pattern = re.compile(r"\.\.\.*")
    
    #wordPuctTokenize = WordPunctTokenizer()
    #words = wordPuctTokenize.tokenize(listItem)
 
    return sum([1 for word in listItem if re.match(pattern, word)])
        
    
    
    
#Rapper function. Takes the text read from the Path-Words.csv and POST.tsv file
#and executes the a fucntion to calculate the frequency of path-words, html tags, emoticons,
#or ellipsis. The function returns a list of numbers measuring the frequencies
def frequentNum(listItem, freqType, word = " "):
    
    #Tokenize the text into periods and words
    tok = WordPunctTokenizer()
    

    #Calculate the frequency of stopwords
    if freqType == "p":
        return [wordFrequency(word, tok.tokenize(sentence)) for sentence in listItem]
    #Calculate the frequency of html tags
    elif freqType == "g":
        return [getGraphics(sentence) for sentence in listItem]
    #Calculate the frequency of emoticans
    elif freqType == "e":
        return [getEmotican(sentence) for sentence in listItem]
    #Calculate the frequency of Ellipses
    elif freqType == "l":
        return [getEllipses(tok.tokenize(sentence)) for sentence in listItem]

#Write result of calculation to CSV result file. Function takes any number of pararmeters
#File handle must be passed        
def writeFile(*content, filename):
        outf = csv.writer(filename, delimiter = ',')
        outf.writerow(content)
        
def normalize(listItem, divisor):
    return [(item/divisor) for item in listItem]
    
    
   
    
    
    
    
if __name__ == '__main__':
    main()