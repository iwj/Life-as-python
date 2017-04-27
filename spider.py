# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-04-27
# Author: wujian
# E-mail: yupwj@qq.com

import bs4
import requests
import json

def get_source(url):
    ret = requests.get(url).text
    if ret:
        return ret
    else:
        return False
