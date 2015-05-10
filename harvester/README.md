Harvester & Classifier module
===================

- - - - 

This module pulls tweets provided by the Twitter streaming API corresponding to a particular bounding box.
During the process, each tweet will be analysed and then stored on a noSQL database (couchdb).

The process analyses 4 main features:

1. ID
2. Sentiment
3. Gender
4. Geo location


- - - - 

## 1. Tweet Identification (ID):

Each tweet has its own ID. It is meant to be unique, so it is used as a document _id for the couchdb database as well.

## 2. Sentiment Analysis:

Sentiment Analysis is performed by a python open source library called tweet_classifier. It takes a text as parameter and returns a list with the sentiment results which includes a cleaned text, sentiment (positive,negative or neutral), polarity (a number between -1.0 and 1.0) and the subjectivity (0 - 100%). Concepts used by the library [TextBlob](http://textblob.readthedocs.org/en/dev/advanced_usage.html#sentiment-analyzers) are highly applied.

Further information: [tweet_classifier](https://github.com/diogonal/classifier), and [TextBlob](http://textblob.readthedocs.org/en/dev/)

## 3. Gender Analysis:

Althought gender is not provided on streamed tweets, this field can be guessed from information defined in the 'user' field. Generally, users put their real names on the 'user.name' field, so we can perform a quick tokenization on the text and use the genderizer open source library to compute the gender and inlcude it on the tweet before inserting on a database.

Genderizer uses NLTK tools to guess whether a first name is male or female. However, given that we cannot control which information is included in most of the fields defined on a tweet, we end up getting rubbish that cannot be processed accurately by the genderizer. In the case a name cannot be guessed, it will throw a null which will be inlcuded on the tweet as well. Anyhow, previous tests showed that 70% - 75% of the tweets have well defined user names, so results still be a richful source of information that may be used for data analysis later on.

Further information: [genderizer](https://github.com/muatik/genderizer)

## 4. Geo location:

Streamed tweets only correspond to a predefined bounding box. The API will allow us to pull 1% of the tweets falling inside the mentioned bounding box. Most of the time (if tweets have geo location activated) exact geotagged tweets have the 'coordinates' field populated with the exact location. However, sometimes they provide only an approximated location defined on the 'place.bounding_box.coordinates' filed. Such filed will be analysed and formatted as a GeoJson polygon, allowing us to analyse data considering more accurate positioning information.

- - - - 

