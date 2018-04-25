# -*- coding: utf-8 -*-
import urllib2
import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages')
from lxml import html
from datetime import date, timedelta

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False

t = None
q = None

try:
    queries = sys.argv[1:]
    if is_int(queries[0]):
        t = queries[0]
        q = queries[1]
    else:
        q = queries[0]
        t = queries[1]
except:
    pass

url1 = 'http://www.snuco.com/html/restaurant/restaurant_menu1.asp'
url2 = 'http://www.snuco.com/html/restaurant/restaurant_menu2.asp'
if t:
    try:
        date = (date.today() + timedelta(days=int(t))).strftime('%Y-%m-%d')
        url1 = url1+('?date=%s'%date)
        url2 = url2+('?date=%s'%date)
    except:
        pass

req1 = urllib2.Request(url1)
req2 = urllib2.Request(url2)
response1 = urllib2.urlopen(req1)
response2 = urllib2.urlopen(req2)
page1 = response1.read()
page2 = response2.read()

def print_dic(dic):
    for key, value in dic.iteritems():
        print key
        print value

items = []

for cafe in range(2):
    if cafe == 0:
        cafeterias = html.fromstring(page1).xpath("//span[@class='left_text14']")
    else:
        cafeterias = html.fromstring(page2).xpath("//span[@class='left_text14']")

    for i in range(len(cafeterias)):
        if (cafe == 1 and i in [4,5,6,8]): continue

        parent = cafeterias[i].getparent().getparent()
        cafeteria = cafeterias[i].text_content()
        breakfast = 'M:' + parent.getchildren()[2].text_content().replace('\n', '/')
        lunch = 'L:' + parent.getchildren()[4].text_content().replace('\n', '/')
        dinner = 'D:' + parent.getchildren()[6].text_content().replace('\n', '/')
        if q == 'm':
            menu = breakfast
        elif q == 'l':
            menu = lunch
        elif q == 'd':
            menu = dinner
        else:
            menu = breakfast + lunch + dinner

        items.append('<item><title>%s</title><subtitle>%s</subtitle></item>'\
                %(cafeteria, menu))


print '<items>'
for item in items:
    print item.encode('utf-8').replace('&', '&amp;')
print '</items>'

