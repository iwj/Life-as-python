# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-04-11
# Author: wujian
# E-mail: yupwj@qq.com


import tornado.web
import requests
import json


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        return self.get_secure_cookie("user")

class T_MainHandler(BaseHandler):
    """
    管理员登录
    """
    def get(self,):
        if not self.current_user:
            self.redirect("/")
        else:
            self.render("tmain.html")


class T_AccountHandler(BaseHandler):
    """
    管理员个人中心
    """
    def get(self,):
        if not self.current_user:
            self.redirect("/")
        else:
            self.write("个人中心页面")
        
class T_StudentHandler(BaseHandler):
    """
    管理学生
    状态码
    1   返回正确的学生数据
    -1  未查询到数据，没有数据返回
    """
    def get(self,):
        sql = "select * from user;"
        ret = self.db.query(sql)
        if ret:
            self.render(
                    "tstudent.html",
                    status_code = 1,
                    students = ret,
                    )
        else:
            self.render(
                    "tstudent.html",
                    status_code = -1
                    )

class T_LessonHandler(BaseHandler):
    """
    管理课程
    """
    @tornado.web.authenticated
    def get(self,):
        teachername = self.current_user
        sql_teacherid = "select * from tuser where username='"+teachername+"'"
        ret_teacherid = self.db.query(sql_teacherid)
        if ret_teacherid:
            teacherid = ret_teacherid[0]['id']
            if teacherid:
                sql_all_lesson = "select * from lesson where teacherid"+\
                        "='"+str(teacherid)+"'"
                ret_all_lesson = self.db.query(sql_all_lesson)
                if ret_all_lesson:
                    self.render(
                            "tlesson.html",
                            arg = ret_all_lesson,
                            )
                else:
#TODO
                    self.render(
                            "tlesson.html",
                            arg = False,
                            )
            else:
#TODO
                print "Error: teacher id"
        else:
#TODO
            print "Teacher id Query failed"

class T_AddHandler(BaseHandler):
    """
    添加课程
    """
    def get(self,):
        self.render(
                "tadd.html"
                )

    def post(self,):
        name = self.get_argument("name")
        cnname = self.get_argument("cnname")
        coverurl = self.get_argument("coverurl")
        sql = "insert into lesson(name, cnname, teacherid, coverurl)"
        teacherid = 1;
        sql += "values('"+name+"','"+cnname+"','"+str(teacherid)+\
                "','"+coverurl+"')";
        ret = self.db.execute(sql)
        if ret:
#TODO
            self.redirect("/tlesson")
        else:
#TODO
            self.redirect("/tadd")

class T_ShowHandler(BaseHandler):
    """
    展示课程详细信息
    状态码
    0   默认加载页面
    1   获取到课程信息、节次信息
    -1  仅仅获取到课程信息，但是该课程尚未添加任何节次
    -100课程有误

    2   添加节次操作完成
    -2  错误，添加节次失败
    """
    def get(self,):
        lesson_id = self.get_argument("lesson_id", 10000)
        sql_class = "select * from class where lesson_id="+str(lesson_id)
        ret_class = self.db.query(sql_class)
        sql_lesson = "select * from lesson where id="+str(lesson_id)
        ret_lesson = self.db.query(sql_lesson)
        if ret_class and ret_lesson:
            self.render(
                    "tshow.html",
                    arg_class = ret_class,
                    arg_lesson = ret_lesson,
                    status_code = 1,
                    )
        elif ret_lesson:
            self.render(
                    "tshow.html",
                    arg_class = None,
                    arg_lesson = ret_lesson,
                    status_code = -1,
                    )
        else:
            self.render(
                    "tshow.html",
                    arg_class = None,
                    arg_lesson = None,
                    status_code = -100,
                    )

    def post(self,):
        lesson_id = self.get_argument("lessonid")
        class_title = self.get_argument("title")
        class_info = self.get_argument("info")
        class_url = self.get_argument("url")
        class_tag = self.get_argument("tag")
        sql = "insert into class(lesson_id, title, info, url, tag)"
        sql += " values('"+lesson_id+"','"+class_title+"','"+class_info+\
                "','"+class_url+"','"+class_tag+"')"
        ret = self.db.execute(sql)
        if ret:
            self.redirect("/tshow?lesson_id="+lesson_id)
        else:
#TODO
            self.write("添加本节次课程失败")

class T_LogoutHandler(BaseHandler):
    """
    退出登录
    """
    def get(self,):
        if(self.get_argument("action", None)):
            self.clear_cookie("user")
            self.redirect("/")

class T_LoginHandler(BaseHandler):
    """
    登录/首页

    状态码
    0   默认状态，首次渲染登录页面
    """
    def get(self,):
        if self.current_user:
            self.redirect("/tmain")
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
            self.set_secure_cookie("user", ret[0]["username"])
            self.redirect(self.get_argument("next", "/tmain"))

