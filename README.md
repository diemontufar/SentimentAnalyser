# Sentiment Analyser
===================

![portal](https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/portal_complete.jpg)

**Exploring the Cultures of Australia through Social Media**

A general analysis across the many languages and cultures of Australia through social media sources of information such as Twitter was performed. A web application sup- porting a range of scenarios was implemented using state-of-the-art distributed and data analysis technologies such as ElasticSearch, with resources from the National eResearch Collaboration Tools and the NeCTAR Research Cloud. Almost 2.5 million tweets were collected from the Twitter streaming API and several sentiment analysis scenarios were applied in order to explore opinions of different ethnic and multi-cultural communities of Australia around a range of different topics including politics, sports and social impact events that took place between March and May 2015. It was shown how statistical data from the last Census (2011) from the Australian Bureau of Statistics can be correlated with information obtained from social media, allowing us to gain a deeper understanding of the multicultural diversity of Australia.
________________

## Features & Modules

* **Harvester:** For pulling tweets from the Twitter streaming API using python tweepy library ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/harvester))<br>
* **Classifier:** using an open sourced library called tweet_classifier used for Sentiment Analysis ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/classifier))<br>
* **Administration tools:** For managing Couchdb databases ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/administration))<br>
* **Orchestration tools:** using Ansible for deployment process ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/orchestrer))<br>
* **Elasticsearch indexer module:** For configuring an index in an elascticsearh cluster ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/orchestrer))<br> 
* **A RESTful web-based portal:** For testing the implemented web services module ([Here](https://github.com/diogonal/services))<br>
* **A Responsive HTML5-based dashboard:** a GUI for showing results ([Here](https://github.com/diogonal/SentimentAnalyser/tree/master/web))<br>

## Getting Started

Visit the [wiki](https://github.com/diogonal/SentimentAnalyser/wiki) or follow the README files listed on each module.

## Credits

**Author:** Diego Montufar<br>
**Supervisor:** Prof. Richard Sinnott

## Find out more

| **[Technical Docs] [techdocs]**     | **[Setup Guide] [setup]**     | **[Roadmap] [roadmap]**           | **[Contributing] [contributing]**           |
|-------------------------------------|-------------------------------|-----------------------------------|---------------------------------------------|
| [![i1] [techdocs-image]] [techdocs] | [![i2] [setup-image]] [setup] | [![i3] [roadmap-image]] [roadmap] | [![i4] [contributing-image]] [contributing] |

## License

The MIT License (MIT)

Copyright (c) 2015 Diego Montufar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[techdocs-image]: https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/docs.png
[setup-image]: https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/setup.png
[roadmap-image]: https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/roadmap.png
[contributing-image]: https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/contributing.png

[techdocs]: https://github.com/diogonal/SentimentAnalyser/wiki
[setup]: https://github.com/diogonal/SentimentAnalyser/wiki
[roadmap]: https://github.com/diogonal/SentimentAnalyser/wiki/Modules
[contributing]: https://github.com/diogonal/SentimentAnalyser/wiki
