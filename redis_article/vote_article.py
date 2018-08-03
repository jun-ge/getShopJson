import time
import redis

ONE_WEEK_IN_SECONDS = 7 * 24 * 60 * 60

conn = redis.Redis()


def post_article(conn, user, title, link):
    conn = redis.Redis()
    article_id = str(conn.incr('article:'))
    voted = 'voted:' + article_id
    # 创建已投用户的集合
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)
    now = time.time()
    article = 'article:' + article_id
    # 创建文章信息的散列
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })
    conn.zadd('score:', article, now + )