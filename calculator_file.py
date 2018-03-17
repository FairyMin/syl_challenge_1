#!/usr/bin/env python3
#coding=utf-8

import sys

class Config(object):
    """读取文件类"""
    def __init__(self,configfile):
        self.cfg_file = configfile
        self._config = {}

    # 获取配置文件的内容
    def get_config(self,pzx):
        with open(self.cfg_file) as file:
            for line in file:
                # 去掉空格
                ss_line = line.replace(" ","")
                s_line = ss_line.strip()
                # 分割字符串
                f_line = s_line.split("=",1) 
                # 去掉空行
                if f_line != [""]:
                #    print(f_line)
                    self._config[f_line[0]] = f_line[1]
        # print(self._config)
        # 返回对应的配置项            
        return self._config[pzx]


class UserData(object):
    """用户类，计算工资并写入指定文件"""
    def __init__(self,userdatafile):
        self.usr_file = userdatafile
        self.userdata = {}
            
    #计算税后工资 
    def calculator(self):
        #print("-"*10)
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
                    self.userdata[f_line[0]] = f_line[1]
        print(self.userdata)
    #将计算结果写入指定文件
    def dumptofile(self,outputfile):
        pass	


def cal(**em_dict):
    tax_dict = {}
    for p in em_dict.keys():
        t = em_dict[p]-em_dict[p]*0.165 - 3500
        if t < 0:
            tax = 0
        elif t<1500:
            tax = t * 0.03
        elif t<4500:
            tax = t * 0.1 - 105
        elif t<9000:
            tax = t * 0.2 - 555
        elif t<35000:
            tax = t * 0.25 - 1055
        elif t<55000:
            tax = t * 0.3 - 2755
        elif t<80000: 
            tax = t * 0.35 - 5505
        else:
            tax = t * 0.45 -13505
        
        taxf = tax
        mon = em_dict[p] - taxf - em_dict[p]*0.165
        tax_dict[p] = format(mon,'.2f')
#    print("-----*------------")
    return tax_dict

def main():
#   print('----main----')
    if len(sys.argv) < 2:
        print("Parameter Error")
    else:
        em_list =sys.argv[1:]
        em_dict = {}
        try:
            for em in em_list:
                t = em.split(':',1)
                em_dict[t[0]] =int(t[1]) 
        except TypeError:
            print('Parameter Error')
        else:
            m = cal(**em_dict)
           # print(m)
            for gh,gz in m.items():
                print("%s:%s"%(gh,gz))
				
#???|óD?í?ó??2??a?ao????óé??a????3ìDò??óDê?3?
if __name__=='__main__':
#    main()
   # con = Config("/home/shiyanlou/syl_challenge_1/test.cfg")
   # con.get_config("JiShuL")

    u = UserData("/home/shiyanlou/syl_challenge_1/user.csv")
    u.calculator()
