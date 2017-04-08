+++
date = "2015-10-30T20:00:00+08:00"
title = "多个github账号的ssh key切换"
categories = ["技术随笔"]
tags = ["程序员", "ssh"]
+++

当拥有多个github账号并且想通过ssh方式同步代码时，就需要在多个账号的ssh key间切换。

## github多个账号ssh key切换

### 配置ssh的config文件

使用`ssh-keygen -t rsa -C "youremail@xxx.com"`生成两个ssh key之后，在~/.ssh/下添加一个config文件，内容如下:

```
Host github.com
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa
Host second.github.com
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa_second
```

### 设置远程仓库的ssh地址

只需要让ssh的目标主机地址变为你写的Host即可。

```sh
git remote add origin git@second.github.com:myname/myrepo.git
```

更加深入的利用ssh config文件可以参考[这篇文章](http://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/)。
