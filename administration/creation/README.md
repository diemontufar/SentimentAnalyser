Database Creation
===================

## Description

Creates databases on the defined nodes depending on their roles and configurations. Thus, a master node may have a big couchdb which is populated through replication by the slave nodes which have other couchdb instances running on them. This is a typical configuration when a Twitter harvesting process is involved.

## Requirements

A couchdb instance assumed to be running on: http://localhost:5984

## Databases

* **CULTURES:** Contains geojson and population information of the suburbs of the main cities of Australia.
* **SUBURBS:** Contains a list of inner suburbs of the main cities of Australia: Melbourne, Sydney, Hobart, Darwin, Brisbane, Perth and Adelaide.
* **LANGUAGES:** Contains information related to languages spoken in he countries of birth found on the cultures database. This serves as a link between tweets and data defined on the cultures and suburbs database.

## Usage

### Creatinng databases individually

Execute the creation script defined inside each directory corresponding to each database.

* **Cultures**

```
$ cultures/create_cities_couchdb.sh
```

* **Suburbs**

```
$ suburbs/create_suburbs_couchdb.sh
```

* **Languages**

```
$ languages/create_languages_couchdb.sh
```

### Creatinng all databases

```
$ create_all.sh
```
