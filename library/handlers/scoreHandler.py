# coding=utf-8
import requests
from bs4 import BeautifulSoup
from flask import jsonify, json

__author__ = 'qi'


class Score:
    def __init__(self, config):
        self.config = config
        # 检查必填配置项
        if self.config.get('username') is None:
            raise Exception('Config \"username\" is required.')
        if self.config.get('userid') is None:
            raise Exception('Config \"userid\" is required.')
        if self.config.get('url') is None:
            raise Exception('Config \"url\" is required.')
        # 检查必填配置 END
        return

    def get_param(self):
        try:
            url = self.config.get('url')
            username = self.config.get('username')
            userid = self.config.get('userid')

            view = requests.get(url)
            soup = BeautifulSoup(view.text)

            input_tag_1 = soup.find('input', attrs={'name': '__VIEWSTATE'}).get('value')
            input_tag_2 = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'}).get('value')
            input_tag_3 = soup.find('input', attrs={'name': '__EVENTVALIDATION'}).get('value')
            value = {
                '_VIEWSTATE': input_tag_1,
                '_VIEWSTATEGENERATOR': input_tag_2,
                '_EVENTVALIDATION': input_tag_3
            }
            return value

        except:
            return None

    def get_info(self, param):
        try:
            score_info = []
            url = self.config.get('url')
            data = {
                'TextBox1': self.config.get('username'),
                'TextBox2': self.config.get('userid'),
                'drop_xn': self.config.get('drop_xn'),
                'drop_xq': self.config.get('drop_xq'),
                'drop_type': self.config.get('drop_type'),
                'Button_cjcx': self.config.get('button_cjcx'),
                'hid_dqszj': self.config.get('hid_dqszj'),
                '__VIEWSTATE': param.get('_VIEWSTATE'),
                '__VIEWSTATEGENERATOR': param.get('_VIEWSTATEGENERATOR'),
                '__EVENTVALIDATION': param.get('_EVENTVALIDATION')
            }
            res = requests.post(url, data=data)
            soup = BeautifulSoup(res.text)
            data_tr_coll = soup.find_all('tr', attrs={'align': 'left', 'onmouseout': 'this.style.backgroundColor=c'})
            for i in range(0, data_tr_coll.__len__()):
                try:
                    data_tr = data_tr_coll[i]
                    data_td_coll = data_tr.findAll('td')
                    xn = data_td_coll[0].text
                    xq = data_td_coll[1].text
                    kcm = data_td_coll[3].text
                    xf = data_td_coll[4].text
                    kcsx = data_td_coll[5].text
                    jsxm = data_td_coll[7].text
                    zpcj = data_td_coll[8].text
                    qmcj = data_td_coll[10].text
                    pscj = data_td_coll[11].text
                    bkcj = data_td_coll[13].text
                    model = {
                        'xn': xn,
                        'xq': xq,
                        'kcm': kcm,
                        'xf': xf,
                        'kcsx': kcsx,
                        'jsxm': jsxm,
                        'zpcj': zpcj,
                        'qmcj': qmcj,
                        'pscj': pscj,
                        'bkcj': bkcj
                    }
                    score_info.append(model)
                except Exception, ex:
                    continue
            # print json.dumps({'success': True, 'scoreInfo': score_info})
            return json.dumps({'success': True, 'score': score_info})
        except Exception, ex:
            return None
