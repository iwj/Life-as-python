# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-04-20
# Author: wujian
# E-mail: yupwj@qq.com


import tornado.web
import views


class T_LoginHandler(views.BaseHandler):
    """
    管理员登录

    状态码
    0   首次进入登录页面（默认状态）
    """
    def get(self,):
        if self.current_user:
            self.redirect("/tensor")
        else:
            self.render("tlogin.html", status_code=0)
    def post(self,):
        get_username = self.get_argument("t_username")
        get_password = self.get_argument("t_password")
        sql = "select * from tuser where username=%s and password=%s"
        ret = self.db.query(sql, get_username, get_password)
        if not ret:
            self.write("登录失败")
        else:
            self.render("tindex.html",arg="登录成功")

class T_IndexHandler(views.BaseHandler):
    def get(self,):
        self.render("tindex.html")

