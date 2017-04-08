+++
date = "2016-04-14T20:00:00+08:00"
title = "CSS Cheat Sheet"
categories = ["技术随笔"]
tags = ["程序员", "WEB"]
+++

## HTML

block element块级元素，撑满一行

inline element行内元素，宽度包围内容

## CSS原理

### 选择符

a, b {} 同时选中a和b

a b {} a是b的祖先元素时选中b

a > b {} a是b的父元素时选中b

a + b {} a紧邻b时选中b

a ~ b {} a和b是同胞时选中b

\* {} 全部选中

.a {} 选中a类

#a {} 选中id为a

a.b {} 选中同时为a标签和b类

.a.b {} 选中同时为a类和b类

a[b] {} 选中a标签中带有b属性的

a[b=c] {} 选中a标签中b属性值为c的

#### 伪类

a标签 a:link a:visited a:hover a:active

a:focus a:target

一组同胞元素中的第几个 a:first-child a:last-child a:nth-child(n) a:nth-child(odd) a:nth-child(even)

#### 伪元素

a::first-letter a::first-line

a::before a::after

搜索引擎不会索引伪元素

#### 继承

字体颜色等相关属性会继承，位置等相关属性不会继承

### 浏览器层叠样式表顺序

1. 浏览器默认
2. 用户样式表
3. 作者链接样式表（按链接先后顺序）
4. 作者嵌入样式表
5. 作者行内样式表

特指度：包含多少标签、类名、ID等（I-C-E三位数），特指度高的优先级高

特指度相同时顺序靠后的优先级高

### CSS属性

文本值

数字值

1. px 像素
2. em 字体中M的宽度
3. ex 字体中x的高度
4. 百分比

颜色值（颜色名，RGB，HSL，16进制）

## 定位元素

垂直外边距叠加：垂直方向相邻两个box取margin较大的作为外边距

```css
p {
  font-size: 1em;
  margin: .75em 30px;
}
```

如上排版文字最好垂直相对外边距，水平绝对外边距

给设定了宽度\高度的盒子加边框、内边距、外边距会使盒子更宽\更高。CSS3的box-sizing属性可以消除这一特点。

### position

1. static：普通文档流
2. relative: 仍然在文档流中，相对原来的box位置变化，原来box占据的位置不变
3. absolute：从文档流中脱出，会随页面滚动
4. fixed：从文档流中脱出，不会随页面滚动

定位上下文：带有非static position的最近祖先元素，默认是body。

### display

1. inline
2. block
3. none（空间会被回收）

最近支持越来越好的flexbox布局，值得有空仔细研究。

### background

1. background-repeat
2. background-size
3. background-attachment

css3支持多张背景图片，先列出的在上层

背景渐变

## 字体和文本

em相对最近的被设置过字体的祖先大小

CSS3 rem相对root即body字体大小

1. text-indent
2. text-align
3. vertical-align: sub(下标) super(上标) top middle bottom

Web字体

## 界面组件

label的for属性可以把标签和控件关联起来

fieldset表单域

用section块级元素包裹label和input

## 响应式布局

### 媒体查询

媒体类型：all handled print screen 等

媒体特性：max-device-width max-width orientation

and not all 等逻辑运算符
