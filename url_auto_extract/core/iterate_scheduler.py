#!-*- encoding:utf-8 -*-
"""
   迭代控制器
"""
import sys
import time
import new_cluster as clus
import verify_coverage as vco
import extract_pattern as epat

URL_DATA_PATH_PRE = "../../url_data/"
DOMAIN_LIST_PATH = "../../source_data/domain.txt"
RE_EXPRESSION_PATH = "../../re_expression/"

def cluster_url(domain,depth):
    # print ">>> clusting..."
    start = time.time()
    repeat = 10
    url_file = URL_DATA_PATH_PRE+domain+".url"
    pat = r':|/|\.|\?|&|=|#'

    
    cluster = clus.List_Tree(depth, repeat)
    with open(url_file) as f:
        url_list = f.read().split('\n')

    for url in url_list:
        cluster.insert(pat, url)
    end = time.time()

    # print "clusting cost %s s"%str(int(end-start))
    # print 

    return cluster.get_repeat()


def extract_url(cluster_url, domain):
    # print ">>> extracting url..."
    start = time.time()
    fname = 'raw_url.txt'
    with open(fname,'w') as f:
        f.write(cluster_url)
        
    re_fname = RE_EXPRESSION_PATH + domain + ".re"
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
    # print "extract cost %s s"%str(int(end-start))
    # print 

    return re_fname
    
def verify_coverage(domain,re_fname,depth):
    # print ">>> verifying url..."
    url_fname = URL_DATA_PATH_PRE+domain+".url"
    start = time.time()
    repeat = 10
    # print '-'*30
    # print 'depth=',depth, 'repeat=',repeat
    coverage = vco.verify(url_fname,re_fname)
    # print '-'*30
    end = time.time()
    # print "verify cost %s s"%str(int(end-start))
    return coverage

if __name__ == '__main__':

    with open(DOMAIN_LIST_PATH) as f:

        with open("best_depth.log", "w") as log:
            domain_list = filter(None, f.read().split('\n'))
            for domain in domain_list:
                domain = domain.lower()
                
                s = "\n---handling:\t"+domain
                print s

                start_depth = len(domain.split('.')) + 1
                max_coverage = 0
                best_depth = 0

                start = time.time()
                for i in range(start_depth, start_depth+3):
                    cluster = cluster_url(domain, i)
                    re_fname = extract_url(cluster, domain)
                    coverage = verify_coverage(domain,re_fname,i)
                    if coverage > max_coverage:
                        max_coverage = coverage
                        best_depth = i
                
                # 最后生成最终的正则表达式
                cluster = cluster_url(domain, best_depth)
                re_fname = extract_url(cluster, domain)
                coverage = verify_coverage(domain,re_fname,i)

                end = time.time()

                s += '\n' + '-'*30 + "\n[domain]:\t"+domain + "\n[coverage]:\t"+str(max_coverage)+"%" + "\n[Best Depth]:\t" + str(best_depth)\
                    + "\nloop cost %s s"%str(int(end-start))\
                    + "\n" +'-'*30
                
                print s

                log.write(s)