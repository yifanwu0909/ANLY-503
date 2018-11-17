import tweepy
from tweepy import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import re
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
##install wordcloud
from wordcloud import WordCloud, STOPWORDS

consumer_key = 'LXZ1jcgZ0T9sL5E9lHpQrN9CL'
consumer_secret = 'uY049Uy5Zf9B4pEwGKS1Fmd7tT6u4pK1K7EX1oEvnduw0iKQSU'
access_token = '894172280724402176-FBacvwsR6t1M01Q2a4EicuenQ5gljtV'
access_secret = 'mWLfogszz05tf6SpmPDwOzI6BhU98AYlzvWWFjeVZCuKq'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#%%
class Listener(StreamListener):
    print("In Listener...") 
    tweet_number=0
    #__init__ runs as soon as an instance of the class is created
    def __init__(self, max_tweets, hfilename, rawfile):
        self.max_tweets=max_tweets
        print(self.max_tweets)     
    #on_data() is a function of StreamListener as is on_error and on_status    
    def on_data(self, data):
        self.tweet_number+=1 
        print("In on_data", self.tweet_number)
        try:
            print("In on_data in try")
            with open(hfilename, 'a') as f:
                with open(rawfile, 'a') as g:
                    tweet=json.loads(data)
                    tweet_text=tweet["text"]
                    print(tweet_text,"\n")
                    f.write(tweet_text) # the text from the tweet
                    json.dump(tweet, g)  #write the raw tweet
        except BaseException:
            print("NOPE")
            pass
        if self.tweet_number>=self.max_tweets:
            sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')
    #method for on_error()
    def on_error(self, status):
        print("ERROR")
        if(status==420):
            print("Error ", status, "rate limited")
            return False
        
hashname=input("Enter the hash name, such as #womensrights: ") 
numtweets=eval(input("How many tweets do you want to get?: "))
if(hashname[0]=="#"):
    nohashname=hashname[1:] #remove the hash
else:
    nohashname=hashname
    hashname="#"+hashname

#Create a file for any hash mine    
hfilename="file_"+nohashname+".txt"
rawfile="file_rawtweets_"+nohashname+".txt"
twitter_stream = Stream(auth, Listener(numtweets, hfilename, rawfile))
twitter_stream.filter(track=[hashname])       

#%%
from nltk.tokenize import word_tokenize

import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import re

linecount=0
hashcount=0
wordcount=0
BagOfWords0=[]
BagOfHashes=[]
BagOfLinks=[]


tweetsfile = 'file_HappyHalloween.txt'#hfilename

###################################

with open(tweetsfile, 'r') as file:
    for line in file:
        #print(line,"\n")
        tweetSplitter = TweetTokenizer(strip_handles=True, reduce_len=True)
        WordList=tweetSplitter.tokenize(line)

        regex1=re.compile('^#.+')
        regex2=re.compile('[^\W\d]')
        regex3=re.compile('^http*')
        regex4=re.compile('.+\..+')
        regex5 = re.compile('^(?:(?!_).)*$')
        regex6 = re.compile('^(?:(?!ud).)*$')
        regex7 = re.compile('^(?:(?![a-z]+\d+).)*$')
        
        for item in WordList:
            if(len(item)>2):
                if((re.match(regex1,item))):
                    newitem=item[1:]
                    BagOfHashes.append(newitem)
                    hashcount=hashcount+1
                elif(re.match(regex2,item)):
                    if(re.match(regex3,item) or re.match(regex4,item)):
                        BagOfLinks.append(item)
                    elif(re.match(regex5, item) and 
                         re.match(regex6, item) and 
                         re.match(regex7, item)):
                        BagOfWords0.append(item.lower())
                        wordcount=wordcount+1
                else:
                    pass
            else:
                pass
     
        
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import stopwords
    
BagOfWords = [lemmatizer.lemmatize(i) for i in BagOfWords0 if i not in stopwords.words()] 

print(BagOfWords)

BigBag=BagOfWords+BagOfHashes

#%%


#list of words I have seen
seenit=[]
#dict of word counts
WordDict={}
Wordfilename="TwitterResults.txt"
Freqfilename="TwitterWordFrq.txt"

#FILE=open(Freqfilename,"w")
#FILE2=open(Rawfilename, "w")
W_FILE=open(Wordfilename,"w")
F_FILE=open(Freqfilename, "w")

IgnoreThese=["and", "and","this", "for", 
             "the", "is", "or", "will", 
             "god", "bible",
              "Download", "free", 
             "hit", "within", "steam", "via", "know",
              "unit", "always", "take", "Take", "left", "Left",
             "lot","robot", "Robot", "Lot", "last", "Last", "Wonder", "still", "Still",
             "ferocious", "Need", "need", "fit", "translator_type", "Flint", "MachineCredit",
             "Webchat", "luxury", "full", "fifdh17", "New", "new", "Caroline",
             "Tirana", "Shuayb", "repro", "attempted", "key", "Harrient", 
             "Chavez", "Women", "women", "Mumsnet", "Ali", "Tubman", "girl","Girl",
             "CSW61", "IWD2017", "Harriet", "Great", "great", "single", "Single", 
             "tailoring", "ask", "Ask", "null", "url", "False", "text", "index", "url",
             "type", "null", "false", "c0deed", "hashtags", "hashtag", "u2026", "u2022",
             "resize", "medium", "true", "name", "entity", "lang", "crop", "truncated", 
             "twitter", "coordinate", "small", "large", "size", "symbol","notification",
             "thumb", "photo", "place", "low", "following", "user", "href", "contributor",
             "contributors", "description", "retweeted", "ufe", "protected",
             "source", "rel", "none", "favorited", "location", "oct", "geo", "nofollow", 
             "iphone", "android", "mon", "web", "client", "wed", "f5f8fa", "verified", 
             "la", "ddeef", "fri", "que", "rosie", "twitch", "tweet", "funko", 
             ]
###Look at the words
for w in BigBag:
    if(w not in IgnoreThese):
        rawWord=w+" "
        W_FILE.write(rawWord)
        if(w in seenit):
            #print(w, seenit)
            WordDict[w]=WordDict[w]+1 #increment the times word is seen
        else:
            ##add word to dict and seenit
            seenit.append(w)
            WordDict[w]=1

for key in WordDict:
    #print(WordDict[key])
    if(WordDict[key]>=1):
        if(key not in IgnoreThese):
            #print(key)
            Key_Value=key + "," + str(WordDict[key]) + "\n"
            F_FILE.write(Key_Value)

W_FILE.close()
F_FILE.close()

Col_FILE = open('tableau.txt', "w")
for word in BigBag:
    Col_FILE.write(word+"\n")
Col_FILE.close()

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
##install wordcloud
from wordcloud import WordCloud, STOPWORDS

with open(Wordfilename) as f:
    lines = f.readlines()                                                                            
text = "".join(lines) 
print(text)

#%%
plt.figure(figsize = (5,5), dpi=800)
wordcloud = WordCloud().generate(text)
# Open a plot of the generated image.
plt.imshow(wordcloud)
plt.axis("off")
plt.show()



































