#! -*- encoding:utf-8 -*-
import re
import sys
import json
import requests

TIMEOUT = 60000
RETURN_NUM = 5000
URL_PRE = 'cq02-bdg-recsys-es21.cq02.baidu.com:8201'
POST_DATA = '{"query": {"bool": {"should": [{"bool": {"must": [{"match_phrase": {"domain": "%s"}}]}}]}}}'
        
class ScrollFetch():

    def __init__(self, index_id, domain, type_id=''):
        """
            两个参数,index, type
        """
        self.index_id = index_id
        self.type_id = type_id
        self.domain = domain

    def get_scroll_url(self, index_id, type_id, timeout=TIMEOUT):
        """
        #初次调用该URL，设定scroll=1m则该分片保存1分钟，向该URL的请求的返回里面包含_scroll_id，标记该检索游标
        """
        url_fix = 'http://%s/%s/%s/_search?q=domain:"%s"&timeout=%s&scroll=100m&size=%s&fields=url' % \
            (URL_PRE, self.index_id, self.type_id, self.domain, timeout, str(RETURN_NUM))

        return url_fix

    def get_scroll_url_fix(self, _scroll_id, timeout=TIMEOUT):
        """
        #利用第一次返回的_scroll_id进行多次检索，加快检索速度
        """
        url_fix = "http://%s/_search/scroll?timeout=%s&scroll=100m&fields=url&scroll_id" \
            "=%s&search_type=scan" % (URL_PRE, timeout, _scroll_id)
        return url_fix

    def fetch_urls(self):
        url = self.get_scroll_url(self.index_id, self.type_id)
        print >> sys.stderr, url
        
        total_num = 0
        count = 0
        url_list = []
        scroll_id_pattern = re.compile('"_scroll_id":"([\S]+.?)","took"')
        urls_pattern = re.compile('"url"\:\[\"([\w:./]+.?)\"\]')
        
        print "\n[domain]:\t", self.domain
        print "[post_data]:\t", POST_DATA%self.domain,'\n'
        while(total_num - count*RETURN_NUM >= 0):
            try:
                resp = requests.post(url, POST_DATA%self.domain)
                
                
                total_num = int(resp.content.split('"hits":{"total":')[-1].split(',"max_score":')[0])
                count += 1
                scroll_id = re.findall(scroll_id_pattern, resp.content)[0]

                urls = []
                mjson = json.loads(resp.content)
                hits = mjson['hits']['hits']
                for hit in hits:
                    urls.append(hit['fields']['url'][0])

                url = self.get_scroll_url_fix(scroll_id)
                url_list.extend(urls)
                print "[进度]:\t",len(url_list),"/",total_num
            except:
                return url_list
        
        return url_list

            

    
if __name__ == "__main__":
    index_id = "yuqing_imp_web"

    with open("../source_data/domain.txt") as f:
        domain_list = f.read().split('\n')

    for domain in domain_list:
        scroll_fetch = ScrollFetch(index_id=index_id,domain=domain)
        urls = scroll_fetch.fetch_urls()
        with open("../url_data/"+domain.lower()+".url",'w') as f:
            f.write("\n".join(urls))
    
