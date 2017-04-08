+++
date = "2015-06-23T20:00:00+08:00"
title = "python解析XML与生成迭代器"
categories = ["技术随笔"]
tags = ["程序员", "python"]
+++

这次来看看python解析XML与生成迭代器。

## 迭代器

使用yield操作符可以使一个函数变成迭代器。如下一段测试代码：

```py
def genTest(n):
  print 1
  print 2
  for i in range(3,n+1):
    yield i
  print n+1
  print n+2

if __name__ == '__main__':
  for i in genTest(5):
    print i
```

输出如下：

```sh
1
2
3
4
5
6
7
```

可以看出第一次调用genTest()时执行了1,2位置的代码。
之后yield将i返回给caller的i，然后再次调用时继续从genTest上次yield之后的代码执行，直至最后return停止，迭代结束。

## python解析XML

python解析XML有许多种方法，它们各有特色。

### ElementTree

[ElementTree](https://docs.python.org/2/library/xml.etree.elementtree.html)是python xml解析的一种轻量级实现。
它将XMl文件读取到内存中以一棵树的形式存储。
它速度快且方便使用，但是不能读取不规范的XMl文件，并且会一次将XML文件解析入内存。
因此适合解析一些小型的XML文件。
cElementTree是它的一个C优化过的版本。

示例代码如下：

```py
def readXMLET(filename):
  try:
    import xml.etree.cElementTree as ET
  except ImportError:
    import xml.etree.ElementTree as ET
  tree = ET.ElementTree(file=filename)
  print 'read finish!'
  root = tree.getroot()
  for child in root:
    yield child.tag, child.attrib
```

### BeautifulSoup Parser

刚提到ElementTree不能读取不规范的XML，[BeautifulSoup Parser](http://lxml.de/elementsoup.html)则可以，它试图修复XML中的不规范成分。
但是由于使用了正则表达式，相对的它的效率会低于ElementTree。

示例代码如下：

```py
def readXMLlxml(filename):
  from lxml.html import soupparser

  tree = soupparser.parse(filename)
  root = tree.getroot()
  for child in root:
    yield child.tag, child.attrib
```

### SAX

前面两种方法都是将XML一次以一棵树的形式读入内存中。
若是XML文件较大的话这种方式会非常慢且消耗内存。
[SAX](https://docs.python.org/2/library/xml.sax.html)则是以一种异步的方式处理它遇到的XML标签，而不是将其一次全部解析，因此比较适合体积很大的XML文件。
但是它不会记得之前处理过的标签算是一个缺点。

你需要继承xml.sax.ContentHandler类，然后在解析的时候将这个类的实例传入即可。

这个类有如下方法：

- characters(content)方法：调用时机为从行开始，遇到标签之前，存在字符，content的值为这些字符串；从一个标签，遇到下一个标签之前， 存在字符，content的值为这些字符串；从一个标签，遇到行结束符之前，存在字符，content的值为这些字符串。标签可以是开始标签，也可以是结束标签。

- startDocument()方法：文档启动的时候调用。

- endDocument()方法：解析器到达文档结尾时调用。

- startElement(name, attrs)方法：遇到XML开始标签时调用，name是标签的名字，attrs是标签的属性值字典。

- endElement(name)方法：遇到XML结束标签时调用。

示例代码如下：

```py
class resHandler(xml.sax.ContentHandler):
  def __init__(self):
    self.count = 0

  def startElement(self, tag, attrib):
    if tag == 'doc':
      self.count += 1
      if self.count % 1000 == 0:
        print self.count
      doc = {
        TAG:tag,
        TITLE:attrib[TITLE],
        ANCHOR:attrib[ANCHOR],
        H1:attrib[H1],
        PATH:attrib[PATH],
        PAGERANK:attrib[PAGERANK]
      }
      print doc

def readXMLSAX(filename):
  parser = xml.sax.make_parser()
  parser.setContentHandler(resHandler())
  parser.parse(filename)
```
