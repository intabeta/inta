from __future__ import print_function

#import nltk
import urllib2
from bs4 import BeautifulSoup
from collections import defaultdict

from subprocess import Popen, PIPE
from os.path import abspath,dirname

STANFORD_PATH='/home/bwloeb/webapps/mlbinta_django/mlbinta/autotag/stanford-postagger/'
directory='/home/bwloeb/webapps/mlbinta_django/mlbinta/autotag/'

def stanfordTag(text):
        text = text.replace('\n','. ')
        text = text.encode('ascii','ignore')
        data=open(directory+'data.txt','w')
        print(text,end='',file=data)
        data.close()
        file=Popen("cd "+STANFORD_PATH+"; ./stanford-postagger.sh models/wsj-0-18-bidirectional-nodistsim.tagger "+directory+"data.txt", shell=True, stdout=PIPE).stdout
        sentences=file.readlines()
        postagged = [[tuple(word.split('_')) for word in sentence] for sentence in [sent.split(' ') for sent in sentences]]
        return postagged

def getnouns(taggedtext):
        taggedwords = [word for sentence in taggedtext for word in sentence]
        return [a[0] for a in taggedwords if a[-1][0]=='N']

def getverbs(taggedtext):
        taggedwords = [word for sentence in taggedtext for word in sentence]
        return [a[0] for a in taggedwords if a[-1][0]=='V']

def collocations(taggedtext):
        bigrams = []
        for sentence in taggedtext:
                for i in range(len(sentence))-1:
                        bigrams.append((sentence[i],sentence[i+1]))
        return bigrams

def filtersent(taggedtext):
        #filter out 'sentences' with no verbs
        result = []
        for sentence in taggedtext:
                for word in sentence:
                        if word[-1][0]=='V':
                                result.append(sentence)
                                break
        return result

def grabtext(url):
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) #opener than can handle cookies
        url = opener.open(url)
        html = ''.join(url.readlines())
        soup = BeautifulSoup(html)

        text=''
        for par in soup.body.find_all('p'):
                text += '\n'+par.get_text()
        return text

def getkeywords(url,n=3):
        text = grabtext(url)
  #      stopwords = nltk.corpus.stopwords.words('english')
        nouns = getnouns(filtersent(stanfordTag(text)))
 #       nouns = [noun.lower() for noun in nouns if noun.lower() not in stopwords]
        data = defaultdict(int)
        for noun in nouns:
                data[noun]+=1

        topnouns = sorted([datum for datum in data.items() if datum[1]>1], key=lambda d: d[1])
        return topnouns[-n:]
