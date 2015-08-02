#encoding:utf-8
'''
author: Harry Wong
time: 2015/7/31
email: huangyangyu@baidu.com
'''
import sys
import time
from pymongo import MongoClient
from dyLoad import dyLoad
import tool

class rankData:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def dictlizeData(self, input, prefix = ""):
        output = {}
        for key in input:
            value = input[key]
            if isinstance(value, int):
                output[prefix+key] = value
            if isinstance(value, dict):
                output.update(self.dictlizeData(value, key+"#"))
            else:
                try:#?
                    value = float(value)
                except:
                    pass
                output[prefix+key] = value
        return output

    def compute(self, conf, input):
        if conf == None or input == None:
            return None
        '''
        获取配置文件参数
        '''
        module = conf["func_module"]
        beta = conf["beta"]
        fields = conf["fields"]
        alpha = conf["alpha"]
        funcs = conf["funcs"]
        '''
        计算排名
        '''
        output = []
        for data in input:
            data = self.dictlizeData(data)
            rank = 0
            scores = []
            for i in xrange(len(beta)):#因子数
                scores.append(0)
                for j in xrange(len(fields)):#字段数
                    #print data[fields[j]]
                    scores[i] += alpha[i][j] * dyLoad.call_func(module, funcs[i][j], data[fields[j]])
                rank += beta[i] * scores[i]
            output.append({"time": int(time.time()),"rank": rank, "scores": scores})
        return output

    def readConf(self, file_name, cut = "::"):
        try:
            conf = {"beta": [], "fields": [], "alpha": [], "funcs": []}
            with open(file_name) as file:
                for line in file:
                    params = line.split("#")[0].strip().split(cut)
                    if len(params) == 2:
                        if params[0] == "score":
                            conf["beta"].append(float(params[1]))
                            conf["alpha"].append([])
                            conf["funcs"].append([])
                        else:
                            conf[params[0]] = params[1]
                    elif len(params) == 3:
                        if len(conf["beta"]) == 1:
                            conf["fields"].append(params[0])
                        conf["alpha"][-1].append(float(params[1]))
                        conf["funcs"][-1].append(params[2])
                    elif len(params) == 1:
                        continue
                    else:
                        return None
            return conf
        except Exception, e:
            print tool.get_cur_info(), e
            return None

    def writeConf(self, file_name, output):
        return None

    def readDB(self, conf):
        try:
            client = MongoClient(conf["url"])
            tb = client[conf["db_name"]]["ceylon"]
            datas = []
            for data in tb.find():
                if len(datas) == 1:
                    break
                datas.append(data)
            client.close()
            return datas
        except Exception, e:
            print tool.get_cur_info(), e
            return None

    def writeDB(self, conf, datas):
        try:
            client = MongoClient(conf["url"])
            tb = client[conf["db_name"]][conf["tb_name"]]
            for key in datas[0]:
                tb.ensure_index(key, backgroud=True)
            for data in datas:
                tb.save(data)
            client.close()
            return True
        except Exception, e:
            print tool.get_cur_info(), e
            return False

def test():
    try:
        rank = rankData()
        conf = rank.readConf("./conf/setting.txt")
        input = rank.readDB(conf)
        #input = {"name": 2, "city": 4}
        #print input
        output = rank.compute(conf, input)
        #print output
        rank.writeDB(conf, output)
    except Exception, e:
        print tool.get_cur_info(), e

if __name__ == "__main__":
    test()
