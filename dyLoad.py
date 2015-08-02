#encoding:utf-8
'''
author: Harry Wong
time: 2015/7/31
email: huangyangyu@baidu.com
'''
import sys
import importlib

class dyLoad:

    @staticmethod
    def call_func(module_name, func_name, x):
        try:
            module_name = module_name.split('.')[0]
            m = importlib.import_module(module_name)
            f = None
            if hasattr(m, func_name):
                f = getattr(m, func_name)
            elif hasattr(m, module_name):
                c = getattr(m, module_name)
                if hasattr(c, func_name):
                    f = getattr(c, func_name)
            return f(x)
        except Exception, e:
            print tool.get_cur_info(), e
            return None

def test():
    print dyLoad.call_func("", "f1", 1)
    print dyLoad.call_func("funcPol", "f1", 2)
    print dyLoad.call_func("funcPool", "f3", 2)
    print dyLoad.call_func("funcPool.py", "f1", 2)
    print dyLoad.call_func("funcPool", "f2", 4)

if __name__ == "__main__":
    test()
