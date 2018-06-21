import MySQLdb
import os

wp_db = MySQLdb.connect(
    host=os.environ['WP_HOSTNAME'],
    user=os.environ['WP_USERNAME'],
    password=os.environ['WP_PASSWORD'],
    db=os.environ['WP_DB_NAME']
)
wiki_db = MySQLdb.connect(
    host=os.environ['WIKI_HOSTNAME'],
    user=os.environ['WIKI_USERNAME'],
    password=os.environ['WIKI_PASSWORD'],
    db=os.environ['WIKI_DB_NAME']
)

dam_db = MySQLdb.connect(
    host=os.environ['DAM_HOSTNAME'],
    user=os.environ['DAM_USERNAME'],
    password=os.environ['DAM_PASSWORD'],
    db=os.environ['DAM_DB_NAME']
)
