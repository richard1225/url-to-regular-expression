#!/usr/bin/ python
#!-*- encoding:utf-8 -*-
"""用法：
   接收两个参数，第一个参数是url文件名，第二个参数是正则列表文件名
   用于评测 生成的正则表达式 对 原url 的覆盖率

   优化：提升了百分之35的速度
"""
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
def verify(url_fname, re_fname):
    
    # 读取原url
    with open(url_fname) as f:
        url_list = f.read().split('\n')
    # 读取正则表达式url
    with open(re_fname) as f:
        re_list =f.read().split("\n")

    # 去处空item
    url_list = filter(None, url_list)
    url_list = "     ".join(url_list)

    re_list = filter(None,re_list)

    # 选取偶数项， 即正则表达式
    re_l = re_list[1::2]

    count = 0
    # 统计有多少个url被覆盖了
    total = []
    for res in re_l:
        try:
            pat = re.compile(res+'[\S]+')
            re_res = re.findall(pat, url_list)
        except:
            print res

        total.extend(re_res)
    total = list(set(total))
    count = len(total)
    url_list = url_list.split("     ")
    
    # print "[覆盖URL数]:\t", count, "\n[总URL数]:\t", len(url_list), "\n[覆盖率]:\t%.2f"%(count*100.0/len(url_list))+"%"
    return count*100.0/len(url_list)

if __name__ == "__main__":

    url_fname = sys.argv[1]
    re_fname = sys.argv[2]
    verify(url_fname,re_fname)
    
