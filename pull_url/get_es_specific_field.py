#!/usr/bin python
#-*- encoding:utf-8 -*-
"""
    从es中拉取指定field。只拉一个field可以节省拉取时间
"""
import ConfigParser
import requests
import json

esconf = ConfigParser.ConfigParser()

esconf.read(r"get_es_specific_field.conf")

es_address = esconf.get("ES_CONF","es_address")
es_field = esconf.get("ES_CONF", "specific_field")
size = esconf.get("ES_CONF", "size")

es_address = es_address % size
with open("es_field.txt","w") as f:
    pass
print es_address
print "[Get]"
resp = requests.get(es_address)
print "[Write]"
with open("es_field.txt","w") as f:
    f.write(resp.content)
print "[Parse]"
import re
pattern = re.compile(es_field+r'":"(.*?)"')
urls = re.findall(pattern,resp.content)
print "[Save url]"
with open("all_url.txt",'w') as f:
    urls = list(set(urls))
    f.write("\n".join(urls))
