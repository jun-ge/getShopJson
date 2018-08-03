import time

import redis

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
    conn = redis.Redis()
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
        conn.zinterstore(key, {'group:' + group, order}, aggregate='max')
        conn.expire(key, 60)
    return get_article(conn, page, key)


if __name__ == '__main__':
    pass
