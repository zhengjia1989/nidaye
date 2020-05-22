# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import *  # noqa

# 正式环境
RUN_MODE = 'PRODUCT'

# 只对正式环境日志级别进行配置，可以在这里修改
LOG_LEVEL = 'ERROR'

# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 正式环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'lanjinexam1',
            'USER': 'yangxin',
            'PASSWORD': '1',
            'HOST': '192.168.5.72',
            # 'HOST': '132.232.12.80',
            'PORT': '3306',
        },
    }
)

