+++
date = "2016-04-09T20:00:00+08:00"
title = "单页应用JWT身份认证与XSS及CSRF防范"
categories = ["技术随笔"]
tags = ["程序员", "WEB"]
+++

最近在开发一个单页应用，采用了前后端分离的策略，即后端只提供RESTful接口，前端进行路由，通过Ajax和后端交互。
为了保持RESTful服务的无状态，要避免使用sesseion来保存登录状态，可以使用token方式来进行认证。
这篇博客就来说一下利用JWT(JSON Web Tokens)进行身份认证，以及如何防范MITM，XSS与CSRF攻击。

## [JWT](https://jwt.io/introduction/)

JWT是RFC 7159规范，利用JSON和一种可选的签名算法定义了一种紧凑且自恰的结构。
相比基于XML的SAML方式更加简单紧凑，节省流量且JSON格式方便处理。
相比基于session的认证方式不用在服务器端维护状态，易于扩展；不用查询数据库，性能更好；可以授权给别的应用。
缺点是实现过于复杂，很多语言库都没有实现完整的JWT规范。

JWT由三部分组成，Header.Payload.Signature。

### Header

Header包含签名算法和type，如下：

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Base64编码后即为Header。

### Payload

主体内容部分。有一些保留属性，如iss (issuer), exp (expiration time), sub (subject), aud (audience)等。也可以声明私有属性。

如下：

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```
Base64编码后即为Payload。

### Signature

签名部分，生成过程如下：

```js
alg(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

其中alg为Header中声明的签名算法，常用的如SHA256等。
结合secret校对签名可以保证JWT的完整性和不可伪造性。

### 身份验证过程

后端API除了注册和登录外的需要身份验证的接口都对JWT签名进行验证，不通过则返回401 Unauthorized，保护API。
用户注册登录后生成JWT返回用户，用户访问受保护的API时需要随请求发送JWT至服务器端。

## 两种常见的安全威胁

接下来看看单页应用开发中几种常见的安全威胁：MITM(Man-In-The-Middle)，XSS(Cross-site scripting)和CSRF(Cross Site Request Forgery)。

### [MITM](https://www.owasp.org/index.php/Man-in-the-middle_attack)

MITM是指在数据传输过程中窃听甚至篡改线路中的数据，如窃听WIFI和ARP欺骗等等。
这里我们在应用层主要使用SSL加密，即HTTPS防范它。
在后端response的header的cookie设置`Secure`字段，强制cookie使用HTTPS传输。

### [XSS](https://www.owasp.org/index.php/Cross-site_Scripting_%28XSS%29)

XSS是指将恶意脚本注入站点，如在用户聊天框输入的地方输入如下内容

```html
<img src=x onerror="alert(XSS!)"/>
```

如果不经过滤就显示内容，那么该网页就会执行被注入的脚本，弹出一个alert。

防范XSS的关键是不要信任任何用户提供的内容，对它们进行充分的过滤再使用。
并且在后端response的header的cookie设置`HttpOnly`字段，禁止浏览器Javascript脚本操作cookie。

### [CSRF](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29)

CSRF利用了一个事实，即如`<img>`标签等发起的简单的GET请求是不被同源策略约束的。
如果攻击者在他的页面中加入一个标签如下：

```html
<img src="http://example.com/api/user"/>
```

引诱你访问这个界面后，该标签像example.com的user api发送GET请求，并且会附上你的example.com的cookie，那么攻击者就能得到你在example.com的user信息。

要防范CSRF，主要有两种方式。
可以在后端的response的header中加入`Access-Control-Allow-Origin`白名单，限制跨域访问；
或者使用一些Synchronizer Token技术。
如在用户新建立一个sesseion时产生一个独有的Synchronizer Token，存储在表单的隐藏域、URL参数等地方，JWT的payload中也存储一份。
然后每次请求时前端都通过Javascript脚本发送Synchronizer Token,而这个token攻击者无法获取（除非先进行XSS）。
据此，后端就可以验证前端的身份非攻击者。

## 前端JWT存储

JWT存储有两种方式，localStorage和cookie。

### localStorage

后端返回JWT后，前端存储在localStorage中，每次请求时设置HTTP Authorization Header，使用Bearer scheme，如下：

```
HTTP/1.1

GET /api/user
Host: example.com
Authorization: Bearer Header.Payload.Signature
```

后端验证即可。

存储在localStorage的优点是不使用cookie，避免了JWT被MIMT和CSRF攻击。缺点时localStorage可以被Javascript访问，容易被XSS攻击。

### cookie

后端response的header设置Set-Cookie，如下

```
HTTP/1.1 200 OK

Set-Cookie: token=Header.Payload.Signature Secure; HttpOnly;
```

前端发器跨域请求时，正确设置(见上一篇blog)后会同时附带cookie，后端验证即可。

存储在cookie的优点是在设置了`Secure; HttpOnly;`后防范了XSS和MIMT攻击，但是容易收到CSRF攻击。

## 总结

JWT提供了一种很好的身份验证方式，至于存储在哪里向来有很多争论，这是一个权衡取舍的过程。
