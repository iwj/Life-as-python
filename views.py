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
    """
    登录模块

    状态码：
    0   首次进登录页面
    1   注册成功的用户跳转过来
    -1  用户名或密码有误
    """
    def get(self):
        if not self.current_user:
            self.render("login.html", status_code = 0)
        else:
            self.redirect("/");

    def post(self):
        get_username = self.get_argument("username")
        get_password = self.get_argument("password")
        sql = "select * from user where username=%s and password=%s"
        ret = self.db.query(sql, get_username, get_password)
        if not ret:
            self.render("login.html", status_code = -1)
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
    """
    注册模块

    状态码：
    0   首次进入注册页面
    1   注册成功
    -1  邮箱已经注册过（存在）
    -2  用户名已经注册过（存在）
    """
    def get(self):
        self.render("register.html", status_code=0)
    def post(self):
        get_username = self.get_argument("username")
        get_password = self.get_argument("password")
        get_email = self.get_argument("email")
        sql_check_username = "select * from user where username = %s"
        sql_check_email = "select  * from user where email = %s"
        ret_check_username = self.db.query(sql_check_username, get_username)
        ret_check_email = self.db.query(sql_check_email, get_email)
        if ret_check_email:
            self.render(
                    "register.html",
                    status_code=-1,
                    input_username = get_username,
                    )
        elif ret_check_username:
            self.render(
                    "register.html",
                    status_code=-2,
                    input_email = get_email,
                    )
        else:
            nick_end = time.time()
            nick_end = (str(nick_end)).split(".")[0]
            sql_register = "insert into user(username, password, nickname,"+\
            " email, regtime) values('%s', '%s', '%s', '%s', now());" % \
                    (get_username, get_password, u"用户"+nick_end, get_email)
            ret_register = self.db.execute(sql_register)
            if ret_register:
                self.render("login.html", status_code = 1)
            else:
                self.write("注册失败！！！")


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
        sql = "select * from math where id=" + str(id) 
        ret_main_lesson = self.db.query(sql)
        sql = "select * from math order by id desc limit 10;"
        ret_link_lesson = self.db.query(sql)
        if(ret_main_lesson and ret_link_lesson):
            self.render(
                    "study.html",
                    arg_main=ret_main_lesson[0],
                    arg_link=ret_link_lesson,
                    status_code=1,
                    )
        else:
            self.render("study.html", status_code=0)

class ErrorHandler(BaseHandler):
    def get(self):
        self.render("error.html", error_code=1)
        

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

