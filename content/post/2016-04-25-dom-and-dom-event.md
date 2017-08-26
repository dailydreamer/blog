+++
date = "2016-04-25T20:00:00+08:00"
title = "DOM和DOM Event"
tags = ["编程", "WEB"]
keywords = ["DOM", "DOM Event", "HTML"]
+++

## DOM和HTML，JavaScript，CSS的关系

[Document Object Model(DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)是W3C制定的一种语言无关的面向对象的文档模型，规定了一组可编程的interface需要实现的属性和方法。
HTML和XML文档实现了DOM，因此拥有面向对象的特性，其结构、样式、内容等可以被其他语言的DOM实现操纵。
DOM Level 4是2015年的最新一版标准。

HTML中`<script>`元素中嵌入的JavaScript就是DOM的一种实现，如下所示：

```js
var paragraphs = document.getElementsByTagName("P");
// paragraphs[0] is the first <p> element
// paragraphs[1] is the second <p> element, etc.
alert(paragraphs[0].nodeName);
```

其中`document`对象，`getElementsByTagName`方法，`alert`方法，`nodeName`属性均是DOM标准规定的。

你也可以用其它语言操作DOM，如下的Python示例：

```py
# Python DOM example
import xml.dom.minidom as m
doc = m.parse("test.xml");
doc.nodeName # DOM property of document object;
p_list = doc.getElementsByTagName("para");
```

HTML是一种文档标记语言，HTML元素除了实现DOM的interface之外，还实现了HTML标准中规定的一些interface。如下示例：

```js
var table = document.getElementById("table");
var tableAttrs = table.attributes; // Node/Element interface
for (var i = 0; i < tableAttrs.length; i++) {
  // HTMLTableElement interface: border attribute
  if(tableAttrs[i].nodeName.toLowerCase() == "border")
    table.border = "1";
}
// HTMLTableElement interface: summary attribute
table.summary = "note: increased border";
```

`attributes`属性是DOM标准，`border`和`summary`属性是HTML标准。

其它XML的方言如SVG等也有实现DOM之外的标准。

CSS是一种为DOM文档标记样式的语言，而DOM Element种的style属性被解释为行内样式表。

## DOM Event

DOM Level 2中规定了基本的[DOM Event Model](https://www.w3.org/TR/DOM-Level-2-Events/events.html)，包括事件的处理流程以及注册方法等等。
这里主要讲一下事件处理流程，感觉和WPF的事件机制很相似。

### 基本流程

在DOM implementation中触发事件后，触发事件的元素EventTarget被指定给Event对象的target属性。
如果该事件没有使用事件捕获和事件冒泡，那么所有的EventListener被执行后事件处理结束。
如果使用了事件捕获或事件冒泡，那么事件传播过程如后文所示，依次执行过程中所有元素上注册的该事件的EventListener。
执行过程是同步的，且一个EventListener内的异常不会影响后续EventListener的执行。

### 事件捕获(Event capture)

事件捕获阶段，事件从DOM树的顶端元素，通常是Document，沿着EventTarget的祖先元素向EventTarget传播。
设置addEventListener方法的useCapture属性为true可以使该EventListener在事件捕获阶段截获由其后代元素产生的相应事件，同时该EventListener在事件冒泡阶段不会再被触发。

注意和WPF等基于delegation的模型不同的是，截获的是后代元素的相应事件，这意味者如果EventTarget上的设置useCapture的EventListener不会被触发，因为自己不是自己的后代；
并且指定的不是一个EventTarget，而是一种特定的事件类型，如果事件类型不同不会被触发。

### 事件冒泡(Event bubbling)

事件冒泡阶段，一开始和没有使用冒泡的事件一样，所有EventTarget上的EventListener都被执行。
然后从EventTarget沿着DOM树，向其祖先元素传播，直到DOM树顶端，过程和事件捕获相反。
设置了useCapture属性的EventListener不会在这一阶段被触发。

事件传播的链条在事件被触发时就已经确定，传播过程中DOM树的改变不影响传播过程。

### stopPropagation

在事件传播的过程中，如果一个EventListener调用了Event对象的stopPropagation方法，那么事件会停止传播，链条上后续元素的EventListener不会被触发。

### preventDefault

一些事件被指定为cancelable。这些事件的DOM implementation通常都会有一些默认的事件处理方法。在这些事件上调用preventDefault方法可以阻止这些事件处理方法的执行。

如下例子展示了用preventDefault阻止非小写字母的输入。

```html
<!DOCTYPE html>
<html>
<head>
<title>preventDefault example</title>
</head>
<body>
<p>请输入一些字母,只允许小写字母.</p>
<form>
<input type="text" id="my-textbox"/>
</form>
<script type="text/javascript">
function checkName(evt) {
var charCode = evt.charCode;
  if (charCode != 0) {
    if (charCode < 97 || charCode > 122) {
      evt.preventDefault();
      alert("只能输入小写字母." + "\n"
            + "charCode: " + charCode + "\n"
      );
    }
  }
}
document.getElementById('my-textbox').addEventListener(
    'keypress', checkName, false
 );
</script>
</body>
</html>
```

### 常用的MouseEvent

有click，mousedown，mouseup，mouseover，mousemove，mouseout。

click是在同一屏幕位置的mousedown和mouseup先后依次触发后被触发。

MouseEvent都会冒泡，并且除mousemove外都Cancelable。
