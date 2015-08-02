#encoding:utf-8
'''
author: Harry Wong
time: 2015/7/31
email: huangyangyu@baidu.com
'''
import sys

def get_cur_info():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return (f.f_code.co_name, f.f_lineno)
