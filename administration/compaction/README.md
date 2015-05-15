Compaction
===================

## Description

![alt tag](https://github.com/diogonal/SentimentAnalyser/blob/master/wiki/img/couchcompact.png)

Resources need to be used efficiently since in some cases they can be reduced like storage capacity. Thus, using compaction which is another feature supported by couchdb, we can compress and get rid of old documents, leading to considerable saves in disk storage. This task may be executed every week or so, depending on the amount of data stored on your databases. 

## Usage

1. Configure your compact.sh file to satisfy your needs.

2. Excecute the program:

```
$ ./compact.sh
```

A log file will be created, which looks something like this:

```
Compacted at:  29/03/2015 09:09:42
Compacted at:  29/03/2015 09:10:57
```
