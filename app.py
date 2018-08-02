
import time

from flask import Flask, g, request, render_template

from getter1 import Getter
from redisClient import RedisClient

app = Flask(__name__)

def redis_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('get_json.html')



@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        key = request.form.get('key')
        print(key)
    conn = redis_conn()
    jsonStr = Getter(key).run()

    conn.add(jsonStr)
    return jsonStr


@app.route('/get', methods=['POST', 'GET'])
def get():
    conn = redis_conn()
    jsonStr = conn.getvalue(key=time.strftime("%Y%m%d%H"))
    return jsonStr





if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, port=5001)
    # manage.run()
    app.run()