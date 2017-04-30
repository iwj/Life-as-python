# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-04-23
# Author: wujian
# E-mail: yupwj@qq.com

import bs4
import requests
import json
import spider

def get_bing_img():
    bing_json = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc\
    =1444634662901&pid=hp"
    result = spider.get_source(bing_json)
    if result:
        try:
            result_dict = json.loads(result)
        except Exception, e:
            print e
            return False
    else:
        result_dict = None
    if result_dict:
        img_url = result_dict.get("images")[0].get("url")
        img_url = "http://cn.bing.com" + img_url
        file_name = img_url.split("/")[-1]
    else:
        img_url = None
    if img_url:
        return img_url
    else:
        return "http://cn.bing.com/az/hprichbg/rb/MirrorBeach_ZH-CN12835554220\
                _1920x1080.jpg"
