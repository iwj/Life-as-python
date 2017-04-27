# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-03-18
# Author: wujian
# E-mail: yupwj@qq.com


import tornado.web
import requests
import json
import time
import bing

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render("login.html", info="")
        else:
            self.redirect("/");

    def post(self):
        get_username = self.get_argument("username")
        get_password = self.get_argument("password")
        sql = "select * from user where username=%s and password=%s"
        ret = self.db.query(sql, get_username, get_password)
        if not ret:
            self.render("login.html", info="用户名或密码错误")
        else:
            self.set_secure_cookie("user", ret[0]["username"])
            self.set_secure_cookie("nickname", ret[0]["nickname"])
            self.redirect(self.get_argument('next', '/'))

class LogoutHandler(BaseHandler):
    def get(self):
        if(self.get_argument("action", None)):
            self.clear_cookie("user")
            self.redirect("/")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")

class IndexHandler(BaseHandler):
    def get(self):
        bing_img = bing.get_bing_img()
        if bing_img:
            self.render("index.html", bing = bing_img)
        else:
            self.render("index.html", bing = None)

class EditHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render(
                "edit.html",
                info="",
                )

    def post(self):
        title = self.get_argument("title")
        author = self.current_user.decode("utf-8")
        text = self.get_argument("text")
        tag = self.get_argument("tag")
        fields = "title, author, text, posttime, tag"
        values = "'%s','%s','%s',CURTIME(),'%s'" % (title ,author,'text','tag')
        sql = "insert into post(%s) values(%s);" % (fields,values)
        ret = self.db.execute(sql)
        if ret:
            self.redirect("/")
        else:#TODO
            self.redirect("/")

class ReadHandler(BaseHandler):
    def get(self,):
        id = self.get_argument("id", 1000)
        sql = "select * from post where id="+str(id)
        ret = self.db.query(sql)
        error_ret = {
                "title":"未找到",
                "posttime":"",
                "author":"",
                "text":"<p>请检查网址是否有误</p><p>或者尝试搜索</p>",
                "tag":""
                }
        if(ret):
            self.render("read.html", arg = ret[0])
        else:
            self.render("read.html",arg = error_ret)



class HelpHandler(BaseHandler):
    def get(self,):
        self.render("help.html")

class AccountHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,):
        sql = "select * from user where username='"+str(self.current_user)+"'"
        ret = self.db.query(sql)
        if(ret):
            self.render("account.html", arg = ret[0])


class SearchHandler(BaseHandler):
    def get(self,):
        self.render("search.html")

    def post(self,):
        time_start = time.time()
        kw = self.get_argument("q")
        sql = "select * from post where title like '%%"+kw+"%%'"
        sql += "or text like'%%" +kw+ "%%'"
        ret = self.db.query(sql)
        time_end = time.time()
        time_spend = time_end - time_start
        if ret:
            self.render("result.html",arg=ret, time = time_spend)
        else:
            ret = False
            self.render("result.html",arg=ret, time = time_spend)


class StudyHandler(BaseHandler):
    def get(self,):
        id = self.get_argument("id", 1)
#TODO 若课程编号有误，跳转
        sql = "select * from math where id=" + str(id) 
        ret = self.db.query(sql)
        if(ret):
            self.render("study.html", arg=ret[0])
        else:
            self.write("未找到课程")

        

class DiscoverHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,):
        sql_math = "select * from math order by id desc limit 5;"
        ret_math = self.db.query(sql_math)
        self.render("discover.html", arg_math = ret_math)


class FinanceHandler(BaseHandler):
    def get(self,):
        wacai_url = "http://bbs.wacai.com/forum.php?gid=16065"
        ret = requests.get(wacai_url).text
        self.render("finance.html", arg = ret)

