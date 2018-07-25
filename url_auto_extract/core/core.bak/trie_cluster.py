#!/usr/bin/python
# -*- coding:utf-8 -*-
# * trie, prefix tree, can be used as a dict
#
from __future__ import print_function
import sys
import re
import threadpool
from Queue import Queue
print = lambda x: sys.stdout.write("%s\n" % x)

reload(sys)
sys.setdefaultencoding('utf-8') 


# Singleton sentinel - works with pickling
class NULL(object):
    pass

class Node:
    def __init__(self, value = NULL, repeat=1, depth=0):
        self.value = value
        self.children = {}
        self.repeat = repeat
        self.depth = depth

class Trie(object):
    def __init__(self):
        self.root = Node()

    def insert(self, key, value = None, sep = ' '): # key is a word sequence separated by 'sep'
        elements = key if isinstance(key, list) else key.split(sep)
        node = self.root
        for e in elements:
            if not e: continue
            if e not in node.children:
                child = Node(depth=node.depth+1)
                node.children[e] = child
                node = child
            else:
                node.repeat += 1
                node = node.children[e]
        node.value = value

    def get(self, key, default = None, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        node = self.root
        for e in elements:
            if e not in node.children:
                return default
            node = node.children[e]
        return default if node.value is NULL else node.value

    def delete(self, key, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        return self.__delete(elements)

    def __delete(self, elements, node = None, i = 0):
        node = node if node else self.root
        e = elements[i]
        if e in node.children:
            child_node = node.children[e]
            if len(elements) == (i+1):
                if child_node.value is NULL: return False # not in dict
                if len(child_node.children) == 0:
                    node.children.pop(e)
                else:
                    child_node.value = NULL
                return True
            elif self.__delete(elements, child_node, i+1):
                if len(child_node.children) == 0:
                    return node.children.pop(e)
                return True
        return False

    def shortest_prefix(self, key, default = NULL, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        results = []
        node = self.root
        value = node.value
        for e in elements:
            if e in node.children:
                results.append(e)
                node = node.children[e]
                value = node.value
                if value is not NULL:
                    return sep.join(results)
            else:
                break
        if value is NULL:
            if default is not NULL:
                return default
            else:
                raise Exception("no item matches any prefix of the given key!")
        return sep.join(results)

    def longest_prefix(self, key, default = NULL, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        results = []
        node = self.root
        value = node.value
        for e in elements:
            if e not in node.children:
                if value is not NULL:
                    return sep.join(results)
                elif default is not NULL:
                    return default
                else:
                    raise Exception("no item matches any prefix of the given key!")
            results.append(e)
            node = node.children[e]
            value = node.value
        if value is NULL:
            if default is not NULL:
                return default
            else:
                raise Exception("no item matches any prefix of the given key!")
        return sep.join(results)

    def longest_prefix_value(self, key, default = NULL, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        node = self.root
        value = node.value
        for e in elements:
            if e not in node.children:
                if value is not NULL:
                    return value
                elif default is not NULL:
                    return default
                else:
                    raise Exception("no item matches any prefix of the given key!")
            node = node.children[e]
            value = node.value
        if value is not NULL:
            return value
        if default is not NULL:
            return default
        raise Exception("no item matches any prefix of the given key!")

    
    def get_prefix_by_depth_repeat(self, depth, repeat):
        """以深度和出现次数为限制条件 以先序遍历的方式打印树的各个分支"""
        results = {}
        self.pre_order(results, [], self.root, depth, repeat)
        return results    


    def longest_prefix_item(self, key, default = NULL, sep = ' '):
        elements = key if isinstance(key, list) else key.split(sep)
        node = self.root
        value = node.value
        results = []
        for e in elements:
            if e not in node.children:
                if value is not NULL:
                    return (sep.join(results), value)
                elif default is not NULL:
                    return default
                else:
                    raise Exception("no item matches any prefix of the given key!")
            results.append(e)
            node = node.children[e]
            value = node.value
        if value is not NULL:
            return (sep.join(results), value)
        if default is not NULL:
            return (sep.join(results), default)
        raise Exception("no item matches any prefix of the given key!")

    def __collect_items(self, node, path, results, sep):

        # 如果这个node 是最后一个node了
        if node.value is not NULL:
            results.append((sep.join(path), node.value, node.depth, node.repeat))
            # print results
        # 递归地append 各条分支到result上
        for k, v in node.children.iteritems():
            path.append(k)
            self.__collect_items(v, path, results, sep)
            path.pop()
        return results  

    def items(self, prefix, sep = ' '):
        """ 拿到以prefix为前缀的所有url """
        elements = prefix if isinstance(prefix, list) else prefix.split(sep)
        node = self.root
        for e in elements:
            if e not in node.children:
                return []
            node = node.children[e]
        results = []
        # print "[prefix]", prefix
        path = [prefix]
        # print "[path]", path
        self.__collect_items(node, path, results, sep)
        return results

    def keys(self, prefix, sep = ' '):
        """ 拿到以prefix为前缀的所有url """

        items = self.items(prefix, sep)
        # print items
        # print [key for key,value,depth,repeat in items]
        return [key for key,value,depth,repeat in items]
    
    def pre_order(self,results = {}, key_list = None, node = None, depth=5, repeat=3):
        if results is None:
            results = {}
        if key_list is None:
            key_list = []
        if node is None:
            node = self.root
       # if key_list is not None:
       #     key_list = key_list
       #     print key_list
        if node.depth > depth:
            #print "\n"
            return
        for e in node.children:
            key_list.append(e)
            #print key_list
            self.pre_order(results, key_list, node.children[e], depth, repeat)
            if len(key_list) == depth and node.repeat >= repeat:
                results['|'.join(key_list)] = node.repeat
                # print key_list
                # print node.repeat
                # print "\n"
            if len(key_list) > 0:
                key_list.remove(e)
        # print node.depth


def make_trie_from_url_list(url_list, pat):
    trie = Trie()
    str_url_map = {}
    for url in url_list:
        e_list = re.split(pat, url)
        e_list = filter(None,e_list) # 去处空字符串   
        # print e_list
        t_list = []
        for e in e_list:
            if not e:
                continue
            if len(e) == 0 or e is None:
                continue
            t_list.append(e)
        trie.insert(t_list, 1)
        str_url_map['|'.join(t_list)] = url
    return trie, str_url_map

def expend_prefix(k):
    t_list = trie.keys(' '.join(k.split('|'))) # 返回类型：['http news changsha cn html 417 list html']
    # print t_list
    res_list = []
    for e in t_list:
        t_str = '|'.join(e.split(' '))
        # print t_str
        # str_list 是 ['http|news|changsha|cn|html|417', 'http|www|hkstv|tv|index|news'...]
        for  e in str_list:
            if t_str in e:
                # print str_url_map[e]
                res_list.append(str_url_map[e])
    # print res_list
    if len(res_list) >= 10:
        i = 1
        urls_str = ""
        for url in res_list:
            if i <= 20:
                urls_str += url+"\n"
                i+=1
        urls_str += "\n"
        print(urls_str)

if __name__ == '__main__':
    #trie = Trie()
    trie = None
    fname = sys.argv[1]
    urls = []
    e_set = set()
    str_url_map = {}
    with open(fname, 'rb') as f:
        while True:
            #url = f.readline().strip().encode('utf-8')
            url = f.readline().strip()
            if len(url) != 0:
                urls.append(url)
            else:
                break
    # print urls
    pat = ':|/|\.|\?|&|=|#'
    # for url in urls:
    #     e_list = re.split(pat, url)
    #     e_list = re.split(':|/|\.|\?|&|=|#', url)
    #     print e_list
    #     e_set |= set(e_list)
    #     t_list = []
    #     for e in e_list:
    #         if not e:
    #             continue
    #         if len(e) == 0 or e is None:
    #             continue
    #         t_list.append(e) 
    #     trie.insert(t_list, 1)
    #     str_url_map['|'.join(t_list)] = url

    trie, str_url_map = make_trie_from_url_list(urls, pat)

    # str_url_map 是 key为 "aa|bb|cc", value为 "aa://bb.cc"的 dict
    # print trie.root.children
    str_list = str_url_map.keys()
    trie.pre_order({}, [], trie.root)
    target_keys = trie.get_prefix_by_depth_repeat(5, 10) #以深度和出现次数为限制条件 以先序遍历树的各个分支,返回类型：{'http|news|changsha|cn|html|417': 12, 'http|www|hkstv|tv|index|news': 11...}
    # print target_keys

    k_list = [k for k in target_keys]
    # pool = threadpool.ThreadPool(20)
    for k in k_list:
        expend_prefix(k)
    # pool_request = threadpool.makeRequests(expend_prefix, k_list)
    # [pool.putRequest(req) for req in pool_request]
    # pool.wait()

