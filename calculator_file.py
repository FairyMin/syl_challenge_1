#!/usr/bin/env python3
import sys

class Config(object):
    def __init__(self,configfile):
        pass
    
    def get_config(self):
        pass

class UserData(object):
    def __init__(self,userdatafile):
        pass

    def calculator(self):
        pass

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
    main()
