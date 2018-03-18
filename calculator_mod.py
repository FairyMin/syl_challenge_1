#!/usr/bin/env python3
#coding=utf-8

import sys
import configparser
import getopt

from datetime import datetime
from multiprocessing import Process,Queue

class Config(object):
    """读取文件类"""
    def __init__(self,configfile,sb_city):
        self.cfg_file = configfile
        self._config = None
        self.get_config(sb_city)

    # 获取配置文件的内容
    def get_config(self,sb_city):
        config = configparser.ConfigParser()
        config.read(self.cfg_file)
        self._config  = config[sb_city]
    
#        with open(self.cfg_file) as file:
#            for line in file:
#                # 去掉空格
#                ss_line = line.replace(" ","")
#                s_line = ss_line.strip()
#                # 分割字符串
#                f_line = s_line.split("=",1) 
#                # 去掉空行
#                if f_line != [""]:
#                #    print(f_line)
#                    self._config[f_line[0]] = f_line[1]
        # print(self._config)
        # 返回对应的配置项            
        #return self._config[pzx]
        #queue1.put(self._config)

class UserData(object):
    """用户类，计算工资并写入指定文件"""
    def __init__(self,userdatafile,pzx):
        self.usr_file = userdatafile
        self.info_dict = pzx._config
        #self.userdata = {}
        #读取社保比例信息
        try:
            self.low = float(self.info_dict['JiShuL'])
            self.high = float(self.info_dict['JiShuH'])
            self.x_yl = float(self.info_dict['YangLao'])
            self.x_yiliao = float(self.info_dict['YiLiao'])
            self.x_shiye = float(self.info_dict['ShiYe'])
            self.x_gs = float(self.info_dict['GongShang'])
            self.x_shengyu = float(self.info_dict['ShengYu'])
            self.x_gjj = float(self.info_dict['GongJiJin']) 
            self.x_sb = (self.x_yl+self.x_shiye+self.x_gs
                    +self.x_shengyu+self.x_gjj+self.x_yiliao)
            #print(self.x_sb)
            #print(type(self.cfg_tmp.get_config('JiShuL')))
        except TypeError:
            print("type error")        
        #self.cfg_obj 用来引用配置文件的对象
        #self.cfg_obj = cfg_tmp
        #self.xx_list = []
    #计算税后工资 
    def get_info(self,queue2):
        #print("-"*10)
        userdata = {}
        #if ~queue1.empty():
        #info_dict = queue1.get()
 
        with open(self.usr_file) as file:
            for line in file:
                #print(line)
                # 去掉空格
                ss_line = line.replace(" ","")
                s_line = ss_line.strip()
                # 分割字符串
                f_line = s_line.split(",",1) 
                # 去掉空行
                if f_line != [""]:
                    #print(f_line)
                    userdata[f_line[0]] = f_line[1]

        #读取到的文件格式 －－ 工号：税前工资
        queue2.put(userdata)
        #print(self.userdata)
        #self.cal()
        #计算社保金额，个税金额，税后工资
    def write_solution(self,queue2,queue3):
        sb_dict = {}
        tax_dict = {}
        shgz_dict = {}
        if ~queue2.empty():
            u_data = queue2.get()
        xx_list = []
        for p in u_data.keys():
            #计算五险一金的基数
            try:
                u_data[p] = float(u_data[p])
                if u_data[p] < self.low:
                    j_shu = self.low
                elif u_data[p] > self.high:
                    j_shu = self.high
                else:
                    j_shu = u_data[p] 
                sb = j_shu * self.x_sb
                t = u_data[p] - sb - 3500
                if t < 0:
                    tax = 0
                elif t<=1500:
                    tax = t * 0.03
                elif t<=4500:
                    tax = t * 0.1 - 105
                elif t<=9000:
                    tax = t * 0.2 - 555
                elif t<=35000:
                    tax = t * 0.25 - 1005
                elif t<=55000:
                    tax = t * 0.3 - 2755
                elif t<=80000: 
                    tax = t * 0.35 - 5505
                else:
                    tax = t * 0.45 -13505
                # 将数据修改为2位小数的数字形式字符串
                # 并存入列表self.xx_list            
                sb_dict[p] = format(sb,'.2f')
                tax_dict[p] = format(tax,'.2f')
                mon = u_data[p] - tax - sb
                shgz_dict[p] = format(mon,'.2f')
                u_data[p] = format(u_data[p],'.0f') 
                xx_list.append([p,u_data[p],sb_dict[p],tax_dict[p],
                            shgz_dict[p]])
                queue3.put(xx_list)

            except TypeError:
                print("type error2")
                
    #将计算结果写入指定文件
    def dumptofile(self,outputfile,queue3):
        if ~queue3.empty():
            w_list = queue3.get()            
        #存储格式：工号，税前工资，社保金额，个税金额，税后工资
        with open(outputfile,'w') as file:
            for item in w_list:
                for i in item:
                    file.write(i)
                    if item.index(i)<=len(item)-1:
                        file.write(",")
                    if item.index(i)==len(item)-1:
                        w_time = datetime.now()
                        w_stime = datetime.strftime(w_time,
                            '%Y-%m-%d %H:%M:%S')
                        file.write(w_stime)
                file.write("\n")
        	


def main():
#    args = sys.argv[1:]
    try:
        opts,args = getopt.getopt(sys.argv[1:],"C:c:d:o:")     
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    for o,a in opts:
        if o == '-c':
            cfg_file = a
        elif o == '-d':
            usr_file = a
        elif o == '-o':
            gz_file = a
        elif o == '-C':
            sb_city = a
        else:
            assert False,"Unhandled option"
    
#    index_c = args.index('-c')
#    cfg_file = args[index_c+1]
#
#    index_d = args.index('-d')
#    usr_file = args[index_d+1]
#    
#    index_o = args.index('-o')
#    gz_file = args[index_o+1]
#
#    index_city = args.index('-C')
#    sb_city = args[index_city+1]
    
    queue1 = Queue()    
    queue2 = Queue()
    queue3 = Queue()

    con = Config(cfg_file,sb_city)
    u = UserData(usr_file,con)

    p1 = Process(target=u.get_info,args=(queue2,))
    p2 = Process(target=u.write_solution,args=(queue2,queue3))
    p3 = Process(target=u.dumptofile,args=(gz_file,queue3))

    p1.start()
    p1.join()

    p2.start()
    p2.join()

    p3.start()
    p3.join()
#    u.calculator()
#    u.cal()
#    u.dumptofile(gz_file)    
				
if __name__=='__main__':
    main()

