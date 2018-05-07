# 
1. 从种子库里拉下来种子，按照netlocation为key，value是一个url的list 来初步分类种子,结果如`{'www.qq.com' : [ "http://www.qq.com/haha/qwe/123.html" ]...}`

2. 对list里面的url进行split(netlocation)的操作，取list的最后一个str作为建trie树的初始str，如`{'www.qq.com' : [ "http://www.qq.com/haha/qwe/123.html" ]...} -> {'www.qq.com' : [ "haha/qwe/123.html" ]...}`

3.  建立trie树，每个节点的成员变量: `node_str = str ,repeat = int, depth = int, children = {}` , 

# 拿到详情页
