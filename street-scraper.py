import re
import requests
import sqlite3

from bs4 import BeautifulSoup

CITIES = [
        ('moscow', 'Москва'),
        ('nnovgorod', 'Нижний Новгород'),
        ('spb', 'Санкт-Петербург'),
        ('petrozavodsk', 'Петрозаводск'),
        ('omsk', 'Омск'),
        ('novosibirsk', 'Новосибирск')
        ]
DBFILE = 'streets-city.db'


for city_en, city_ru in CITIES:
    URL = 'http://www.street-viewer.ru/%s/street/' % city_en
    page = 1
    db = sqlite3.connect(DBFILE)
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS streets (name TEXT, city TEXT, used INT)')
    db.commit()
    while True:
        r = requests.get(URL + str(page))
        soup = BeautifulSoup(r.text, 'html.parser')
        for lst in soup.find_all('ul'):
            for street in lst.find_all('li'):
                ref = street.find(u'a')
                href = ref.attrs['href']
                name = ref.get_text(strip = True)
                if not re.match('\w*ая улица$', name):
                    continue
                name = name.split()[0]
                print(name, city_ru)
                cur.execute('INSERT INTO streets VALUES (?, ?, ?)', (name, city_ru, 0))
        db.commit()
        pagebar = soup.find('table', {'width' : '100%'}).find('div')
        pages = int(pagebar.find_all(u'a')[-1].get_text(strip = True))
        page += 1
        if page > pages:
            break
    db.close()
