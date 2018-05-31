#!-*- encoding:utf-8 -*-
"""
   迭代控制器
"""
import sys
import time
import new_cluster as clus
import verify_coverage as vco
import extract_pattern as epat


def cluster_url():
    print ">>> clusting..."
    start = time.time()
    depth = sys.argv[1]
    repeat = sys.argv[2]
    url_file = sys.argv[3]
    pat = r':|/|\.|\?|&|=|#'

    cluster = clus.List_Tree(depth, repeat)
    with open(url_file) as f:
        url_list = f.read().split('\n')

    for url in url_list:
        cluster.insert(pat, url)
    end = time.time()

    print "clusting cost %s s"%str(int(end-start))
    print

    return cluster.get_repeat()


def extract_url(cluster_url):
    print ">>> extracting url..."
    start = time.time()
    fname = 'raw_url.txt'
    with open(fname,'w') as f:
        f.write(cluster_url)
        
    re_fname = 're_url.txt' 
    url_list = []
    with open(fname, 'rb') as f:
        with open(re_fname, 'wb') as of:
            netloc = ''
            while True:
                line = f.readline()
                if line:
                    if line == '\n':
                        if len(url_list) >= 10:
                            # print netloc
                            # print url_list
                            pat = epat.pattern_extract(url_list)
                            # print pat
                            # print '\n'
                            of.write(netloc)
                            of.write('\n')
                            of.write(pat)
                            of.write('\n')
                            of.write('\n')
                        url_list = []
                    else:
                        if len(url_list) <= 50:
                            r = epat.urlparse(line)
                            netloc = r.netloc
                            url_list.append(line.strip())
                else:
                    break
    
    end = time.time()
    print "extract cost %s s"%str(int(end-start))
    print 

    return re_fname
    
def verify_coverage(url_fname,re_fname):
    print ">>> verifying url..."
    start = time.time()
    depth = sys.argv[1]
    repeat = sys.argv[2]
    print '-'*30
    print 'depth=',depth, 'repeat=',repeat
    vco.verify(url_fname,re_fname)
    print '-'*30
    end = time.time()
    print "verify cost %s s"%str(int(end-start))
    print 

if __name__ == '__main__':
    cluster = cluster_url()
    re_fname = extract_url(cluster)
    verify_coverage(sys.argv[3],re_fname)
    