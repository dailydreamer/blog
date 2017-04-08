+++
date = "2015-06-22T20:00:00+08:00"
title = "ElasticSearch搜索配置（2）"
categories = ["技术随笔"]
tags = ["程序员", "ElasticSearch"]
+++

这次再来说说ElasticSearch的其他一些特性。

## Bulk

使用Index进行索引是一次索引一条doc，而bulk提供了批量索引的功能，能够显著的减少索引时间。
经过实际测试，对于1个100Mb约20K条doc，向远程服务器单节点发起索引的完成时间对比如下表。

| chunck_size | time/s |
| :-----------: | :------: |
| 200 | 298.34 |
| 500 | 216.84 |
| 1000 | 169.64 |
| 2000 | 164.71 |

可以看出chunck_size在一个合适的区间时可以显著减少索引时间，而chunck_size的选取也和一个doc的大小有关。

这里是[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html)。

ElasticSearch的python API中对bulk进行了封装，有`helpers.streaming_bulk`和`helpers.bulk`两个方法，[官方文档](https://elasticsearch-py.readthedocs.org/en/master/helpers.html?highlight=bulk#elasticsearch.helpers.bulk)在这。大致使用方法如下：

```py
for success, fail in helpers.streaming_bulk(es, genDoc(filename), index=INDEX, doc_type=DOCTYPE, chunk_size=1000):
	print 'success: ', success
```

```py
success, fail = helpers.bulk(es, genDoc(filename), index=INDEX, doc_type=DOCTYPE, chunk_size=1000)
```

其中geDoc()是一个迭代器。
这两个方法的区别在于bulk调用了streaming_bulk并将信息一起返回。

## 拼音搜索

对于中文内容较多的索引，如果能够使用拼音搜索会十分方便。
ElasticSearch有插件[elasticsearch-analysis-pinyin](https://github.com/medcl/elasticsearch-analysis-pinyin)可以实现这个功能。
它可以将中文转化为拼音字母，在建立索引的时候就可以在倒排列表中使对应的拼音字母关联到包含中文的Doc上。

为了将拼音搜索的索引和IK分词的索引结合，需要用到另一个插件[elasticsearch-analysis-combo](https://github.com/yakaz/elasticsearch-analysis-combo/)。
它可以将两个Analyzer的结果合并起来得到一个新的Analyzer。

基本的配置如下。

```yml
index:
  analysis:
    analyzer:
      ik:
          alias: [news_analyzer_ik,ik_analyzer]
          type: org.elasticsearch.index.analysis.IkAnalyzerProvider
      ik_max_word:
          type: ik
          use_smart: false
      ik_smart:
          type: ik
          use_smart: true
      pinyin:
        type: custom
        tokenizer: standard
        filter:
         - standard 
         - pinyin_filter
         - lowercase         
      combo:
        type: combo
        sub_analyzers: 
         - ik
         - pinyin
    filter:
      pinyin_filter : 
        type : pinyin
        first_letter : none
        padding_char : ''
```

先使用pinyin插件定义一个pinyin filter， `first_letter`属性看是否得到拼音首字母缩写，`padding_char`属性确定首字母缩写和全拼音的连接方式。
然后定义一个custom的pinyin analyzer。tokenizer使用standard，将所有汉字词语分成单个字，filter先通过standard初步过滤，然后使用pinyin filter转成单个字的拼音，最后使用lowercase统一小写。

效果如下：

输入命令

```sh
curl -XGET 'http://localhost:9200/school_search_index/_analyze?analyzer=pinyin&pretty' -d '清华大学'
```

得到结果

```json
{
  "tokens" : [ {
    "token" : "qing",
    "start_offset" : 0,
    "end_offset" : 1,
    "type" : "<IDEOGRAPHIC>",
    "position" : 1
  }, {
    "token" : "hua",
    "start_offset" : 1,
    "end_offset" : 2,
    "type" : "<IDEOGRAPHIC>",
    "position" : 2
  }, {
    "token" : "da",
    "start_offset" : 2,
    "end_offset" : 3,
    "type" : "<IDEOGRAPHIC>",
    "position" : 3
  }, {
    "token" : "xue",
    "start_offset" : 3,
    "end_offset" : 4,
    "type" : "<IDEOGRAPHIC>",
    "position" : 4
  } ]
}
```

最后使用combo analyzer将两个analyzer合并。

## 自动补全

搜索引擎的自动补全有两种类型。
一种是基于你过去或者是其他人的热门的搜索历史进行补全，另一种是基于语言模型进行补全。

对于第一种根据搜索历史的补全，适用与拥有大量数据的搜索引擎。
在ElasticSearch中可以使用[Completion Suggester](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters-completion.html)实现。
由于不适用与用户数据较少的搜索引擎，便不细说，可以参考[这篇文章](http://blog.qbox.io/quick-and-dirty-autocomplete-with-elasticsearch-completion-suggest)。

第二种基于语言模型的补全，可以使用类似于拼音搜索的实现方式，在建立索引的时候对一个单词string的所有substring都建立到包含该string的Doc的映射即可。
但是需要注意的是这样会显著增加索引的大小。

在ElasticSearch中可以使用[n-Gram Tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-ngram-tokenizer.html#analysis-ngram-tokenizer)或[n-Gram filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-ngram-tokenfilter.html)实现。
具体可以参考[这篇文章](http://jontai.me/blog/2013/02/adding-autocomplete-to-an-elasticsearch-search-application/)。