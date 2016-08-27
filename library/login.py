# coding=utf-8
import requests
import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

__author__ = 'qi'


class Login:
    def __init__(self):
        return

    @staticmethod
    def login(username, password):
        loginURL = "http://211.70.149.135:88/Default3.aspx"
        try:
            # Load login page ，to get information: __VIEWSTATE
            view = requests.get(loginURL)
            soup = BeautifulSoup(view.text)

            input_tag = soup.find('input', attrs={'name': '__VIEWSTATE'})
            _view = input_tag.get('value')
        except:
            return (None, '0')
        try:
            # to make postData
            # page = urllib2.urlopen(loginURL).read()
            postdata = urllib.urlencode({'__VIEWSTATE': _view})
            postdata += '&Button1=+%B5%C7+%C2%BC+&ddl_js=%D1%A7%C9%FA&TextBox1='
            postdata += username
            postdata += '&TextBox2=' + password

            # to make headers
            temp = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                   'Chrome/41.0.2272.76 Safari/537.36'
            headers = {
                'User-Agent': temp
            }
            # cookie valid is login or not
            cookie = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            myRequest = urllib2.Request(loginURL, postdata, headers)
            loginPage = opener.open(myRequest).read()
            page = unicode(loginPage, 'gb2312').encode("utf-8")  # get the cookie
            # print page
            # while login successful
            if 'window.open' in loginPage:
                return (cookie, username)
            else:
                return (None, '0')
        except:
            return (None, '0')
