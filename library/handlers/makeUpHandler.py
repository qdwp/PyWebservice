# coding=utf-8
import requests
from bs4 import BeautifulSoup
from flask import jsonify, json

__author__ = 'qi'


class MakeUp:
    def __init__(self, config):
        self.config = config
        # 检查必填配置项
        if self.config.get('cookies') is None:
            raise Exception('Config \"cookies\" is required.')
        if self.config.get('url') is None:
            raise Exception('Config \"url\" is required.')
        if self.config.get('xnd') is None:
            raise Exception('Config \"xnd\" is required.')
        if self.config.get('xqd') is None:
            raise Exception('Config \"xqd\" is required.')
        # 检查必填配置 END
        return

    def get_param(self):
        try:
            url = self.config.get('url')
            cookies = self.config.get('cookies')
            view = requests.get(url, cookies=cookies)
            soup = BeautifulSoup(view.text)

            eventtarget = soup.find('input', attrs={'name': '__EVENTTARGET'}).get('value')
            eventargument = soup.find('input', attrs={'name': '__EVENTARGUMENT'}).get('value')
            viewstate = soup.find('input', attrs={'name': '__VIEWSTATE'}).get('value')
            value = {
                '__EVENTTARGET': eventtarget,
                '__EVENTARGUMENT': eventargument,
                '__VIEWSTATE': viewstate
            }
            return value

        except:
            return None

    def get_info(self, param):
        try:
            makeup_info = []
            url = self.config.get('url')
            cookies = self.config.get('cookies')
            data = {
                '__EVENTTARGET': param.get('__EVENTTARGET'),
                '__EVENTARGUMENT': param.get('__EVENTARGUMENT'),
                '__VIEWSTATE': param.get('__VIEWSTATE'),
                'xnd': self.config.get('xnd'),
                'xqd': self.config.get('xqd')
            }
            res = None
            if self.is_last() is True:
                res = requests.get(url, cookies=cookies)
            else:
                res = requests.post(url, data=data, cookies=cookies)
            soup = BeautifulSoup(res.text)
            datelist = soup.find('table', attrs={'class': 'datelist', 'id': 'DataGrid1'})
            data_tr_coll = datelist.find_all('tr')
            for i in range(1, data_tr_coll.__len__()):
                try:
                    data_tr = data_tr_coll[i]
                    data_td_coll = data_tr.findAll('td')
                    xkkh = data_td_coll[0].text
                    kcmc = data_td_coll[1].text
                    xm = data_td_coll[2].text
                    kssj = data_td_coll[3].text
                    ksdd = data_td_coll[4].text
                    zwh = data_td_coll[5].text
                    ksxs = data_td_coll[6].text
                    model = {
                        'xkkh': xkkh,
                        'kcmc': kcmc,
                        'xm': xm,
                        'kssj': kssj,
                        'ksdd': ksdd,
                        'zwh': zwh,
                        'ksxs': ksxs
                    }
                    makeup_info.append(model)
                except Exception, ex:
                    continue
            # print json.dumps({'success': True, 'scoreInfo': makeup_info})
            return json.dumps({'success': True, 'makeup': makeup_info})
        except Exception, ex:
            return None

    def is_last(self):
        try:
            url = self.config.get('url')
            cookies = self.config.get('cookies')
            xnd = self.config.get('xnd')
            xqd = self.config.get('xqd')
            r = requests.get(url, cookies=cookies)
            soup = BeautifulSoup(r.text)
            data_list = soup.find_all('option', attrs={'selected': 'selected'})
            xn = data_list[0].get('value')
            xq = data_list[1].get('value')
            if xnd == xn and xqd == xq:
                return True
            else:
                return False

        except Exception, ex:
            return False
