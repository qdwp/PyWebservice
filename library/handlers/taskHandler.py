# coding = utf-8
import requests
from bs4 import BeautifulSoup
from flask import jsonify, json

__author__ = 'qi'


class Task:
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
            url = self.config.get('url')
            cookies = self.config.get('cookies')
            data = {
                '__EVENTTARGET': param.get('__EVENTTARGET'),
                '__EVENTARGUMENT': param.get('__EVENTARGUMENT'),
                '__VIEWSTATE': param.get('__VIEWSTATE'),
                'xnd': self.config.get('xnd'),
                'xqd': self.config.get('xqd')
            }
            result = None
            if self.is_last() is True:
                result = requests.get(url, cookies=cookies)
            else:
                result = requests.post(url, data=data, cookies=cookies)
            res = result.text.replace('&nbsp;', '')
            soup = BeautifulSoup(res)
            table = soup.find('table', attrs={'id': 'DataGrid1'})
            data_tr_coll = table.findAll('tr')
            content = []
            for i in range(1, data_tr_coll.__len__(), 1):
                data_tr = data_tr_coll[i]
                tds = data_tr.findAll('td')
                value = {
                    'xkkh': tds[0].text,  # 选课课号
                    'kcmc': tds[1].text,  # 课程名称
                    'kssj': tds[3].text,  # 考试时间
                    'ksdd': tds[4].text,  # 课程地点
                    'ksxs': tds[5].text,  # 课程形式
                    'zwh': tds[6].text,  # 座位号
                    'xq': tds[7].text  # 校区
                }
                content.append(value)
            # json.dumps(data) 比 jsonify(data) 所占内存较少
            # return jsonify({'success': True, 'taskInfo': content})
            return json.dumps({'success': True, 'task': content})

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
