
import classifier_settings as settings #Custom Settings
import re #Parsisng
from ttp import ttp #For extracting usernames and hashtags
from textblob import TextBlob #Parsing and Sentiment analysis
import json #Working with sentiments
import html.parser
import time

with open('tweet_classifier/sentiments.json') as sentiments_json:    
    sentiments = json.load(sentiments_json)

email_regex = re.compile(settings.email)

# Remove usernames, hashtags and 
def extractUsernamesHashtagsURLS(ttp_obj,text):
	for username in ttp_obj.users:
		text = text.replace('@'+username,'')

	for tag in ttp_obj.tags:
		text = text.replace('#'+tag,'')

	for url in ttp_obj.urls:
		text = text.replace(url,'')
	return text

# Twitter text comes HTML-escaped, so unescape it.
# We also first unescape &amp;'s, in case the text has been buggily double-escaped.
def normalizeTextForTagger(text):
    text = text.replace("&amp;", "&")
    text = html.parser.HTMLParser().unescape(text)
    return text

#Remove emails
def removeEmails(text):
	email_regex = re.compile(settings.email)
	text = email_regex.sub('', text) #remove URL
	return text

#Remove line breaks helper
def removeLineBreaks(text):
	return text.replace('\n',' ')

#Parse Text:
#	1. Remove URL's
#	2. Remove line breaks (convert then into spaces)
#	3. Remove emojis
def parseText(text):

	p = ttp.Parser()
	ttp_result = p.parse(text)
	text = extractUsernamesHashtagsURLS(ttp_result,text)
	text = normalizeTextForTagger(text)
	text = removeEmails(text)
	text = removeLineBreaks(text)

	# Loop over each character finding strange characters
	emojis = {}
	i = 1
	for character in text:
		if(ord(character)>128):
			# print("Found a strange thing: " + str(ord(character)))
			#emojis[code] = span -> {code:span} pairs
			emojis[i] = str(ord(character)) 
		i+=1

	# print("Emojis: ", emojis)

	temp_text = list(text)
	for emoji in emojis:
		index = int(emoji) - 1
		if emojis[emoji] in sentiments["sentiments"]["emojis"]:
			# print("Emoji was found!")
			temp_text[index] = str(sentiments["sentiments"]["emojis"][emojis[emoji]]) + " "
		else:
			# print("Emoji was ignored!")
			temp_text[index] = "" #-> Here we should call another method to check if it's english
	text = "".join(temp_text)

	return text #Return parsed/cleaned tweet

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


#Get the analysed text. This is the main method which perfomrs sentiment analysis
#The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a 
#float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.
def doSentimentAnalysis(text):
	text = parseText(text)
	tweet = TextBlob(text)
	sentiment = getSentiment(tweet)
		
	return { 'text': text, 
		'sentiment': sentiment, 
		'subjectivity': tweet.subjectivity* 100.0,
		'polarity': tweet.polarity }



