# coding = utf-8

import requests
from flask import json

__author__ = 'qidunwei'


class Update:
    def __init__(self):
        self.file_path = "http://dunwei.top/ahutcourse/static/update.txt"

    def get_version(self):
        try:
            file_content = requests.get(self.file_path)
            info = json.loads(file_content.text)
            return info
        except Exception, ex:
            return None

    def set_version(self, version):
        pass
