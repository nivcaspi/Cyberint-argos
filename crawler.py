import re
from bs4 import BeautifulSoup
import cookielib
import urllib
import urllib2
from captcha4 import captcha_to_string
import pickle
import pdb


class Crawler():

    def __init__(self):
        # init
        self.login_url = '''http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/login.php'''
        self.captcha_url = '''http://54.69.105.130/simple-php-captcha.php?_CAPTCHA&t=0.76120300+1419259319'''
        self.index_url = '''http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/index.php?op=solvejschl'''
        self.headers = {'input-username': 'argos5652',
                        'input-password': 'ghgsl3lsf@'}
        self.url_data = None
        cookies = cookielib.CookieJar()

        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(cookies))

    def resolve_captcha(self):
        # reslove captcha
        res_dict = pickle.load(open('res_dict.p', 'rb'))
        key = 'some string not from captcha'
        print 'resolving captcha'
        while key not in res_dict:
            response = self.opener.open(self.login_url)
            f = self.opener.open(self.captcha_url)
            img = f.read()
            open('out.png', 'wb').write(img)
            key = captcha_to_string('out.png')

        captcha_str = res_dict[key]

        self.headers['input-captcha'] = captcha_str
        self.url_data = urllib.urlencode(self.headers)

    def resolve_ddos(self):
        # resolve DDOS
        result = None
        print 'resloving DDOS prevention'
        while result is None:
            response = self.opener.open(self.login_url, self.url_data)
            the_page = response.read()

            challenge = re.search('val(.+?)Challenge', the_page)
            if challenge:
                found = challenge.group(1)
                found = found[1:-6]
                result = int(found[0:found.index('+')]) + int(found[found.index('+')+1:found.index('*')]) * int(found[found.index('*')+1:])

        self.headers['jschl_answer'] = result
        self.url_data = urllib.urlencode(self.headers)

    def crawl(self):
        # crawl
        self.response = self.opener.open(self.index_url, self.url_data)
        the_page = self.response.read()
        self.soup = BeautifulSoup(''.join(the_page), 'lxml')
        self.posts = self.soup.findAll('a', style="min-height:120px;")
        url = 'http://54.69.105.130/36e294b1d0dbe06a0cf626221ed54fc0/'

        def refresh_page():
            print 'refreshing posts page'
            self.response = self.opener.open(url, self.url_data)
            self.soup = BeautifulSoup(''.join(self.response.read()), 'lxml')
            self.posts = self.soup.findAll('a', style="min-height:120px;")

        # keep track of reported posts
        posts_list = []
        print
        print '''crawling. new cyberint links and mails will print below, please wait. Ctrl-c to stop'''
        print
        # keep crawling until Ctrl-C
        while(True):
            p = self.posts[0]

            for po in self.posts:
                preview = po.contents[8].string
                if [w for w in preview.split(" ") if 'cyberint' in w.lower()]:
                    p = po

            href = p['href'] if p['href'] != '#' else p['onclick'][15:-1]
            self.response = self.opener.open(url+href, self.url_data)
            self.soup = BeautifulSoup(''.join(self.response.read()), 'lxml')
            link = url + href
            post = self.soup.find('p').string
            author_and_time = p.contents[4].string
            preview = p.contents[8].string
            if preview in posts_list:
                refresh_page()
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
                refresh_page()

# run or run tests
if __name__ == "__main__":
    crawler = Crawler()
    crawler.resolve_captcha()
    crawler.resolve_ddos()
    crawler.crawl()
