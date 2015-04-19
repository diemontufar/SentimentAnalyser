import sys

sys.path.insert(0,"/Library/WebServer/Documents/SentimentAnalyser/classifier")
sys.path.append("/Library/WebServer/Documents/SentimentAnalyser/classifier/tweet_classifier")
from tweet_classifier import classifier #classifier helper

text = "I hate you but I love you"
analysed_result = classifier.doSentimentAnalysis(text)
print("Sentiment: ", analysed_result["sentiment"])
print("Polarity: ", analysed_result["polarity"])
print("subjectivity",analysed_result["subjectivity"])