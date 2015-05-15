Administration & Security Module
===================

# Description

Here we define a module which can be used for doing administration tasks on databases and system. Such tasks include:

1. Creation

Creates databases on the defined nodes depending on their roles and configurations. Thus, a master node may have a big couchdb which is populated through replication by the slave nodes which have other couchdb instances running on them. This is a typical configuration when a Twitter harvesting process is involved.

2. Replication

Duplicate tweets are removed by using replication as a tool provided by couchdb itself. Replication should be configured once you have defined your architecture and after database creation/configuration. However it may be necessary to run this process again when the system experience outages or is restarted (which is something that could happen on cloud environments).

4. Compaction

Resources need to be used efficiently since in some cases they can be reduced like storage capacity. Thus, using compaction which is another feature supported by couchdb, we can compress and get rid of old documents, leading to considerable saves in disk storage. This task may be executed every week or so, depending on the amount of data stored on your databases. 

5. Backup

Couchdb are stored on the file system as single files with .couchdb extension. This eases the backup process since we are managing the concept of documents instead of registers. This task allow us to have a complete copy of our databases in separate date labeled directories. Again, this task may be or may not be executed many times. Depending on your configuration, replication could be enough in some cases.