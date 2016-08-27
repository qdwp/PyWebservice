# coding=utf-8
import requests
from bs4 import BeautifulSoup
from flask import jsonify, json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'qi'


class Course:
    def __init__(self, config):
        self.config = config
        # 检查必填配置项
        if self.config.get('cookies') is None:
            raise Exception('Config \"cookies\" is required.')
        if self.config.get('url') is None:
            raise Exception('Config \"url\" is required.')
        if self.config.get('pwd') is None:
            raise Exception('Config \"pwd\" is required.')
        # 检查必填配置 END
        return

    def get_courses(self):
        try:
            url = self.config.get('url')
            cookies = self.config.get('cookies')
            result = requests.get(url, cookies=cookies)
            res = result.text.replace('<br>', '*')
            soup = BeautifulSoup(res)
            table = soup.find('table', attrs={'id': 'Table1'})
            data_tr_coll = table.findAll('tr')

            student_id = soup.find('span', attrs={'id': 'Label5'}).text.split(u'：')[1]
            student_xm = soup.find('span', attrs={'id': 'Label6'}).text.split(u'：')[1]
            student_xy = soup.find('span', attrs={'id': 'Label7'}).text.split(u'：')[1]
            student_zy = soup.find('span', attrs={'id': 'Label8'}).text.split(u'：')[1]
            student_bj = soup.find('span', attrs={'id': 'Label9'}).text.split(u'：')[1]
            student = {
                'userXH': student_id,
                'userXM': student_xm,
                'userXY': student_xy,
                'userZY': student_zy,
                'userBJ': student_bj,
                'userMM': self.config.get('pwd')
            }

            content = []
            time = 0
            for i in range(2, data_tr_coll.__len__() - 3, 2):
                data_tr = data_tr_coll[i]
                tds = data_tr.findAll('td')
                value = []
                week = 0
                if tds.__len__() == 9:
                    for k in range(2, 9, 1):
                        start_time = ''
                        end_time = ''
                        place = ''
                        td = tds[k].text
                        v = td.split('*')
                        title = v[0] if (v.__len__() > 1) else ''
                        time_tag = v[1] if (v.__len__() > 1) else ''
                        teacher = v[2] if (v.__len__() > 1) else ''
                        place_temp = v[3] if (v.__len__() > 1) else ''
                        if title is '':
                            week += 1
                            continue
                        place = place_temp.replace(u'东教', '').replace(u'一', '').replace(u'东区', '')
                        # if u'阶' in place_temp:
                        #     place = place_temp.replace(u'东教一', '')
                        # else:
                        #     place = place_temp.replace(u'东', '').replace(u'一', '').replace(u'东区', '')
                        if time_tag is not '':
                            time_temp = time_tag.split('{')[1].replace(u'第', '').replace(u'周', '').replace('}', '') \
                                .replace('|2节/', '')
                            start_time = time_temp.split('-')[0]
                            end_time = time_temp.split('-')[1]
                        val = {
                            'week': week,
                            'time': time,
                            'name': title,
                            'startweek': int(start_time),
                            'endweek': int(end_time),
                            'teacher': teacher,
                            'place': place
                        }
                        week += 1
                        # value.append(val)
                        content.append(val)
                elif tds.__len__() == 8:
                    for k in range(1, 8, 1):
                        start_time = ''
                        end_time = ''
                        place = ''
                        td = tds[k].text
                        v = td.split('*')
                        title = v[0] if (v.__len__() > 1) else ''
                        time_tag = v[1] if (v.__len__() > 1) else ''
                        teacher = v[2] if (v.__len__() > 1) else ''
                        place_temp = v[3] if (v.__len__() > 1) else ''
                        if title is '':
                            week += 1
                            continue
                        place = place_temp.replace(u'东教', '').replace(u'一', '').replace(u'东区', '')
                        # if u'阶' in place_temp:
                        #     place = place_temp.replace(u'东教一', '')
                        # else:
                        #     place = place_temp.replace(u'东', '').replace(u'一', '').replace(u'东区', '')
                        if time_tag is not '':
                            time_temp = time_tag.split('{')[1].replace(u'第', '').replace(u'周', '').replace('}', '') \
                                .replace('|2节/', '')
                            start_time = time_temp.split('-')[0]
                            end_time = time_temp.split('-')[1]
                        val = {
                            'week': week,
                            'time': time,
                            'name': title,
                            'startweek': int(start_time),
                            'endweek': int(end_time),
                            'teacher': teacher,
                            'place': place
                        }
                        week += 1
                        # value.append(val)
                        content.append(val)
                time += 1
                # content.append(value)
            # return jsonify({'success': True, 'coursesInfo': content,'student':student})
            return json.dumps({'success': True, 'courses': content, 'student': student}), student

        except Exception, ex:
            return None
