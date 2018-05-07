#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
import sys
from urlparse import *

'''
#priority: az > AZ > 09 > - > _
g_pat_list = {
    'az':'[a-z]+',
    'AZ':'[A-Z]+',
    '09':'[0-9]+,'
    'azAZ':'[a-zA-Z]+',
    'az09':'[a-z0-9]+',
    'az-': '[a-z-]+',
    'az_': '[a-z_]+',
    'azAZ09' : '[a-zA-Z0-9]+',
    'azAZ-' : '[a-zA-Z-]+',
    'azAZ_' : '[a-zA-Z_]+',
    'az09-' : '[a-z0-9-]+',
    'az09_' : '[a-z0-9_]+',
    'az-_' : '[a-z-+]+',
    'azAZ09-' : '[a-zA-Z0-9-]+',
    'azAZ09_' : '[a-zA-Z0-9_]+' 
    'AZ09': '[A-Z0-9]+',
    'AZ-': '[A-Z-]+',
    'AZ_': '[A-Z_]+',
    '09-': '[0-9-]+',
    '09_': '[0-9_]+',
    }
'''


g_meta_chars = ['/', '=', '?', '&', '#', '.']

def find_lcsubstr(s1, s2): 
    p = 0
    str_len = len(s1) if len(s1) < len(s2) else len(s2)
    for i in range(str_len):
        if s1[i] == s2[i]:
            p+=1
        else:
            break
    return s1[0:p],p+1   #返回最长子串及其长度
print find_lcsubstr('abcdfg','abdfg')
a='http://www.yc.ifeng.com/toLogin?next=/book/3051216/199/'
b='http://www.yc.ifeng.com/toLogin?next=/book/3050122/624/'
print find_lcsubstr(a, b)

url_list = [
    'http://www.yc.ifeng.com/toLogin?next=/book/3050091/510/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3050091/1006/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3047834/193/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3042999/174/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3042999/384/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3022193/1582/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3048917/152/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3048917/178/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3048562/380/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3048562/210/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3022231/440/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3022231/254/',
    'http://www.yc.ifeng.com/toLogin?next=/book/3049983/64/'
]


def find_lcsubstr_among_strlist(strlist, pat_flag=False):
    if len(strlist) == 0 or strlist is None:
        return ''
    lcsubstr = ''
    mid_res = () # 保存长度最小的公共子串
    s1 = strlist[0]
    s2 = strlist[1]
    mid_res = find_lcsubstr(s1, s2)

    """ 优化部分 """
    for i in range(2, len(strlist) - 1):
        s1 = strlist[i]
        #print s1,s2
        res = find_lcsubstr(mid_res[0], s1)
        if res[1] < mid_res[1]:
            mid_res = res
    #print mid_res

    lcsubstr = mid_res[0]

    # 防止出现 http://www.baidu.com/[a-z]+[ 的情况
    if pat_flag:
        # print "\n[pat_flag]: ", lcsubstr
        # ？？为什么要]
        if lcsubstr[len(lcsubstr)-1]  in ['[', ']']:
            return lcsubstr[:len(lcsubstr)-1]
        #return mid_res[0]
    if lcsubstr[len(lcsubstr)-1] not in g_meta_chars:
        #print "lcsubstr -1: ", lcsubstr[len(lcsubstr)-1]
        p1 = lcsubstr.rfind('/')
        p2 = lcsubstr.rfind('&')
        p3 = lcsubstr.rfind('?')
        pos = max(p1, p2)
        pos = max(pos, p3)

        # 找到URL中最后一个是 '/' or '&' or '?' 的字符的位置，并从这个位置开始，截掉后面的字符，保留最后一个'/&?'字符
        if pos != len(lcsubstr) - 1:
            return lcsubstr[:(pos+1)]

    return lcsubstr

substr = find_lcsubstr_among_strlist(url_list)
print substr


def gen_pat(s):
    """生成参数的正则表达式pattern"""
    if s is None or len(s) == 0:
        return ''
    res = ''
    az_flag = 0
    AZ_flag = 0
    digit_flag = 0
    hyphen_flag = 0
    underline_flag = 0
    percentage_flag = 0
    slash_flag = 0
    other_flag = 0
    other_chars = []
    for c in s:
        if c >= 'A' and  c <= 'Z':
            AZ_flag = 1
        elif c >= 'a' and c <= 'z':
            az_flag = 1
        elif c >= '0' and c <= '9':
            digit_flag = 1
        elif c == '-':
            hyphen_flag = 1
        elif c == '_':
            underline_flag = 1
        elif c == '%':
            percentage_flag = 1
        elif c == '/':
            slash_flag = 1
        else:
            other_flag = 1
            other_chars.append(c)
    
    if az_flag == 1:
        res += 'a-z'
    if AZ_flag == 1:
        res += 'A-Z'
    if digit_flag == 1:
        res += '0-9'
    if hyphen_flag == 1:
        res += '-'
    if underline_flag == 1:
        res += '_'
    if percentage_flag == 1:
        res += '%'
    if slash_flag == 1:
        res += '/'
    res = '[' + res + ']+'
    if other_flag == 1:
        print other_chars
    return res, other_flag, other_chars

print gen_pat('3049983azdsaf-AZ._++')
   
# 参数格式化
def format_pat_url(url, substr):
    """  返回该url泛化的正则表达式 """
    #print "substr: ", substr
    # print "url: ", url
    beg = -1
    end = -1
    res = url
    #pos = url.rfind(substr)
    pos = len(substr)
    beg = pos
    res = url[:beg]
    #print pos
    for i in range(pos, len(url)):
        # print i, url[i]
        if url[i] in g_meta_chars and beg == -1: 
            beg = i
        elif (url[i] in g_meta_chars or i == len(url) - 1) and end == -1:
            # 截取到一个参数
            end = i
            s = ''
            if i == len(url) - 1 and url[end] not in ['/', '+', '=', '?']:
                s = url[beg:end+1]
            else:
                s = url[beg:end]

            # print "s: ", s

            if len(s) == 0: #t&mid=&srctag=cpz_sh_imtj_
                res += url[end]
                beg = end + 1
                end = -1
                continue
            # print "res: ", res
            t_res, f, c_list = gen_pat(s)
            # print "[t_res]: ", t_res
            if f != 1:
                #res = res.replace(url[beg:end], t_res)
                #print url[:beg]
                #print t_res
                #print url[end:]
                res +=  t_res
                if i != len(url) -1 or (i == len(url) - 1 and url[end] == '/'):
                     res += url[end]
            else:
                print 'other c', c_list
            beg = end + 1
            end = -1
            
        else:
            continue
    # print "res", res, '\n'
    return res

def trans_dot(s):
    if len(s) == 0:
        return
    s = s.replace('?', '\?')
    s = s.replace('.', '\.')
    return s  
  
    
'''
# print format_pat_url('http://www.yc.ifeng.com/toLogin?next=/book/3049983/64/', substr) 
pat_url_list = []
for url in url_list:
    print url
    pat_url_list.append(format_pat_url(url, substr))
    
print pat_url_list

pat_substr = find_lcsubstr_among_strlist(pat_url_list)
print pat_substr


ul2 = [
'http://m.ishare.iask.sina.com.cn/f/7207450.html',
'http://m.ishare.iask.sina.com.cn/f/22029879.html',
'http://m.ishare.iask.sina.com.cn/f/33549194.html',
'http://m.ishare.iask.sina.com.cn/f/62125756.html',
'http://m.ishare.iask.sina.com.cn/f/1qkZ7OkuSPUF.html',
'http://m.ishare.iask.sina.com.cn/f/17198825.html',
'http://m.ishare.iask.sina.com.cn/f/1qm1oTZv9PBv.html',
'http://m.ishare.iask.sina.com.cn/f/36799270.html',
'http://m.ishare.iask.sina.com.cn/f/33660738.html',
'http://m.ishare.iask.sina.com.cn/f/8PXYuA7djtd.html',
'http://m.ishare.iask.sina.com.cn/f/66142506.html',
'http://m.ishare.iask.sina.com.cn/f/22928722.html',
'http://m.ishare.iask.sina.com.cn/f/68463151.html',
'http://m.ishare.iask.sina.com.cn/f/19750968.html',
'http://m.ishare.iask.sina.com.cn/f/15208914.html',
'http://m.ishare.iask.sina.com.cn/f/16878895.html',
'http://m.ishare.iask.sina.com.cn/f/25317916.html',
'http://m.ishare.iask.sina.com.cn/f/8PHOSf7RsXD.html'
]

substr2 = find_lcsubstr_among_strlist(ul2)
print substr2      
pat_url_list2 = []
for url in ul2:
    print url
    pat_url_list2.append(format_pat_url(url, substr2))
    
print pat_url_list2

pat_substr2 = find_lcsubstr_among_strlist(pat_url_list2)
print pat_substr2
if substr2 == pat_substr2:
    pat_substr2 += '*'
    print pat_substr2
    print trans_dot(pat_substr2)
'''

def pattern_extract(url_list):
    substr = find_lcsubstr_among_strlist(url_list)
    pat_url_list = []
    for url in url_list:
        pat_url_list.append(format_pat_url(url, substr))
    pat_substr = find_lcsubstr_among_strlist(pat_url_list, True)
    print pat_substr
    if substr == pat_substr or pat_substr[len(pat_substr)-1] in g_meta_chars:
        pat_substr += '*'
    return trans_dot(pat_substr)


ul3 = [
'http://wap.ifeng.com/tech/app/news?ou=p%3D3&aid=111647103',
'http://wap.ifeng.com/tech/app/news?m=b775ae2893651f1_5619349&cid=0&aid=100311204',
'http://wap.ifeng.com/tech/app/news?m=9c62b25bcaf6b15_1750828&cid=0&aid=111770495',
'http://wap.ifeng.com/tech/app/news?m=7c182dc64d498d1_2772953&aid=98820217',
'http://wap.ifeng.com/tech/app/news?m=c5d4357692aebd2_8662167&aid=95454771&p=3',
'http://wap.ifeng.com/tech/app/news?m=4293f4c837fb5a0_16924079&aid=112146540',
'http://wap.ifeng.com/tech/app/news?m=e0a684c315c2ddd_15435872&cid=0&aid=100314418',
'http://wap.ifeng.com/tech/app/news?cid=0&aid=101551869',
'http://wap.ifeng.com/tech/app/news?cid=0&aid=98851827',
'http://wap.ifeng.com/tech/app/news?cid=0&aid=101794798'
]


ul4 = [
'http://wap.ifeng.com/tech/digi/shouji/news?ou=ifeng_tmall&v=5&aid=119353960',
'http://wap.ifeng.com/tech/digi/shouji/news?m=1&cid=0&aid=101555306',
'http://wap.ifeng.com/tech/digi/shouji/news?m=880ca9bfd13536e_8324436&cid=0&aid=114009751',
'http://wap.ifeng.com/tech/digi/shouji/news?m=97c6bc2d6431b30_15389722&cid=0&aid=113871491',
'http://wap.ifeng.com/tech/digi/shouji/news?m=f52beec9fdd8db8_1319451&cid=0&aid=114435412',
#'http://wap.ifeng.com/tech/digi/shouji/news?m=1'+onmouseover%3Dijv%3D128+'&aid=119318100',
'http://wap.ifeng.com/tech/digi/shouji/news?m=p%3D5&cid=0&aid=119163529',
'http://wap.ifeng.com/tech/digi/shouji/news?m=a7616e6c71b016e_12611427&cid=0&aid=114002007',
'http://wap.ifeng.com/tech/digi/shouji/news?m=f8a15a46ddbce38_11201912&cid=0&aid=119306079',
'http://wap.ifeng.com/tech/digi/shouji/news?m=4fbd2f65b00453e_14955738&aid=110484188',
'http://wap.ifeng.com/tech/digi/shouji/news?_gp=0&m=1&cid=0&aid=110686859',
'http://wap.ifeng.com/tech/digi/shouji/news?cid=0&aid=71063578',
'http://wap.ifeng.com/tech/digi/shouji/news?cid=0&aid=97030028',
'http://wap.ifeng.com/tech/digi/shouji/news?cid=0&aid=107658312&p=1',
'http://wap.ifeng.com/tech/digi/shouji/news?cid=0&aid=102599953&p=4',
'http://wap.ifeng.com/tech/digi/shouji/news?cid=0&aid=87327954'
]
print pattern_extract(ul3)
print pattern_extract(url_list)
print pattern_extract(ul4)


if __name__ == '__main__':
    fname = sys.argv[1]
    ofname = sys.argv[2]
    url_list = []
    with open(fname, 'rb') as f:
        with open(ofname, 'wb') as of:
            netloc = ''
            while True:
                line = f.readline()
                if line:
                    # print line
                    if line == '\n':
                        #print "do something and clear list"
                        if len(url_list) >= 10:
                            print netloc
                            print url_list
                            pat = pattern_extract(url_list)
                            print pat
                            print '\n'
                            of.write(netloc)
                            of.write('\n')
                            of.write(pat)
                            #of.write(str(url_list))
                            of.write('\n')
                            of.write('\n')
                        url_list = []
                    else:
                        if len(url_list) <= 50:
                            r = urlparse(line)
                            netloc = r.netloc
                            url_list.append(line.strip())
                else:
                    break
