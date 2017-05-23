# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-04-11
# Author: wujian
# E-mail: yupwj@qq.com


from views import *

#路径映射配置

HANDLERS = [
        (r"/", T_LoginHandler),
        (r"/tlogin", T_LoginHandler),
        (r"/tlogout", T_LogoutHandler),
        (r"/tmain", T_MainHandler),
        (r"/taccount", T_AccountHandler),
        (r"/tstudent", T_StudentHandler),
        (r"/tlesson", T_LessonHandler),
        (r"/tadd", T_AddHandler),
        (r"/tshow", T_ShowHandler),
        ]
