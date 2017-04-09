+++
date = "2016-06-09T20:00:00+08:00"
title = "从函数式语言想到的"
tags = ["编程", "编程语言"]
+++

最近看了一本书[Seven Languages in Seven Weeks](https://pragprog.com/book/btlang/seven-languages-in-seven-weeks)。
原来一直都在面向对象编程，对函数式语言了解并不多，看完这本书之后还是很受启发，接触了许多不同语言的新的思想。

## 各种编程范式

### imperative programming

古老的编程范式，以冯诺以曼结构的机器思考的方式编程，如C语言。

### object oriented programming

现在正当年的主力编程范式，如Java、C#、ruby、python，以及深度融合了函数式思想但本质还是OOP的scala。

它的分支Prototype-based programming，如JavaScript，是一种十分灵活的编程方式。
没有Class定义，所有的Object都以另一个Object为prototype，可以很灵活的改变原型链上的Object的数据和方法。

### logic programming

面向推理逻辑的特定编程范式，是一种高等级的抽象，如prolog，声明定义和推导即可得出特定问题的答案。

### functional programming

被认为是下一代的编程范式。
函数式编程范式基于lambda calculus的思想，很早就在大名鼎鼎Lisp中出现。
其核心思想是认为一切程序都可以由纯函数组成，纯函数没有副作用，输入一样则输出必然一样；
所有数据结构都是immutable的，其值不能被改变。

早年由于我们的计算机架构是冯诺以曼结构，其基本操作都是基于副作用的，因此这种函数式编程带来的性能上的极大损失使其没有像命令式编程一样成为主流语言。
现在随着计算机性能的提升以及相关理论和实现的完善，函数式编程的思想带来的好处逐渐体现，并且也积极的影响着其它现在的主流语言。
同时涌现了一批为了兼容现有平台而作出一定妥协的”过渡性语言”，如Scala（Better Java）、Clojure（JVM上的Lisp）、F#（.Net上的OCaml）。

## 函数式语言的积极影响

### 基于immutable思想的数据结构

immutable带来的好处是程序的结果更加的可以预测，变量不会在你看不见的地方被偷偷改变。
而且在多核的并行架构下Immutable能够避免复杂的状态和逻辑维护，使程序更加高效简单。

过去Lisp中主要的immutable数据结构是List,在某些情况下这种数据结构的性能非常糟糕（如查找是O(n)）。
而现在一些精巧复杂的树状的数据结构可以兼顾immutable和性能（以一定的存储空间为代价），如[Ideal Hash Trees](https://infoscience.epfl.ch/record/64398/files/idealhashtrees.pdf)中的Hash array mapped trie(HAMT)。
[这篇文章](http://hypirion.com/musings/understanding-persistent-vector-pt-1)详细讲解了Clojure中的Persistent Vectors（虽然叫Vector但只是接口一样，实际这货是个树）的实现原理。
它基于HAMT，能够在保持immutable维护过去状态以供回滚的同时达到增加、更新、查找都为O(1)的性能。
知乎上的[这个讨论](http://www.zhihu.com/question/35244627)介绍了一些其它的相关数据结构。

### 基于immutable的系统

[Nix OS](https://nixos.org/)是一种使用Nix packager manager的纯函数式思想的系统。
Nix packager manager也可以在Linux和Mac OS X上使用。
它将每一个软件包都独立开来，升级软件的时候不会影响原来已经安装好的其它版本的该软件，使得软件可以轻松回滚，并且不会出现由于版本导致的各种问题，是ruby的RVM，node.js的NVM，python的virtualenv等等软件所解决问题的终极解决方案。

### 类型

Haskell拥有强大的类型系统。
static type是指其编译时进行类型检查，strong type是指其类型检查要求类型严格匹配。
配合type inference，Haskell的类型系统做到了你不需要时感受不到，需要清晰接口时可以显示声明。
它永远在保障着程序的正确性，不会产生JavaScript中一些被人广泛诟病的错误（[这个视频](https://www.destroyallsoftware.com/talks/wat)我笑了好久。。。）。
Scala中也有type inference，但是由于JVM的限制功能很有限。

Haskell中的type class可以优雅的实现generics和polymorphism，并且可以避免很多OOP中因为不能把函数作为一等公民传递（高阶函数）而造成的臃肿的设计模式。
Julia中multiple dispatch更进一步，根据每个参数的类型不同调用不同的函数实现，更符合直觉，且避免了OOP中dynamic dispatch的动态查找带来的性能损失。

### 并发

OOP中对于并发的处理通常是基于thread以及共享内存和互斥锁，这个模型被实践证明即使是有经验的程序员也很难驾驭。
而许多函数式语言提出了更好的解决方案。

erlang是为了稳定的企业级基础服务而开发的语言。
erlang虚拟机使得新建进程更加轻量，进程间通讯更加方便。
结合immutable特性以及actor进程池模型和消息传递来解决并发问题。
erlang虚拟机还有一个厉害的特性是能够在语言内轻易管理进程的生命周期，这催生了独特的let it crash哲学，以及不用停止程序即可修改代码等等的神奇功能，使得erlang程序可以运行多年而不用重启。

scala中也使用actor作为并发模型。
clojure中借鉴了关系型数据库的transactional特性，使用software transactional memory管理并发。

这些模型都被实践证明更加容易产生可靠的代码且更容易理解。

### Pattern matching

不同于传统OOP对象相等比较的是引用相等，如Java中String类型的`==`和`equals()`的令人迷惑的区别，Pattern matching是深度比较两个对象，更加符合直觉，并且配合immutable也可以有很好的性能。
当然Pattern Matching更加灵活，带来了匹配类型，destructing等等实用的功能。

### meta programming

Lisp中程序即数据，整个程序就是用List数据结构表达的，使得其macro远远强大于C的字符串替换，可以实现很多优雅的domain specific language(DSL)。
后来很多语言都将macro和meta programming作为自己的重要特性，即使是拥抱了OOP的ruby和scala。

### 其它

如Currying，Functor，Applicative，Monad等等新的概念和抽象，使用Maybe Monad杜绝Null这一Java程序员永远的痛等等。

## 总结

函数式编程为我们带来了更优雅简洁易懂的程序，以及许多优秀的思想。
虽然今天的主流语言仍然是OOP，但是我们可以靠自己慢慢推动新一代编程范式的发展，找到最佳的结合点。

需要注意的是不应该盲目推崇函数式编程的思想。
编程语言里还有另一种实用派，学术派眼中的“另类”，从实际出发得出的迥然不同的语言，如C和go。
不同的思路有着不同的权衡取舍，取其精华去其糟粕，结合自己的使用场景选择，合适的才是最好的。
