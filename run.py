import random
import sqlite3
import time
import tweepy
import datetime

DBFILE = 'streets-city.db'
TEMPLATE = ' Народная Республика'

TWITTER_CONSUMER_KEY = 'I\'M'
TWITTER_CONSUMER_SECRET = 'NOT'
TWITTER_ACCESS_TOKEN = 'SO'
TWITTER_ACCESS_SECRET = 'STUPID'

TIME = [5, 10, 16]

def get_street(db, change = False):
    cur = db.cursor()
    cur.execute('SELECT rowid, name, city FROM streets WHERE used = 0')
    ret = random.choice(cur.fetchall())
    if change:
        cur.execute('UPDATE streets SET used = 1 WHERE rowid = %d' % ret[0])
        db.commit()
    return ret[1], ret[2]

def get_twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.secure = True
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)

def tweet(api, name, city, images):
    text = name + TEMPLATE + '\n' + 'https://www.google.ru/maps/place/улица+%s+%s' % (name, city.replace(' ', '+'))
    api.update_status(status = text)

if __name__ == '__main__':
    api = get_twitter_api()

    while True:
        now = datetime.datetime.now()
        nxt = None
        for twtime in TIME:
            tm = datetime.datetime.now()
            tm = tm.replace(hour = twtime, minute = random.randint(0, 59), second = 0)
            while tm <= now:
                tm = tm + datetime.timedelta(1)
            if nxt:
                nxt = min(nxt, tm)
            else:
                nxt = tm
        print('Waiting till ', nxt)
        time.sleep((nxt - now).total_seconds())
        db = sqlite3.connect(DBFILE)
        name, city = get_street(db, True)
        print(name + TEMPLATE)
        tweet(api, name, city, None)
        db.close()
