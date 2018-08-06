import time

import redis

from redisClient import RedisClient

ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60
VOTE_SCORE = 432
ARTICLE_PRE_PAGE = 25

conn = redis.Redis()


# vote
def vote_article(conn, user, article, flag=None):
    conn = redis.Redis()
    coutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < coutoff:
        return
    article_id = article.split(':')[-1]
    # 若是用户添加成功，返回1
    if conn.sadd('voted:' + article_id, user):
        if not flag:
            # 对有序集合score里面的指定文章增加分数
            conn.zincrby('score:', article, VOTE_SCORE)
            # 对散列article：+ id里面的votes对应的值（投票数） + 1
            conn.hincrby(article, 'votes', 1)
        else:
            # 对有序集合score里面的指定文章减少分数
            conn.zincrby('score:', article, -VOTE_SCORE)
            # 对散列article：+ id里面的unvotes对应的值（投反对票数） + 1
            conn.hincrby(article, 'unvotes', 1)


# post
def post_article(conn, user, title, link):
    article_id = str(conn.incr('article:'))
    voted = 'voted:' + article_id
    # 创建已投用户的集合
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)
    # 创建

    now = time.time()

    article = 'article:' + article_id
    # 创建文章信息的散列
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
        'unvotes': 0,
    })
    # 创建/添加文章'分数'的有序集合
    conn.zadd('score:', article, now + VOTE_SCORE)
    # 创建/添加文章'创建时间'的有序集合
    conn.zadd('time:', article, now)
    return article_id


def change_vote(conn, article):
    temp = conn.hget(article, 'votes')
    conn.hset(article, 'votes', conn.hget(article, 'unvotes'))
    conn.hset(article, 'unvotes', temp)


def get_article(conn, page, order='score'):
    start = (page - 1) * ARTICLE_PRE_PAGE
    end = start + ARTICLE_PRE_PAGE
    # 获取所有文章的id
    ids = conn.zrevrange('score:', start, end)
    articles = []
    for id in ids:
        # 获取文章的详细信息
        article_data = conn.hgetall(id)
        article_data['id'] = id
        articles.append(article_data)
    return articles


def add_remove_groups(conn, article_id, to_add=[], to_remove=[]):
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group, article)
    for group in to_remove:
        conn.srem('group:' + group, article)


def get_group_articles(conn, group, page, order='score:'):
    key = order + group
    if not conn.exists(key):
        # 根据评分对群组的文章，交叉的数据取最大值（key（产生的新的群组），{所有，群组按分数交叉}，取最大值（若是aggregate默认则并集求和sum相加，或可设置min取小，max去大
        #    若是weights则（num1，num2），则求交集，先分别乘以，各个集合元素先对于的num值, 对于zunionstore,最后一个参数为weights是，表示并集，所有元素都包含））
        # 在python中，keys参数若是字典类型，keys的key的value将作为weight值与每个数相乘。若是列表则正常处理

        conn.zinterstore(key, ['group:' + group, order], aggregate='max')
        conn.expire(key, 60)
    return get_article(conn, page, key)


"""
cookie 包括签名（signed）和令牌（token）两种

"""


def check_token(conn, token):
    return conn.hget('login:', token)


def update_token(conn, token, user, item=None):
    conn = redis.Redis()
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent: ', token, timestamp)
    if item:
        # 记录商品的浏览时间,和浏览次数, zadd与数据库操作不同，先写key在写value
        conn.zadd('viewed:' + token, item, timestamp)
        # 移除旧的记录，删除浏览分数最小的26个元素，(最近浏览的商品）
        conn.zremrangebyrank('viewed:' + token, 0, -26)
        # ，记录商品的浏览次数，给item的score值减少1，分值越小越靠前
        conn.zincrby('viewed:', item, -1)


"""
回话的清理
"""
QUIT = False
# 最大回话限制
LIMIT = 10000000


def clean_full_session(conn):
    conn = redis.Redis()

    while not QUIT:
        # zcard获取sorted set类型数据的数量
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue

        end_index = min(size - LIMIT, 100)
        # 获取[0, end_index-1]的浏览数据
        sessions = conn.zrange('recent: ', 0, end_index - 1)
        session_keys = []
        for sess in sessions:
            session_keys.append('viewed:' + sess)
            session_keys.append('cart:' + sess)

        # 删除浏览记录
        conn.delete(*session_keys)
        conn.hdel('login:', *sessions)
        conn.zrem('recent:', *sessions)


"""
购物车的缓存
"""


def add_to_cart(conn, session, item, count):
    # conn = redis.Redis()

    if count <= 0:
        conn.hdel('cart:' + session, item)
    else:
        conn.hset('cart:' + session, item, count)


def cache_request(conn, request, callback):
    # 如果求情不能被缓存，直接调用回调函数。
    if not can_cache(conn, request):
        return callback(request)
    # 将请求转换为简单字符串（hash），方便查找
    page_key = 'cache:' + hash_request(request)
    # 尝试查找被缓存的页面
    content = conn.get(page_key)

    # 如果没有，则生成页面，存入到缓存里面
    if not content:
        content = callback(request)
        # 将键page_key的值设置为返回的页面content，300秒后过期
        conn.setex(page_key, content, 300)
    return content


"""数据行缓存，（对于经常变化的数据） 持续运行的守护进程，短时间将指定的数据更新缓存到redis
                若是不经常变化的数据，或者商品缺货后可以接受，可是将更新的延时设置为几1分钟
"""


def schedule_row_cache(conn, row_id, delay):
    conn = redis.Redis()
    # delay时间  记录了自定数据行的缓存需要每隔多少秒更新一次
    conn.zadd('delay: ', row_id, delay)
    # 时间戳 记录了何时将数据行缓存到redis
    conn.zadd('schedule:', row_id, time.time())


# 守护进程
def cache_rows(conn):
    import json
    conn = redis.Redis()
    while not QUIT:

        # 尝试获取下一个需要被缓存的数据行和他的调度时间戳
        next = conn.zrange('schedule:', 0, 0, withscores=True)
        now = time.time()
        # 如果时间 记录的调度时间戳不大于现在的时间，停0.5,秒。（没到延时时间）
        if not next or next[0][1] > now:
            time.sleep(0.5)
            continue

        # 延时时间到........
        # 获取数据行id
        row_id = next[0][0]
        # 提前获取下一次数据行调度的延迟时间值
        delay = conn.zscore('delay:', row_id)
        # 不必再缓存这个行数据，将他的所有信息从缓存中删除
        if delay <= 0:
            conn.zrem('delay:', row_id)
            conn.zrem('schedule:', row_id)
            conn.delete('inv:' + row_id)

        # 读取数据
        row = Inventory.get(row_id)
        # 更新 调度数据时间
        conn.zadd('schedule:', row_id, now + delay)
        # json格式存储
        conn.set('inv:' + row_id, json.dumps(row.to_dict()))


"""
部分页面的缓存，更新update_token
"""


# 守护进程 函数rescale_viewed()，将缓存的商品，
def rescale_viewed(conn):
    conn = redis.Redis()
    while not QUIT:
        # 按下标删除[0, -20001]的商品，删除排行20000名之后的商品，0处是最小的元素
        conn.zremrangebyrank('viewed:', 0, -20001)
        # viewed里面的每个元素的值乘以0.5。
        conn.zinterstore('viewed:', {'viewed:': .5})
        time.sleep(300)

# 判断请求页面是否要被缓存办，判断最终条件是：商品的浏览次数值 不为0且小于10000
def can_cache(conn, request):
    # 尝试从页面获取商品id
    item_id = extract_item_id(request)

    if  not item_id or is_dynamic(request):
        return False
    # 若是 获取商品的在viewed里面的index
    rank = conn.zrank('viewed:', item_id)
    # 若是该商品的浏览次数
    return rank is not None and rank < 10000# 优先级or < and < not




if __name__ == '__main__':
    pass

