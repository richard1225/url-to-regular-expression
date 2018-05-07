#!/usr/bin/python
# -*- coding:utf-8 -*-
# * trie, prefix tree, can be used as a dict
#
import sys
import re

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
                #print key_list
                #print node.repeat
                #print "\n"
            if len(key_list) > 0:
                key_list.remove(e)
        #print node.depth

    
    def get_prefix_by_depth_repeat(self, depth, repeat):
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
        if node.value is not NULL:
            results.append((sep.join(path), node.value, node.depth, node.repeat))
        for k, v in node.children.iteritems():
            path.append(k)
            self.__collect_items(v, path, results, sep)
            path.pop()
        return results  

    def items(self, prefix, sep = ' '):
        elements = prefix if isinstance(prefix, list) else prefix.split(sep)
        node = self.root
        for e in elements:
            if e not in node.children:
                return []
            node = node.children[e]
        results = []
        path = [prefix]
        self.__collect_items(node, path, results, sep)
        return results

    def keys(self, prefix, sep = ' '):
        items = self.items(prefix, sep)
        return [key for key,value,depth,repeat in items]

if __name__ == '__main__':
    trie = Trie()
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
    pat = ':|/|\.|\?|&|=|#'
    for url in urls:
            e_list = re.split(pat, url)
            #e_list = re.split(':|/|\.|\?|&|=|#', url)
            #print e_list
            #e_set |= set(e_list)
            t_list = []
            for e in e_list:
                if not e:
                    continue
                if len(e) == 0 or e is None:
                    continue
                t_list.append(e) 
            trie.insert(t_list, 1)
            str_url_map['|'.join(t_list)] = url

    #print str_url_map
    str_list = str_url_map.keys()
    #print str_list
    t_list = trie.keys('http enshi house ifeng com search')
    #print t_list
    for e in t_list:
        t_str = '|'.join(e.split(' '))
        #print t_str
        for  e in str_list:
            if t_str in e:
                #print str_url_map[e]
                pass
    #print trie.items('http digi 163 com')
    #trie.pre_order({}, [], trie.root)
    target_keys = trie.get_prefix_by_depth_repeat(6, 10)
#   print target_keys
    for k in target_keys:
        t_list = trie.keys(' '.join(k.split('|')))
        #print t_list
        for e in t_list:
            t_str = '|'.join(e.split(' '))
            #print t_str
            for  e in str_list:
                if t_str in e:
                    print str_url_map[e]
        print "\n"
       

trie = Trie()
trie.insert('happy 站台', 1)
trie.insert('happy 站台 xx', 10)
trie.insert('happy 站台 xx yy', 11)
trie.insert('happy 站台 美食 购物 广场', 2)
trie.insert('sm', 222)
trie.insert('sm 国际', 22)
trie.insert('sm 国际 广场', 2)
trie.insert('sm 城市广场', 3)
trie.insert('sm 广场', 4)
trie.insert('sm 新生活 广场', 5)
trie.insert('sm 购物 广场', 6)
trie.insert('soho 尚都', 3)

print trie.get('sm')
print trie.longest_prefix([], default="empty list")
print trie.longest_prefix('sm')
print trie.shortest_prefix('happy 站台')
print trie.shortest_prefix('happy 站台 xx')
print trie.shortest_prefix('sm')
print trie.longest_prefix('sm xx', sep = ' ', default = None)
print 'sm 广场 --> ', trie.get('sm 广场')
print trie.get('sm 广场'.split(' '))
print trie.get('神马')
print trie.get('happy 站台')
print trie.get('happy 站台 美食 购物 广场')
print trie.longest_prefix('soho 广场', 'default')
print trie.longest_prefix('soho 尚都 广场')
print trie.longest_prefix_value('soho 尚都 广场')
print trie.longest_prefix_value('xx 尚都 广场', 90)
print trie.longest_prefix_value('xx 尚都 广场', 'no prefix')
print trie.longest_prefix_item('soho 尚都 广场')

print '============== keys ================='
print 'prefix "sm": ', ' | '.join(trie.keys('sm'))
print '============== items ================='
print 'prefix "sm": ', trie.items('sm')

print '================= delete ====================='
print trie.delete('sm 广场')
print trie.get('sm 广场')
print trie.delete('sm 国际')
print trie.get('sm 国际')
print trie.delete('sm xx')
print trie.delete('xx')

print '====== no item matches any prefix of given key ========'
print trie.longest_prefix_value('happy')
print trie.longest_prefix_value('soho xx')

