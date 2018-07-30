import time

from flask import Flask, g, request

from getter import Getter
from reidsClient import RedisClient

app = Flask(__name__)

def redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        q = request.args.get('q')
    conn = redis_conn()
    jsonStr = conn.getvalue(key=time.strftime("%Y%m%d"))
    return jsonStr


@app.route('/get', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        q = request.args.get('q')
    jsonStr = Getter(q).run()
    return jsonStr


if __name__ == '__main__':
    app.run(allow='0.0.0.0', debug=True)
