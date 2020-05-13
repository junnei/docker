import time
import redis
from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

#db = SQLAlchemy(app)

#conn_string = "host='localhost' dbname ='postgres' user='postgres' password='postgres'"
#conn = psycopg2.connect(conn_string)
#cur = conn.cursor()

#class Result(db.Model):
#    __tablename__ = 'results'
#
#    id = db.Column(db.Integer, primary_key=True)
#    url = db.Column(db.String())
#    result_all = db.Column(JSON)
#    result_no_stop_words = db.Column(JSON)
#
#    def __init__(self, url, result_all, result_no_stop_words):
#        self.url = url
#        self.result_all = result_all
#        self.result_no_stop_words = result_no_stop_words
#
#    def __repr__(self):
#        return '<id {}>'.format(self.id)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

#    if(count<=1):
#        cur.execute("CREATE TABLE countdb (nid PRIMARY KEY, creation_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
#        conn.commit()​
#        return 'Hello World! I have been seen first times.\n'.format(count)
#    else:
#        query = """INSERT INTO countdb (nid) VALUES (%s)"""
#        cur.execute(query, cound)
#        conn.commit()​
#        query = """SELECT * from countdb"""
#        result = execute(query)
#        print(result)
#        return 'Hello World! I have been seen {} times.\n'.format(count)
