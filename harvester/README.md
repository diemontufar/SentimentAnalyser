Harvester & Classifier Module
===================

- - - - 

This module harvests tweets coming from the Twitter streaming API falling within a particular bounding box.
During the process, each tweet will be analysed and then stored on a noSQL database (couchdb).

##Features:

* Harvesting tweets from a particular bounding-boxed zone
* Starting and Stopping scripts for running multiple instances (multiple zones)
* Notification tools (for emailing status and printing logs)

## Analysis stage

Analysis stage involves the following steps:

1. Obtaining tweet ID
2. Performing Sentiment analysis on text field
3. Performing Gender analysis on user names
4. Mining Geo location

- - - - 

## 1. Obtaining Tweet Identification:

Each tweet has its own ID. It is meant to be unique, so it is used as a document _id for the database on couchdb as well. If the database does not exists, it will be created automatically as defined on the settings.py file.

## 2. Sentiment Analysis:

Sentiment Analysis is performed by using a python open source library called tweet_classifier which was specially developed and open sourced for this project. It takes a text as parameter and returns a list with the sentiment results, which includes a cleaned version of the original text, the sentiment (positive,negative or neutral), the polarity (a number between -1.0 and 1.0) and the subjectivity (0 - 100%). Concepts used by the library [TextBlob](http://textblob.readthedocs.org/en/dev/advanced_usage.html#sentiment-analyzers) are highly applied.

Further information:<br>
* [tweet_classifier](https://github.com/diogonal/classifier)<br> 
* [TextBlob](http://textblob.readthedocs.org/en/dev/)

## 3. Gender Analysis:

Althought gender is not provided on streamed tweets, this field can be guessed from information defined in the 'user' field. Generally, users put their real names on the 'user.name' field, so we can perform a quick tokenization to the text and use the genderizer open source library to compute the gender and inlcude it on the tweet before inserting on a database.

Genderizer uses NLTK tools to guess whether a first name is male or female. However, given that we cannot control which information is included in most of the fields defined on a tweet, we end up getting rubbish, which cannot be processed accurately by the genderizer. In the case a name cannot be guessed, it will throw a null which will be included on the tweet as well. Anyhow, previous tests showed that 70% - 75% of the tweets have well defined user names, so results still are a richful source of information that may be used for data analysis later on.

Further information: [genderizer](https://github.com/muatik/genderizer)

## 4. Geo location:

Streamed tweets only correspond to a predefined bounding box. The API will allow us to pull 1% of the tweets falling inside the mentioned bounding box. Most of the time (if tweets have geo location activated) exact geotagged tweets have the 'coordinates' field populated with the exact location. However, sometimes they provide only an approximate location defined on the 'place.bounding_box.coordinates' filed. Such filed will be analysed and formatted as a GeoJson polygon, allowing us to analyse data considering more accurate positioning information on later stages.

# Getting Started

## Background 

Since tweets are streamed continuously from he Twitter API, we need to run the harvester program as a daemon process. Alternatively, one may want to keep multiple instances running at the same time. Often, each instance corresponds to a particular bounding box defining a zone of interest. 

This module presents two alternatives for harvesting tweets. The first one is a generic version which allows you to harvest tweets and perform Sentiment analysis before storing them on a couchdb database. The second one does the same job, but considering Gender analysis as well. The later was developed as a proof of concept in order to test accuracy and usefulness of the genderizer python library.

## Requirements

* **Python 2.7+** (Newer python versions works as well)
* **tweet_classifier**        -> Sentiment Analysis
* **TextBlob**                -> Sentiment & Gender Analysis
* **twitter-text-python**     -> Sentiment Analysis
* **couchDB**                 -> Save tweets on coucdb database
* **python-memcached**        -> Gender Analysis
* **naiveBayesClassifier**    -> Gender Analysis
* **genderizer**              -> Gender Analysis
* **tweepy**                  -> Pulling tweets from the Twitter API

All the libraries listed above can be installed individually or by executing the following command:

```
$ sudo pip install -r requirements.txt
```

## Configuration

There are two python programs which can be used for harvesting tweets:

1. **generic_harvester.py:** Harvest tweets and perform Sentiment Analysis and Geo location process only.
2. **harvester_classifier.py:** Harvest tweets and perform Sentiment Analysis, Geo location process and Gender Analysis.

Before executing any of the mentioned programs you must configure the settings.py. There are three main points which should be considered:

1. The Harvester 

## Execution & Termination

The following variables must be replaced with your configuration parameters.

**{quadrant_number}:** Parameter which defines the quadrant defined on the settings.py file (i.e 2)<br>
**{initial_quadrant_number}:** Parameter which defines the initial quadrant defined on the settings.py file (i.e 4)<br>
**{final_quadrant_number}:** Parameter which defines the final quadrant defined on the settings.py file (i.e 8)<br>
**{process_num}:** System process id generated by the OS to the daemon process<br>

* Running a single instance of the program (As a Python program):

```
$ python harvester_classifier.py {quadrant_number}
```
* Running a single instance of the program (As a unix daemon process):
```
$ nohup python harvester_classifier.py {quadrant_number} 2>1 &
```
* Running a range of instances of the program (As unix daemon processes):
```
$ ./start_harvesting.sh {initial_quadrant_number} {final_quadrant_number}
```
* Running all configured instances of the program (As unix daemon processes):
```
$ ./start_harvesting.sh
```
* Stopping a single instance of the program (As a Python program):
```
$ Crtl+C
```
* Stopping a single instance of the program (As a daemon process):
```
$ sudo kill -15 {process_num}
```
* Stopping multiple instances of the program (As daemon processes):
```
$ ./stop_harvesting
```
## Notifications

Email notifications are sent whether a process starts, stops unexpectedly or a certain amount of tweets are collected.

* A notification for a starting process looks like this:
```
Server has initiated harvesting process
Process initiated at: Fri May  8 09:14:00 2015
Location: Queensland, Quadrant: 1
Process Id: 777
Server: http://localhost:5984/
Database: queensland
VM: node4:115.146.**.**
```

* A notification for an unexpected interruption of the process looks like this:
```
Server has interrupted harvesting process.
Process terminated at: Thu May  7 07:45:05 2015
Location: WesternAU1, Quadrant: 2
VM: node3:115.146.**.**
Process Id: 646
Total tweets received: 2661
```
* A notification for an update of the process looks like this:
```
Harvesting process status update
10K new tweets on database: nsw
```
