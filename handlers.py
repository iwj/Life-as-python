# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Date  : 2017-03-13
# Author: wujian
# E-mail: yupwj@qq.com


from views import *
from tviews import *

#路径映射配置

HANDLERS = [
        (r"/", IndexHandler),
        (r"/login", LoginHandler),
        (r"/edit", EditHandler), 
        (r"/help", HelpHandler),
        (r"/logout", LogoutHandler),
        (r"/reg", RegisterHandler),
        (r"/account", AccountHandler),
        (r"/search", SearchHandler),
        (r"/study", StudyHandler),
        (r"/discover", DiscoverHandler),
        (r"/finance", FinanceHandler),
        (r"/error", ErrorHandler),
        (r"/tensor/login", T_LoginHandler),
        (r"/tensor", T_IndexHandler),
        ]
