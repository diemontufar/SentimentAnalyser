
import re #Parsisng
from ttp import ttp
from textblob import TextBlob #Parsing and Sentiment analysis
import json #Working with sentiments
import html.parser

with open('sentiments.json') as sentiments_json:    
    sentiments = json.load(sentiments_json)

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

def removeEmails(text):
	email = "([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"
	email_regex = re.compile((email))
	text = email_regex.sub('', text) #remove URL
	return text

p = ttp.Parser()
# text = "We both have dots in our Pictures ! Mine taken a few weeks ago in Melb yours in Syd today! #Special @ricky_martin 👽👾👽 http://t.co/hZWfDAcNSW"
text = "@yousesei なわけあるか∑(ﾟДﾟ)"
ttp_result = p.parse(text)
text = extractUsernamesHashtagsURLS(ttp_result,text)
text = normalizeTextForTagger(text)
text = removeEmails(text)

# Loop over each character finding strange characters
emojis = {}
i = 1
for character in text:
	if(ord(character)>128):
		print("Found a strange thing: " + str(ord(character)))
		#emojis[code] = span -> {code:span} pairs
		emojis[i] = str(ord(character)) 
	i+=1

print("Emojis: ", emojis)

temp_text = list(text)
for emoji in emojis:
	index = int(emoji) - 1
	if emojis[emoji] in sentiments["sentiments"]["emojis"]:
		print("Emoji was found!")
		temp_text[index] = str(sentiments["sentiments"]["emojis"][emojis[emoji]]) + " "
	else:
		print("Emoji was ignored!")
		temp_text[index] = "" #-> Here we should call another method to check if it's english
text = "".join(temp_text)
print("New text: ", text)

zen = TextBlob(text)
print("Words: ", zen.words)
# print(text)
# getEmojis(text)
# print(ttp_result.users)
# print(ttp_result.tags)
# print(ttp_result.urls)
# print(ttp_result)