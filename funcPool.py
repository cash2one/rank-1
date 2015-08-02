#encoding:utf-8
'''
author: Harry Wong
time: 2015/7/31
email: huangyangyu@baidu.com
'''
import sys

def f1(x):
    return x ** 2.0

class funcPool:

    @staticmethod
    def f2(x):
        return x ** 0.5

def test():
    print f1(2)
    print funcPool.f2(4)

if __name__ == "__main__":
    test()
