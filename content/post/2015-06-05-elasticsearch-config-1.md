+++
date = "2015-06-05T20:00:00+08:00"
title = "ElasticSearch搜索配置（1）"
tags = ["编程", "ElasticSearch"]
+++

最近在用ElasticSearch做一些搜索，来谈谈其中用到的一些特性。

ElasticSearch是基于Lucene的分布式包装，其中每一个分片或一个副本都是一个Lucene实例。
ElasticSearch实现了很好的扩展性和冗余，自动负载均衡。可以通过Restful API与ElasticSearch集群交互。
我使用的是[python API](https://elasticsearch-py.readthedocs.org/en/master/)。

可以参考[ElasticSearch权威指南](https://www.elastic.co/guide/en/elasticsearch/guide/master/index.html)，讲解非常清楚。

## 建立索引

建立索引的时候可以使用mapping建立对每个字段建立映射。

```py
mapping_body = {
	'mappings':{
		'tweet':{
			"properties":{
				'text':{'type':'string', 'index':'analyzed', 'analyzer':'ik_smart', 'similarity': 'BM25'}
			}
		}
	}
}
es.indices.create(index='test-index', body=mapping_body)
```

上面为'test-index'的索引中'tweet'的type中'text'字段建立映射。

'index'设置为analyzed说明要先通过分析器，'analyzer'设置分析器为ik分词的智能粒度切分，默认为standard，不适合中文分词;'similarity'设置了相似度算法为BM25，默认为向量空间算法。

具体可以看[文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html)。

## 查询

查询可以通过ID来检索，但是作为一个搜索引擎，ElasticSearch提供了一种基于JSON的[DSL查询格式](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)。

```py
search_body = {
	"query": {
        "multi_match": {
            "query":       "Hello世界",
            "type":        "cross_fields", 
            "operator":    "or",
            "fields":      [ "author", "text^2" ]
        }
	 },
	'highlight':{
		'fields':{
			'author':{},
			'text':{}
		}
	}

}
res = es.search(index='test-index', doc_type='tweet', body=search_body)
```

### Query

上面的示例中使用了[multi match query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-multi-match-query.html)来进行多字段查询，multi match query对fields中的每个field进行query查询。

'operator'定义了对查询结果进行的操作，'or'代表取并集。

fields中的`^`代表对该字段进行boost，之后的值为浮点数，小于1表示减轻权重，否则加大权重。

'type'中的类型和适用场景见下表

| Type | Explain |
| ---- | ------- |
| best_fields | (default) Finds documents which match any field, but uses the `_score` from the best field. See best_fields. |
| most_fields | Finds documents which match any field and combines the `_score` from each field. See most_fields. |
| cross_fields | Treats fields with the same analyzer as though they were one big field. Looks for each word in any field. See cross_fields. |
| phrase | Runs a match_phrase query on each field and combines the `_score` from each field. See phrase and phrase_prefix. |
| phrase_prefix | Runs a match_phrase_prefix query on each field and combines the `_score` from each field. See phrase and phrase_prefix. |

`cross_fields`是将所有字段放在一起搜索，跟对`_all`进行query相比它可以附加权重，但是效率略微低一点。

更加详细的type的使用情景可以看权威指南的[Know Your Data](https://www.elastic.co/guide/en/elasticsearch/guide/current/_single_query_string.html)一节。

### Function Score query和script

如果需要吧离线算好的pagerank和在线查询的得分结合起来给结果排序，可以使用强大的[Function Score query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html)和[script](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting.html#_indexed_scripts)来做到这一点。

```py
"query":{
	"function_score": {
	    "boost_mode": "replace",
		"query": {
	        "multi_match": {
	            "query":query,
	            "type":"cross_fields", 
	            "operator":"or",
	            "fields":SEACHFIELDS
	        }
		 },
	    "script_score": {
			"lang":"groovy",
	        "params": {
	        	"pagerankField": PAGERANK, 
	            "pagerankW": PAGERANKW, 
	            "scoreW": 1 - PAGERANKW
	        },
	        "script_file": "school-search"
	    }
	}
}
```

使用`function_score`将原query包裹起来，在`script_score`中，`lang`设置脚本语言，默认为groovy;`params`设置脚本参数，`script_file`指定脚本文件，脚本文件保存在`./config/scripts/`下，不用写出后缀名，`config/scripts/group1/group2/test.py`应该命名为`group1_group2_test`。

脚本内容类似下面

```groovy
_score * scoreW + doc[pagerankField].value * pagerankW
```

其中`_score`是query得分，`doc[field_name]`可以获得当前doc的field，也可在其中使用`parms`中指定的参数。

还有一种使用脚本的方法是将其索引在一个特殊文件`.scripts`中，但是由于这个功能曾经爆出漏洞，而且性能不如上面的方法，现在已经默认关闭，在此不再讨论。

### Highlight

使用highlight可以在返回结果的'highlight'字段中对匹配词进行高亮，'fields'设置要高亮的field，还可以对高亮格式进行设置，默认为<em></em>。详细可以看[这里](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-highlighting.html#_highlight_query)。

### Filter

filter更像是数据库中的一些操作，不会返回_score值，只有满足条件才会被返回，但是相比query效率更高。详细可以看[这里](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-filters.html)。

有了这些基本能够满足简单的搜索需要了。

找到了一个翻译了一部分权威指南的Blog，记录在[这里](http://blog.csdn.net/dm_vincent/article/details/41820537)。