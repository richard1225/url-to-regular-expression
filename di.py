#!python
"""计算信息熵
"""
import math
from math import log
class HalfPatten:

    def __init__(self,x):
        self.x = x
        self.type = "halfPatten"
        self.shan = 0.
        self.regShan= 0.
        self.x_length = [len(i) for i in x]
        for i in set(self.x_length):
            self.shan -= (float(self.x_length.count(i))/len(self.x_length))*log(float(self.x_length.count(i))/len(self.x_length))
        for c in set(self.x):
            self.regShan -= (float(self.x.count(c))/len(self.x))*log(float(self.x.count(c))/len(self.x))


    def detection(self,string):
        s = ''.join(string)
        if len(s)==0:
            return ""
        if s.isalnum():
            if s.isdigit():
                return "\d"
            return "\w"
        else:
            return "."

    def gener(self,patten):
        if patten=="all":
            return "%s+"%(self.detection(self.x))
        elif patten=="zone":
            x_len = self.x_length
            x_len.sort()

            return "%s{%i,%i}"%(self.detection(self.x),x_len[0],x_len[-1])
        else:
            return "%s{%i}"%(self.detection(self.x),self.x_length[0])

    def regex(self,shanRule):
        if self.detection(self.x)=="":
            return ""
        if self.shan>0:
            if self.shan>shanRule:
                return self.gener("all")
            else:
                return self.gener("zone")
        else:
            return self.gener("length")

def main(shan=1.):
    exmple = ['123','123']
    exmple2 = ['123e','1234']
    half = HalfPatten(exmple)
    half2 = HalfPatten(exmple2)
    print half.regex(shan)
    print half2.regex(shan)

if __name__ =="__main__":
    main()
    main(0.)
