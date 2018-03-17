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
    def __init__(self,userdatafile,cfg_tmp):
        self.usr_file = userdatafile
        self.userdata = {}
        #self.cfg_obj 用来引用配置文件的对象
        self.cfg_obj = cfg_tmp
        self.xx_list = []
        try:
            self.low = float(self.cfg_obj.get_config('JiShuL'))
            self.high = float(self.cfg_obj.get_config('JiShuH'))
            self.x_yl = float(self.cfg_obj.get_config('YangLao'))
            self.x_yiliao = float(self.cfg_obj.get_config('YiLiao'))
            self.x_shiye = float(self.cfg_obj.get_config('ShiYe'))
            self.x_gs = float(self.cfg_obj.get_config('GongShang'))
            self.x_shengyu = float(self.cfg_obj.get_config('ShengYu'))
            self.x_gjj = float(self.cfg_obj.get_config('GongJiJin')) 
            self.x_sb = (self.x_yl+self.x_shiye+self.x_gs
                    +self.x_shengyu+self.x_gjj+self.x_yiliao)
            print(self.x_sb)
            #print(type(self.cfg_tmp.get_config('JiShuL')))
        except TypeError:
            print("type error")        
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
        #读取到的文件格式 －－ 工号：税前工资
        #print(self.userdata)
        self.cal()
        #计算社保金额，个税金额，税后工资
    def cal(self):
        sb_dict = {}
        tax_dict = {}
        shgz_dict = {}
        for p in self.userdata.keys():
            #计算五险一金的基数
            try:
                self.userdata[p] = float(self.userdata[p])
                if self.userdata[p] < self.low:
                    j_shu = self.low
                elif self.userdata[p] > self.high:
                    j_shu = self.high
                else:
                    j_shu = self.userdata[p] 
            except:
                print("type error2")
                
            sb = j_shu * self.x_sb
            t = self.userdata[p] - sb - 3500
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
            
            sb_dict[p] = format(sb,'.2f')
            tax_dict[p] = format(tax,'.2f')
            mon = self.userdata[p] - tax - sb
            shgz_dict[p] = format(mon,'.2f')
            self.userdata[p] = format(self.userdata[p],'.0f') 
            self.xx_list.append([p,self.userdata[p],sb_dict[p],tax_dict[p],
                        shgz_dict[p]])

            
        #print(self.xx_list)
        #print(sb_dict)
        #print("-"*10)
        #print(tax_dict)
        #print('-'*10)
        #print(shgz_dict)
        #print("-----*------------")



    #将计算结果写入指定文件
    def dumptofile(self,outputfile):
        #存储格式：工号，税前工资，社保金额，个税金额，税后工资
        with open(outputfile,'w') as file:
            for item in self.xx_list:
                for i in item:
                    file.write(i)
                    if item.index(i)<len(item)-1:
                        file.write(",")
                file.write("\n")
        	

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
    con = Config("/home/shiyanlou/syl_challenge_1/test.cfg")
   # con.get_config("JiShuL")

    u = UserData("/home/shiyanlou/syl_challenge_1/user.csv",con)
    u.calculator()
    u.dumptofile('/home/shiyanlou/syl_challenge_1/gongzi.csv')

