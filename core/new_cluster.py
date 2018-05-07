#! -*- encoding:utf-8 -*-
"""
    优化之后的聚类URL模块
    不再生成树
    取URL的路径depth个前缀作为key，url的list作为value，维护一个key/value的映射

    取分类好的URL列表

"""
import re
import sys

class List_Tree(object):
    def __init__(self, depth=0, repeat=1):
        self.depth = int(depth)
        self.repeat = int(repeat)
        self.url_dict = {}  # kv映射 url前缀／url list

    def insert(self, pat, url):
        # 分割url成路径，并去除空项
        e_list = re.split(pat, url)
        e_list = filter(None,e_list)

        # 只留下路径长度比需求深度大的url
        if len(e_list) >= self.depth:
            # 用路径构造前缀
            prefix = '|'.join(e_list[:self.depth])
            # 简历prefix : url[] 的映射
            if prefix not in self.url_dict:
                self.url_dict[prefix] = {'repeat':1, 'url':[url]}
            else:
                self.url_dict[prefix]['repeat'] += 1
                self.url_dict[prefix]['url'].append(url)
    
    def get_repeat(self):
        for prefix in self.url_dict:
            if self.url_dict[prefix]['repeat'] >= self.repeat:
                length = len(self.url_dict[prefix]['url'])
                if len(self.url_dict[prefix]['url']) > 10:
                    length = 10
                for url in self.url_dict[prefix]['url'][:length]:
                    print url
                print '\n'

if __name__ == '__main__':
    depth = sys.argv[1]
    repeat = sys.argv[2]
    url_file = sys.argv[3]
    pat = r':|/|\.|\?|&|=|#'

    cluster = List_Tree(depth, repeat)
    with open(url_file) as f:
        url_list = f.read().split('\n')

    for url in url_list:
        cluster.insert(pat, url)
    
    cluster.get_repeat()