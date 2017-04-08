+++
date = "2016-03-20T20:00:00+08:00"
title = "一种新科学"
categories = ["读书笔记"]
tags = ["科学"]
+++

本书作者是Mathematica之父Stephen Wolfram。
他在完成Mathematica后挣了一大笔钱，然后几十年一直在搞自己喜欢的研究和探索，最终著成本书（论经济基础对研究的重要性）。
虽然书中的研究缺少确实的证据而更多的是作者的猜测，但是以目前的科学也不足以证伪。
不过有计算复杂性科学家发过[paper](http://scottaaronson.com/papers/nks.pdf)评判这种没有同行评阅和修改的出书模式，并且质疑了其内容的价值。
但是作为思路开阔一读也未尝不可。

而且这本书实在是太长了，并且充满了各种论断但是缺少证据，最终没有看完，日后有机会再补完。

## The Foundation for a New Kind of Science

实际上系统理论没必要必须建立在传统数学规律之上。
使用传统数学规则经常无法使用简单的规则解释复杂的自然现象，但是遵从简单规律的程序却可以产生复杂的结果。

Principle of Computational Equivalence: Whenever one sees behavior that is not obviously simple - in essentially any system - it can be thought of as correspoding to a computation of equivalent sophitication.

这个原理揭示了传统数学规则的局限性，它只能解释简单的系统因为它大大简化了计算复杂度。

现在的物理太依赖连续的数学表示或概率，但是离散的其实更简单，并且可以解释很多基本现象。

现在数学不能解释复杂的生物系统，而简单程序可以。

A new kind of science不仅能够解释各个学科的复杂问题，也能对经典的基础问题进行解释。

## The Crucial Experiment

### How do simple program behave?

细胞自动机即使从简单条件开始，遵从简单条件发展，也会展示惊人的复杂性，正如我们在自然中看到的。

尽管每个cell都遵从相同的规律，但是因为环境的不同，它们的行为也不同。

### The need for a new intuition

细胞自动机的复杂性与我们认为一个复杂事物必然构成复杂的直觉相反，而这种直觉可能来自于工程中，那里我们从功能出发，逐步将系统分解到细节，我们能预测系统的一切行为。
但是却不是这样，事实上类似细胞自动机这种不可预测的结构在自然中很常见。

### Why these discoveries were not made before

早期计算机太昂贵，而这些工作没有传统科学框架下的意义。

既需要基础科学的知识，又需要计算科学的经验和直觉。

许多发现都指向了new kind of science，如二维细胞自动机the game of life，但是都被人们忽略了。

## The world of simple programs

二色一维两个邻居的细胞自动机有256种情况，三色有3^8种情况，但是其中的模式大都类似。

Mobile Automata: 一次只有一个active cell，下一步active cell左移或右移。

active cell越多，越容易有复杂性。

Turing machine, Substitution system…

系统依赖的规则稍加复杂，结果就显示出惊人的复杂性，但是之后依赖规则再复杂也不会有太大的不同。

大量的实验，简单的实验适合用计算机编程，但同时也可能模拟复杂现象。

## System based on numbers

2进制digital sequence显示出和细胞自动机相似的复杂性。

递归序列、素数序列等等...

连续的细胞自动机，微分方程，连续的系统也能产生复杂的结构。

## Two dimensions and beyond

二维三维的系统有类似的复杂性。

基于限制的系统，也是当规则复杂到3*3时才会产生随机现象。

传统数学规律大多基于限制，因此难于发现复杂性。

## Starting from randomness

随机开始的细胞自动机会最终归于4个模式。

## Mechanisms in programs and nature

### University of behavior

自然中的一些复杂性和细胞自动机中表现出的模式相同。

### Three mechanisms of randomness

三种导致随机的机制：每一步输入均随机、初始输入(敏感)随机、无外界随机因素intrinsic randomness generation。
船在水上的运动是第一种，混沌效应是第二种，第三种有rule 30自动机，伪随机数生成器，自然界中最常见第三种。

实际设备的问题限制了随机性的观测，即内部状态恢复的速率和不可避免的相关性。

Mathematica使用rule 30细胞自动机产生随机数。。。

大部分随机数生成器使用multiplier 65539 linear congruential generators，因为它更易被数学分析，但是有最大重复间隔使得不是完全随机。

intrinsic randomness generation和自然界随机的共同特征是可重复实验，而其他两种机制则不可重复。

intrinsic randomness generation对扰动的容忍程度大于第二种机制，而实际系统中总是有扰动的。

### The phenomenon of continuity

宏观上看起来连续的系统微观上也可能是离散的，如水流和风等。

这样的原因之一是随机性。

### Origins of discreteness

连续的系统也能引起离散的行为，如量变引起质变的烧开水。

### The problem of satisfying constraints

基于限制的大都只能产生简单的现象。

### Origins of simple behavior

uniformity, repetition, nesting都可以从各种机制中产生。

## Implications for everyday system

### Issues of modeling

为日常生活中的复杂现象通过简单程序的规则建模。

模型可以是粗略的描画复杂现象的轮廓，而不必使得模型内部的部分对应于实际系统的部分。

传统模型大多是数学等式的集合，因而不能很好的刻画复杂现象；
传统模型很难轻松得到结果，由于连续不能直接运行在计算机上。
而简单程序模型就没有这些问题。

### The growth of crystals

用二维六边形细胞自动机模拟雪花生成结构。

### Fluid flow

只要粒子和动量的数量级一致，即使是高度粒子模型也能显示出湍流的行为。

传统的数学解释认为湍流系统是出事输入敏感的，但是细胞自动机模型却不这么假设。
这也更符合实际现象。

### Fundamental Issues in Biology

从部分organism角度看生物，在显微镜规模下，就是简单程序的细胞自动机。

自然选择也许类似于工程，倾向于原则简单而可控的部件和规则，避免过度的复杂性。

而复杂的高等动物则是自然选择的搜索过程中的一些随机采样的结果，因为没有引入缺陷而保留了下来。

## Fundamental Physics

能否抛开现有的物理体系使用简单程序构建起新的物理体系。

### The Notion of Reversibility

只有一少部分细胞自动机是可逆的，但是系统仍然展示了高度的复杂性。

### Irreversibility and the Second Law of Thermodynamics

粒子物理可逆但是很多自然现象不可逆，并且演变的越来越随机越复杂。

根据简单程序模拟，越来越复杂是因为初始情况设置的简单。

自然现象的初始情况都很简单，是因为初始情况的计算复杂性应该要小于实验过程。

如果系统产生了足够的随机性，可以认为它们之间的趋同使得它们的属性跟初始条件无关。
这使得现在我们可以使用很少的参数来近似表示一些物理系统。

但是自然中，尤其是生物系统存在一些不遵热力学第二定律，即越来越复杂的系统，否则宇宙就变得趋同了，而不是现在这样多样。

根据37号自动机观察所得，热力学第二定律不是普适的。
宇宙持续变大，一些信息被忽略，自成一个有组织的小系统独自发展，然后相互重复。

### Ultimate models for the universe

根据本书发现，宇宙的终极模型可能依赖于简单的规则。

如何发现这个规则呢？根据物理现象推倒超出计算能力范围，因此试图遍历所有可能的简单模型看能否产生想要的宇宙的结果。

现在发现的规律很可能都是终极模型的表象。

### The nature of space

宇宙空间很可能是离散的。而过去一直认为是连续的，因为传统数学善于计算这种模式。

### Space as a network

空间可能是由节点网络构成的。

节点的距离和网络的维度有关。

### The relationship of space and time

现代物理倾向于认为时间和空间本质相似，是时空第四维。
但是时间和空间的相似性很可能是不够小的实验数据导致的。
探索后作者发现在最本质上时空分离，就像元胞自动机的演化。

## Time and causal metwork

时空很可能是一种mobile automaton或图灵机，一次之更新一个单元。

但是对于图灵机内部的单元来说，他察觉到变化时已经更新了一轮，因此感觉不到一次只更新了一个。

## 我的结论

我就看到这里为止了，总的来说提供了一种新颖的离散化的思想。
世界就是一种巨大的计算机，谁都曾经这么想过，但是Wolfram对其进行了更深入的探讨。
蕴含其中的是宇宙遵循着简单的规则，这和许多科学家是相同的。

后面几章引用一下[豆瓣的书评](https://book.douban.com/review/1287160/)，留待以后补完。


>9.Fundamental Physics
我认为这章的内容很重要，首先，我们要有一个信念：这个世界就是一个计算机，每一件事情都是计算。
在这个前提下，我们来看世界，怎样的宇宙才是从程序上最可行的呢？
作者探讨了空间网络、因果网络等模型。
究竟宇宙是不是一太计算机，我们实际上不能证伪，但是如果从程序的角度出发，却发现我们可以从一个完全不同的角度得到很多疑难问题的解答。
在因果网络模型下，相对论、量子论等等都是系统涌现出来的一种结果。
如果这一切正确的话，我们自然能得到一个统一量子论和相对论的工具。
另外，本章提出来的时空观是非常关键的，因果网络是最本质的东西，时间和空间甚至都是涌现出来的现象。

>10.Processes of Perception and Analysis
讲述把细胞自动机应用到计算机科学、人工智能、信息处理等领域的具体方法。
视觉感知、加密解密、思维过程等等都有涉猎。

>11.The Notion of Computation
究竟什么是计算？在很早，丘奇图灵论题就指出，一切与图灵机等价的过程就是计算。
那么细胞自动机与图灵机那个更强呢？
通过作者特别的证明（运用图形和说明，而不是数学推导），我们看到一类特制的细胞自动机可以模拟任何一台其他的细胞自动机，而且还能模拟图灵机以及其他的计算系统。
翻过来，图灵机和其他计算模型也都能模拟细胞自动机。
实际上能够执行通用计算的机器仅仅需要简单的规则，也就是101号细胞自动机。
作者认为101细胞自动机非常重要，因为它规则简单，而且能够模拟任意的复杂计算过程。

>12.The Principle of Computational Equivalence
本章提出了一个猜想：The Principle of Computational Equivalence，也就是计算等价性原理，作者认为宇宙的一却活动都是一种计算，而且能够完成复杂计算的过程都是等价于通用计算的，所以，原则上讲，细胞自动机110能够模拟任何一个复杂的计算过程。
作者当然也讨论了哥德尔定理、不可判定问题，认为对于第四类细胞自动机，我们除了运行它以外，根本无法判定它在未来的行为，即使在原则上，因为它是不可判定的问题。
