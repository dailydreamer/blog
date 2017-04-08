+++
date = "2016-04-08T20:00:00+08:00"
title = "CORS解决单页应用跨域问题"
categories = ["技术随笔"]
tags = ["程序员", "WEB"]
+++

## [同源策略](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)

最近在开发一个单页应用，采用了前后端分离的策略，即后端只提供RESTful接口，前端进行路由，通过Ajax和后端交互。
这时前端和后端部署在不同的服务器上。
而浏览器为了安全，运行在浏览器中的Javascript脚本受到同源策略限制。

同源是指协议+主机名+端口号全部相同，称为同源。
详细见下表，是跟"http://www.example.com/dir/page.html"做比较。

| Compared URL | Outcome | Reason |
| :----------- | :------ | :----- |
| http://www.example.com/dir/page2.html	| Success |	Same protocol, host and port |
| http://www.example.com/dir2/other.html | Success | Same protocol, host and port |
| http://username:password@www.example.com/dir2/other.html | Success | Same protocol, host and port |
| http://www.example.com:81/dir/other.html | Failure | Same protocol and host but different port |
| https://www.example.com/dir/other.html | Failure | Different protocol |
| http://en.example.com/dir/other.html | Failure | Different host |
| http://example.com/dir/other.html | Failure | Different host (exact match required) |
| http://v2.www.example.com/dir/other.html | Failure | Different host (exact match required) |
| http://www.example.com:80/dir/other.html | Depends | Port explicit. Depends on implementation in browser |

Javascript不能访问非同源下的资源，如cookie，localstorge等，这也意味着ajax请求后返回的数据会被浏览器认为是非同源而禁止Javascript操作。
通常的解决方法有JSONP(JSON with Padding)和CORS(Cross-origin resource sharing)。
当然如果要求实时性的话也可以考虑WebSocket协议，这点本文不展开。

## [JSONP](https://en.wikipedia.org/wiki/JSONP)

HTML标准里的`<script>`标签，它可以调用部署在CDN上或其他服务器上的非同源Javascript。
JSONP实际上是利用了这一点，和服务器端约定，在发送请求时加入了一个回调函数的参数。
如Jquery中设置参数`dataType: "jsonp"`后，请求相当于插入页面如下标签

```html
<script src="http://www.example.net/api/example?callback=mycallback"></script>
```

服务器端返回的payload为`mycallback(data)`，通过`<script>`标签执行，就完成了ajax请求。

JSONP的优点是实现简单，兼容性很好。
缺点是只支持GET请求。

## [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS)

CORS是W3C推荐的跨域HTTP请求的新机制，它可以支持如下请求：

- XMLHttpRequest(即ajax请求)
- Web Fonts
- WebGL textures
- canvas中drawImage产生的Images/video frames
- CSS
- Scripts

### 简单请求

简单请求，是指满足如下条件的请求：

只允许如下方法：

- GET
- HEAD
- POST

除了浏览器自动设置的属性（如Connection, User-Agent等), 只允许设置如下头部属性：

- Accept
- Accept-Language
- Content-Language
- Content-Type

只允许如下Content-Type值:

- application/x-www-form-urlencoded
- multipart/form-data
- text/plain

对于简单请求，要允许CORS，需要在后端返回的response的header中设置`Access-Control-Allow-Origin`允许前端服务器地址的ajax请求，可以使用通配符或白名单。
如`Access-Control-Allow-Origin: *`允许所有跨域请求，`Access-Control-Allow-Origin: http://example.com`允许前端服务器example.com的跨域请求。

发送CORS跨域请求默认不带cookie。
可以设置request的header中xhr对象` withCredentials: true`一同发送cookie，同时后端返回的response的header中设置`Access-Control-Allow-Credentials: true`接收cookie。
注意使用cookie时`Access-Control-Allow-Origin`的值不能是通配符`*`。

### Preflighted requests

除了简单请求外的请求都是复杂请求。
在发送复杂请求之前需要先发送一个OPTIONS方法的Preflighted requests，后端确认安全后再发送正式请求。
具体设置可以参考[W3C推荐标准](https://www.w3.org/TR/cors/)。
