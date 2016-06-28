import re
from bs4 import BeautifulSoup
import cookielib
import urllib
import urllib2
from captcha4 import captcha_to_string
import pickle
import pdb
# init
cookies = cookielib.CookieJar()

opener = urllib2.build_opener(
    urllib2.HTTPRedirectHandler(),
    urllib2.HTTPHandler(debuglevel=0),
    urllib2.HTTPSHandler(debuglevel=0),
    urllib2.HTTPCookieProcessor(cookies))
# reslove captcha
res_dict = pickle.load(open('res_dict.p', 'rb'))
key = 'some string not from captcha'
print 'resolving captcha'
while key not in res_dict:
    login_url = 'http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/login.php'
    response = opener.open(login_url)
    captcha_url = "http://54.69.105.130/simple-php-captcha.php?_CAPTCHA&t=0.76120300+1419259319"
    f = opener.open(captcha_url)
    img = f.read()
    open('out.png', 'wb').write(img)
    key = captcha_to_string('out.png')

captcha_str = res_dict[key]

values = {  'input-username' : 'argos5652',
            'input-password' : 'ghgsl3lsf@',
            'input-captcha' : captcha_str}
data = urllib.urlencode(values)
# resolve DDOS
result = None
print 'resloving DDOS prevention'
while result == None:
    response = opener.open(login_url, data)
    the_page = response.read()

    m = re.search('val(.+?)Challenge', the_page)
    if m:
        found = m.group(1)
        found = found[1:-6]
        result = int(found[0:found.index('+')]) + int(found[found.index('+')+1:found.index('*')]) * int(found[found.index('*')+1:])

values['jschl_answer'] = result
data = urllib.urlencode(values)
# crawl
index_url = 'http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/index.php?op=solvejschl'
response = opener.open(index_url, data)
the_page = response.read()
soup = BeautifulSoup(''.join(the_page), 'lxml')
posts = soup.findAll('a', style="min-height:120px;")
# keep track of reported posts
posts_list = []
print
print 'crawling. new cyberint links and mails will print below, please wait'
print
# keep crawling until Ctrl-C
while(True):
    print 'refreshing posts page'
    p = posts[0]

    for po in posts:
        preview = po.contents[8].string
        if [w for w in preview.split(" ") if 'cyberint' in w.lower()]:
            p = po

    url = 'http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/'
    href = p['href'] if p['href'] != '#' else p['onclick'][15:-1]
    response = opener.open(url+href, data)
    soup = BeautifulSoup(''.join(response.read()), 'lxml')
    link = url + href
    post = soup.find('p').string
    author_and_time = p.contents[4].string
    preview = p.contents[8].string
    if preview in posts_list:
        response = opener.open(url, data)
        soup = BeautifulSoup(''.join(response.read()), 'lxml')
        posts = soup.findAll('a', style="min-height:120px;")
    else:
        posts_list.append(preview)
        links = [w for w in post.split(" ") if 'cyberint' in w.lower()]
        if links:
            print
            print 'new Cyberint links or emails found:'
            for l in links:
                print l
            print author_and_time
            print post
            print link
            print
        response = opener.open(url, data)
        soup = BeautifulSoup(''.join(response.read()), 'lxml')
        posts = soup.findAll('a', style="min-height:120px;")

