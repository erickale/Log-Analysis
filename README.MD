# Logs Analysis

Intro to Programming Nanodegree's Back-End Development Final Project. 
This application will analyze and retrieve a data report from a PostgresSQL database.   

## Files Included
1. news_filter.py
2. Logs Analysis Project - Output.txt

## Install

``` 
pip install pcycopg2
```

## Getting Started
Run the news_filter.py file to generate the data report.

I've included a function called **create_db_views** within the new_filer.py that will 
generate the required database views. 

The code below is provided encase you want to manually create the database views.

```postgresql
CREATE VIEW top_articles AS
SELECT articles.title, count(*) AS hits
FROM log  JOIN articles ON substring(path, 10) = articles.slug
WHERE status = '200 OK' AND length(path) > 1 
GROUP BY log.path, articles.title
ORDER BY hits DESC LIMIT 3;
```

```postgresql
CREATE VIEW top_authors AS
SELECT authors.name, count(*) AS hits
FROM log JOIN articles ON substring(path, 10) = articles.slug
JOIN authors ON articles.author = authors.id
WHERE status = '200 OK' AND length(path) > 1
GROUP BY authors.name ,articles.title
ORDER BY authors.name DESC;
```

```postgresql
CREATE VIEW error_hits AS
SELECT (cast(time AS DATE)) AS error_date, count(*) AS error_hits
FROM log WHERE status = '404 NOT FOUND'
GROUP BY error_date, status
ORDER BY error_date;
```

```postgresql
CREATE VIEW total_hits AS
SELECT (cast(time AS DATE)) AS total_date, count(*) AS total_hits
FROM log
GROUP BY total_date
ORDER BY total_date;
```

### Sample Data Output

Most popular articles of all time.
1) Candidate is jerk, alleges rival - 338647 views
2) Bears love berries, alleges bear - 253801 views
3) Bad things gone, say good people - 170098 views

Most popular authors of all time.
1) Ursula La Multa - 507594 views
2) Rudolf von Treppenwitz - 423457 views
3) Anonymous Contributor - 170098 views
4) Markoff Chaney - 84557 views

Day with the highest error rate. 

July 17,2016 - 2.28% errors


## Built With

* [Python 3.60](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/)


## Authors

* Eric M Kale 

## last Updated
07/07/2017