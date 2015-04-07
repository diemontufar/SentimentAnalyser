
import classifier_settings as settings #Custom Settings
import re #Parsisng
from textblob import TextBlob #Parsing and Sentiment analysis
import sentiments #Dictionaries of emojis and extra sentiment to help TextBlob for more accurate analysis

emojire = re.compile(settings.emoji_regex, re.UNICODE)
urlre = re.compile(settings.email_regex)

#Parse Text:
#	1. Remove URL's
#	2. Remove line breaks (convert then into spaces)
#	3. Remove emojis
def parseText(text):
	text = removeURLs(text)
	text = removeLineBreaks(text)
	text = removeEmojis(text)
	return text #Return parsed/cleaned tweet

#Remove URL's helper
def removeURLs(text):
	text = urlre.sub('', text) #remove URL
	return text

#Remove Emojis hlper
def removeEmojis(text):
	text = emojire.sub('', text) #remove Emojis
	return text

#Encode UTF8
def encodeTextUTF8(text):
	return text.encode('utf-8').strip()

#Remove line breaks helper
def removeLineBreaks(text):
	return text.replace('\n',' ')

#Perform sentiment analysis
def getSentiment(tweet):
	# determine if sentiment is positive, negative, or neutral
	if tweet.sentiment.polarity < 0:
	    sentiment = "negative"
	elif tweet.sentiment.polarity == 0:
	    sentiment = "neutral"
	else:
	    sentiment = "positive"
	return sentiment

#Perform Language detection
def getLanguage(text):
	text = TextBlob(text)
	return text.detect_language()

#Get the analysed text. This is the main method which perfomrs sentiment analysis
#The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a 
#float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
def doSentimentAnalysis(text):
	text = parseText(text)
	tweet = TextBlob(text)
	sentiment = getSentiment(tweet)
	lang = getLanguage(text)
	return { 'text': text, 
		'sentiment': sentiment, 
		'lang': lang , 
		'subjectivity': tweet.subjectivity* 100.0,
		'polarity': tweet.polarity }



