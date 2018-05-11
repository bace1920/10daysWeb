# 10daysWeb
**A just-for-learning web framework that can be developed in 10 days.**

# 啰嗦
出于某些原因，我需要一个自己开发的轮子，大约只有十天时间。

于是我打算开发一个python web框架，这是我一直想做却又未完成的事。

我打算每天迭代，一遍写一遍查阅资料，记录新的想法和发现。

这样如果有谁与我处境相似，这个项目也许能够有所帮助。

最好能用成品再搭个博客什么的。

即使没有成功，也不会一无所获。

我们开始吧。

## Day 1
**万事开头难，相信我不是唯一一个在项目开始时感到无从下手的人。**

首先我下载了热门框架Flask的0.1版本的源码，三百余行的代码已经包含了一个web框架所必要的全部功能，还附带了一个使用示例。[如何下载最早的commit代码](#如何下载最早的commit代码)

对于我要实现的第一个最简单版本来说，flask仍然过于复杂了，我只提炼出`route`这个关键部件在第一版中实现。

`Route`用来管理一个web应用具体响应哪些路径和方法。通过装饰器，框架在启动时注册所有的用户函数，并在符合条件时自动调用。

    @testApp.route('/', methods=['GET'])
    def hello():
        return 'hello world'

而`Rule`则具体表示某个需要被响应的路径，它主要由`url`, `methods`和`endpoint`组成。

`methods`包含一系列HTTP Method，表示要处理的请求类型。而`endpoint`则是实际产生返回内容的`Callable`对象，可以是函数或者类。

关于http包含哪些method，以及后续我们需要参考的报文格式和状态码，参见[RFC 2616](#https://tools.ietf.org/html/rfc2616)。

现在我们还缺少一段代码，用于监听和收发http报文，python3.4以后加入的asyncio提供了这个功能，而[官方文档](#http://asyncio.readthedocs.io)恰好给了我们一个极简的示例。

`asyncio.start_server`需要三个基本参数，收到请求时的自动调用的`client_connected_cb`，以及需要监听的地址和端口。

`client_connected_cb`则需要支持两个参数，`reader`和`writer`，份别用于读取请求报文和回写响应报文。

我在`client_connected_cb`中添加了简易的获取请求的路径的代码，用于和注册好的应用函数匹配。

同样我也已经定义了包含所有Http method的宏，不过还没有与请求进行匹配。

这样我们就得到了一个可以运行的"Web框架"，目前只能算是prototype，不过已经足够让我们印出那句世纪名言了。

    Hello World!


## Day 2
**我们有了一个原型，但很多方面亟待完善**

我使用了一个开源第三方库来解析http报文，并实现了`Request`和`Response`来抽象请求。

我从rfc文档中摘取了http的状态码，和methods一起放在`utils.py`中。

尝试定义了一个异常，初步的设向是它可以让框架的使用者随时使用异常直接返回http的错误状态，`content`则是为了支持自定义的错误页面，但这部分仍不确定，也许我会使用`@error_handler`的形式来提供自定义异常时的行为。

添加了log，但在我的终端中还没有输出，待解决。

我使用了标准库`asyncio`，因为我希望这个框架是支持异步的，调整后的`handle`方法提现了处理一个请求的基本思路，但它看起来仍然很糟糕，对于异步我还有很多内容要学习。


## 如何下载最早的commit代码

作为一个知名的开源项目，Flask在github已经积累了数千此提交。

最可恨的是，github在Commit列表页面竟然没有提供一个按页跳转的功能。

下面一个不是很优雅，但确实更快的方法

首先在本地`git clone`下目标项目

使用`--reverse`参数倒置结果，拿到提交历史上最早的commit id

    git log --reverse

在github上随意打开一个commit，替换掉url中的id即可。

哦，你还需要点一下`Browse files`