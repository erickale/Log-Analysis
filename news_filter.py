from datetime import datetime
import psycopg2

# Objective
# 1. What are the most popular three articles of all time?
# 2. Who are the most popular article authors of all time?
# 3. On which days did more than 1% of requests lead to errors?

#Constants
DATABASE_FILENAME = 'news'
DB_CONNECTION_STRING = 'dbname={}'.format(DATABASE_FILENAME)


def create_db_views():
    """
    This will allow for an easy update to the database without running several command lines and takes
    the burden off the end user to setup the views correctly.
    """
    with psycopg2.connect(DB_CONNECTION_STRING) as connection:
        c = connection.cursor()
        # This will remove the current views from the database and recreate them if they exist.
        print('Creating database views')
        c.execute("DROP VIEW IF EXISTS top_articles")
        c.execute("DROP VIEW IF EXISTS top_authors")
        c.execute("DROP VIEW IF EXISTS error_hits")
        c.execute("DROP VIEW IF EXISTS total_hits")

        sql_create_view_top_articles = "CREATE VIEW top_articles AS " \
                                       "SELECT articles.title, count(*) AS hits " \
                                       "FROM log  JOIN articles ON substring(path, 10) = articles.slug " \
                                       "WHERE status = '200 OK' AND length(path) > 1  " \
                                       "GROUP BY log.path, articles.title " \
                                       "ORDER BY hits DESC LIMIT 3"

        sql_create_view_top_authors = "CREATE VIEW top_authors AS " \
                                      "SELECT authors.name, count(*) AS hits " \
                                      "FROM log JOIN articles ON substring(path, 10) = articles.slug " \
                                      "JOIN authors ON articles.author = authors.id " \
                                      "WHERE status = '200 OK' AND length(path) > 1 " \
                                      "GROUP BY authors.name ,articles.title " \
                                      "ORDER BY authors.name DESC"

        sql_create_view_error_hits_count = "CREATE VIEW error_hits AS " \
                                           "SELECT (cast(time AS DATE)) AS error_date, count(*) AS error_hits " \
                                           "FROM log WHERE status = '404 NOT FOUND'  " \
                                           "GROUP BY error_date, status " \
                                           "ORDER BY error_date;"

        sql_create_view_total_hits_counts = "CREATE VIEW total_hits  AS " \
                                            "SELECT (cast(time AS DATE)) AS total_date, count(*) AS total_hits  " \
                                            "FROM log " \
                                            "GROUP BY total_date" \
                                            " ORDER BY total_date;"

        c.execute(sql_create_view_top_articles)
        c.execute(sql_create_view_top_authors)
        c.execute(sql_create_view_error_hits_count)
        c.execute(sql_create_view_total_hits_counts)

        print('Finished creating database views')


def top_articles():
    # this will return the top 3 articles of all time.
    # this function will use the top_articles view we created to generate the report

    with psycopg2.connect(DB_CONNECTION_STRING) as connection:
        cur = connection.cursor()
        sql_string = "SELECT * FROM top_articles"
        cur.execute(sql_string)
        rows = cur.fetchall()
        print()
        print("Most popular articles of all time.")
        for count, row in enumerate(rows):
            print("{0}) {1} - {2} views".format(count + 1, row[0], row[1]))


def top_authors():
    # this will return the authors in order of their article views.

    with psycopg2.connect(DB_CONNECTION_STRING) as connection:
        cur = connection.cursor()
        sql_string = "SELECT name, sum(hits) AS total_hits " \
                     "FROM top_authors " \
                     "GROUP BY name " \
                     "ORDER BY total_hits DESC;"
        cur.execute(sql_string)
        rows = cur.fetchall()
        print()
        print("Most popular authors of all time.")
        for count, row in enumerate(rows):
            print("{0}) {1} - {2} views".format(count + 1, row[0], row[1]))


def error_rate():
    #this function will query the database for which day had the highest error rate.

    with psycopg2.connect(DB_CONNECTION_STRING) as connection:
        cur = connection.cursor()
        sql_string = "SELECT total_date, total_hits, error_hits, " \
                     "error_hits::DOUBLE PRECISION/total_hits::DOUBLE PRECISION * 100 " \
                     "FROM total_hits " \
                     "JOIN error_hits ON error_hits.error_date = total_hits.total_date;"
        cur.execute(sql_string)
        rows = cur.fetchall()
        print()
        print("Day with the highest error rate. ")
        temp = max(rows, key=lambda x: x[1])
        year = str(temp[0])[0:4]
        day = str(temp[0])[8:10]
        mydate = datetime.now()
        print("{} {},{} - {:.2f}% errors".format(mydate.strftime("%B"), day, year, temp[3]))

def main():

    create_db_views()
    top_articles()
    top_authors()
    error_rate()


if __name__ == '__main__':
    main()
