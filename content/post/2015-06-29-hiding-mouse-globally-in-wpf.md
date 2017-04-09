+++
date = "2015-06-29T20:00:00+08:00"
title = "WPF全局隐藏鼠标"
tags = ["编程", "编程语言"]
+++

前些日子使用WPF实现了一个填平两个屏幕间缝隙的小程序，在那里面需要让光标在两个屏幕间的时候将其隐藏。
在一个程序内部隐藏鼠标很容易，在WPF中只需设置`Mouse.OverrideCursor = Cursors.None`。
但是当程序最小化后鼠标还能隐藏着实费了一番功夫。
大致有如下几种思路。

1. 将系统的光标图标设置为一个blank.cur的空图标，要显示时再替换回来，这样就可以全局隐藏鼠标，具体方法可以看[这里](http://stackoverflow.com/questions/10541014/hiding-system-cursor)。
但是这种方法有一些问题，一个是需要将系统所有状态的光标图标都替换为空图标，十分繁琐；
而且非常危险，因为一旦你的程序在隐藏鼠标时崩溃，那么鼠标就消失了！
只有重启才能重新显示鼠标。

1. 要隐藏鼠标时将鼠标的位置一直设置在右下角。
这样虽然看不见鼠标了，但是有时会触发侧边栏，尤其是Win8的右边栏；
同时无法知道用户此时已经将光标移动到哪里了，因此也不是非常好用。

1. 最后终于找到了一种十分讨巧的方法。
就是在要隐藏光标的范围内新建一个透明窗口，然后在这个窗口上将光标隐藏。
大致代码如下：

```cs
Window cursorWin;
private void cursorWinInit()
{
    cursorWin = new Window();
    cursorWin.Left = bound - (W + hideBuffer);
    cursorWin.Top = 0;
    cursorWin.Width = 2 * (W + hideBuffer);
    cursorWin.Height = maxHeight;
    cursorWin.ShowInTaskbar = false;            //禁止在任务栏显示
    cursorWin.WindowStyle = WindowStyle.None;   //无边框
    cursorWin.AllowsTransparency = true;        //透明
    cursorWin.Topmost = true;                   //置顶
    cursorWin.Background = new SolidColorBrush(Color.FromArgb(1, 0, 0, 0));     //透明
}
private void myHideCursor()
{
    cursorWin.Dispatcher.Invoke(
        new Action(
            delegate
            {
                cursorWin.Show();
                Mouse.OverrideCursor = Cursors.None;
            }));
}

private void myShowCursor()
{
    cursorWin.Dispatcher.Invoke(
        new Action(
            delegate
            {
                cursorWin.Hide();
                Mouse.OverrideCursor = null;
            }));
}
```
