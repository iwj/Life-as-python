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
    -3  已经有用户登录
    """
    def get(self):
        if self.current_user:
            #self.render("register.html", status_code=-3)
            self.redirect("/account")
        else:
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
                self.write("注册失败")


class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class AddlessonHandler(BaseHandler):
    def post(self,):
        lesson_id = self.get_argument("lesson_id")

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

class AddHandler(BaseHandler):
    def get(self,):
        sql_all = "select id from lesson"
        ret_all = self.db.query(sql_all)

        username = str(self.current_user)
        sql_userid = "select id from user where username='"+username+"'"
        ret_userid = self.db.query(sql_userid)
        user_id_origin = ret_userid[0]['id']
        #print user_id_origin
        if ret_userid:
            sql_added = "select lessonid from record where userid='"+\
                    str(user_id_origin)+"'"
            ret_added = self.db.query(sql_added)
        else:
            self.write("用户ID未找到，请联系管理员")

        #print ret_all
        #print ret_added

        list_all = []
        list_added = []
        list_notadded = []

        for i in ret_all:
            list_all.append(int(i['id']))
        for j in ret_added:
            list_added.append(int(j['lessonid']))

        for i in list_all:
            if not (i in list_added):
                list_notadded.append(i)

        #print list_all
        #print list_added
        #print list_notadded

        sql = "select * from lesson"
        ret = self.db.query(sql)
        if ret:
            self.render(
                    "addlesson.html",
                    arg_lesson = ret,
                    arg_added_list = list_added,
                    user_id = user_id_origin,
                    )
        else:
            self.render(
                    "addlesson.html",
                    arg_lseeon = None,
                    )

    def post(self,):
        user_id = self.get_argument("user_id")
        lesson_id = self.get_argument("lesson_id")
        sql_insert_record = "insert into record(userid, lessonid, add_date)"+\
                " values(" + user_id + "," + lesson_id + ", now())"

        ret = self.db.execute(sql_insert_record)
        if ret:
            self.redirect("/addlesson")
        else:
            self.redirect("/addlesson")

class RemoveHandler(BaseHandler):
    def post(self,):
        user_id = self.get_argument("user_id")
        lesson_id = self.get_argument("lesson_id")
        sql_remove_record = "delete from record where "+\
                "userid="+user_id+" and lessonid="+lesson_id
        #print sql_remove_record
        ret = self.db.execute(sql_remove_record)
        print str(ret)
        if not ret:
            self.redirect("/addlesson")
        else:
            self.redirect("/addlesson")

class HelpHandler(BaseHandler):
    def get(self,):
        self.render("help.html")

class AccountHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,):
        lesson_info_flag = True
        sql_user = "select * from user where username='"+\
                str(self.current_user)+"'"
        ret_user = self.db.query(sql_user)

        sql_lesson_id = "select lessonid from record where userid="+\
                str(ret_user[0]['id'])+""
        ret_lesson_id = self.db.query(sql_lesson_id)
        
        list_add = []
        for i in ret_lesson_id:
            list_add.append(i['lessonid'])

        
        sql_all = "select * from lesson"
        ret_all = self.db.query(sql_all)

        if(ret_user and ret_lesson_id and ret_all):
            self.render(
                    "account.html",
                    arg_user = ret_user[0],
                    arg_added_list = list_add,
                    arg_lesson = ret_all,
                    lesson_info_flag = lesson_info_flag,
                    )
        else:
            self.render(
                    "account.html",
                    arg_user = ret_user[0],
                    arg_added_list = None,
                    arg_lesson = ret_all,
                    lesson_info_flag = lesson_info_flag,
                    )
            self.write("Erroe: Query user info faild.")


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
        sql = "select * from class where id=" + str(id) 
        ret_main_lesson = self.db.query(sql)
        sql = "select * from class order by id desc limit 10;"
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


class LessonHandler(BaseHandler):
    """
    课程专属页
    状态码：
    0   默认状态
    1   课程信息、课程节次信息均查询到
    2   只有课程信息、尚未添加课程节次
    -1  错误，数据源有误
    """
    def get(self,):
        lesson_id = self.get_argument("lesson_id", 10000)
        sql_lesson = "select * from lesson where id="+str(lesson_id)
        ret_lesson = self.db.query(sql_lesson)
        sql_class = "select * from class where lesson_id="+str(lesson_id)
        ret_class = self.db.query(sql_class)
        if ret_lesson and ret_class:
            self.render(
                    "lesson.html",
                    lesson_info = ret_lesson,
                    class_info = ret_class,
                    status_code = 1,
                    )
        elif ret_lesson:
            self.render(
                    "lesson.html",
                    lesson_info = ret_lesson,
                    status_code = 2,
                    )
        else:
#TODO
            self.render("lesson.html", status_code = -1)

class ErrorHandler(BaseHandler):
    def get(self):
        self.render("error.html", error_code=1)
        

class DiscoverHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,):
        sql_random = "select * from class order by id desc limit 10"
        ret_random = self.db.query(sql_random)
        sql_lesson = "select * from lesson order by id desc limit 50;"
        ret_lesson = self.db.query(sql_lesson)
        if ret_random and ret_lesson:
            self.render(
                    "discover.html",
                    arg_lesson = ret_lesson,
                    arg_random = ret_random,
                    )
        else:
            self.write("ERROR, please contact the administrator.")


class FinanceHandler(BaseHandler):
    def get(self,):
        origin_url = "http://"
        pass

