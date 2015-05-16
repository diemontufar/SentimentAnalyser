Web Module
===================

## Description

The web module is a dashboard-based HTML5 application which shows sentiment analysis restuls and other data analysis charts by calling serveral web services implemented for this project. 

## Features

* **Searches by Topic**

* **Maps Module:** GeoJson information about the main cities and suburbs of Australia will be loaded depending on user's selection. Tweets falling within selected area will be shown as colored markers on the map. 

* **Sentiment Analysis:** Several modules show sentiment analysis results with different dynamic chart configurations. The most relevant are: Sentiment totals by suburb/city and Top lists of trends, twitterers and twitterer cultures.

* **Feed module:** Tweet texts are shown in a feed module separated by positives, negatives and neutrals. Thus, it is easy for a human to verify the accuracy of the results obtained by the sentiment classifier module.

* **Cluster of topics:** Trends can be identified not only by looking at the hashtag top lists, but considering correlated topics and phrases as well. The clustering module uses a lingo algorithm to create a cluster of topics found by giving it a key (which is the text we are looking for) and a date range. This process is executed on the fly against our elasticsearch index and helps to understand better what people is twittering about and to have a more general idea on which trends are currently happening or happened in the past. 

## License

The MIT License (MIT)

Copyright (c) 2015 Diego Montufar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.