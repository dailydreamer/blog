+++
date = "2018-11-25T17:43:19-08:00"
title = "Python 并发模型"
tags = ["编程","编程语言"]
keywords = ["并发","asyncio"]
+++

同步的I/O操作会白白消耗很多时钟周期，因此许多编程语言都提供了并发模型来实现异步I/O。今天简单介绍一下Python中的并发模型。

开始之前先澄清一下并发和并行的关系。并发（Concurrency）是指一次处理很多事情，而并行（Parallelism）是指同时做很多事情。并发是处理问题的一种方式，而并行则必须由硬件支持。

![并发和并行](/images/2018-11-25-python-concurrency/concurrent_and_parallelism.png)

## Multi-thread

多线程是最传统的并发模型之一，线程之间通过共享内存来通信，通过互斥锁来防止对临界区域同时读写。

曾经以为由于CPython在实现上采用了GIL（Global Interpreter Lock）来保证线程安全，导致其多线程模型基本不可用。后来了解到Python标准库里所有阻塞I/O函数都会释放GIL，自己编写的函数也可以通过C扩展来释放GIL。所以Python多线程模型在I/O密集型程序中是完全可用的。对于计算密集型程序，可以使用有类似接口的多进程模型处理。

但是多线程模型有一些缺点：
1. 一个线程可能在任何时候被打断，需要上锁，导致很难理解
2. 线程的存储和切换负担相对协程还是较重

为了解决这些问题，Python 3.4引入了asyncio的协程模型。

## asyncio

Python的asyncio使用轻量级的协程作为调度单位，因此可以达到更高并发。同时协程运行过程中天然被保护，必须显示交出控制权（yeild）给其它协程运行，否则不会被打断。

Python的asyncio非常类似于Node.js的Event loop + Async/Await。 Node.js曾尝试使用回调函数并发模型，但是最后因为回调地狱走向了Async/Await。相比于回调，Async/Await还解决了回调context丢失，不好错误处理的问题。

但是asyncio给Python带来了新的问题：生态的分裂。协程链最后会被asyncio的API驱动，比如`loop.run_until_compelte()`；而协程链最开始总是被异步I/O API发起，比如`asyncio.sleep()`或`aiohttp.request()`。因此要使用`asyncio`框架，则需要生态中的所有部分如Web框架、数据库驱动、消息队列、各种客户端等全部用协程重写。目前来看Python的`asyncio`生态还是不够成熟。

## Go Model

当然，其它语言也有着很多不同类型的并发模型。写到这里不得不提一下Golang，作为近些年来热度不断上升的语言，它的并发模型有其独到之处。

Golang实现了CSP（communicating sequential processes) Model。它使用轻量级协程和runtime中的调度器来实现并发，即使其I/O函数是同步的。当一个goroutine阻塞时，runtime调度器会自动切换到其它goroutine，这有点类似于轻量级的多线程模型。不同于多线程模型的是goroutines之间通过channel传递信息通信，而非共享内存，这样来保证同一时间只有一个goroutine访问一个临界区域。正如Rob所说，“Do not communicate by sharing memory; instead, share memory by communicating.”

虽然Golang也存在其它问题，尤其是跟Erlang实现的Actor Model对比时，但是它的成功是显而易见的。

## 结语

本文回顾了Python中不同的并发模型，简略提到了Golang中的并发模型。从来没有一个最好的语言和并发模型，只有最适合的。虽然Golang的高性能和高并发很吸引人，Python的优雅、灵活、快速开发则是其长盛不衰的原因。