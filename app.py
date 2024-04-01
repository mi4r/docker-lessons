import time
import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def number_of_visits():
    retries = 10
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.3)

@app.route('/')
def hello():
    count = number_of_visits()
    return 'The ammount of visits to this site is equal to {}.\n'.format(count)
