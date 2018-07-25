# 简介 (Introduction)

对同个域名下的URL, 进行聚类, 泛化正则表达式操作, 输入是 `URL列表`, 输出是 `分类好的正则表达式列表`

# 快速上手（Getting Started）
## 环境准备
* `python2.7`

## 执行demo
参考最下面的执行目录执行

1. 把域名列表放入 `./source_data/domain.txt`
2. `cd ./pull_url & python es_fetch_scroll.py` 对es库进行拉取,url放入 `./url_data``re_expression`
3. `cd ../url_auto_extract/core & python iterate_scheduler.py` 执行迭代脚本,生成的正则表达式放入 `../re_expression` 文件夹下, 同时会生成覆盖率的log文件 `./url_auto_extract/core/best_depth.log `
# 目录如下
```
.
├── README.md
├── pull_url
│   └── es_fetch_scroll.py
├── re_expression
├── source_data
│   ├── data_source.url
│   ├── domain.txt
│   └── url.txt
├── url_auto_extract
│   └── core
│       ├── best_depth.log 
│       ├── core.bak
│       │   └── trie_cluster.py
│       ├── extract_pattern.py
│       ├── extract_pattern.pyc
│       ├── iterate_scheduler.py
│       ├── new_cluster.py
│       ├── new_cluster.pyc
│       ├── raw_url.txt
│       ├── re_url.txt
│       ├── verify_coverage.py
│       └── verify_coverage.pyc
└── url_data
```