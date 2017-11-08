# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

DBNAME = "forum"


def get_posts():
  """Return all posts from the 'database', most recent first."""
  conn = psycopg2.connect(dbname=DBNAME)
  c = conn.cursor()
  c.execute("select content, time from posts order by time desc;")
  posts = c.fetchall()
  conn.close()
  return posts

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  content = bleach.clean(content)
  conn = psycopg2.connect(dbname=DBNAME)
  c = conn.cursor()
  c.execute("insert into posts values (%s)", (content,))
  conn.commit()
  conn.close()



