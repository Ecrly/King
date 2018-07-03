# King
2018中国软件杯——开源赛题：智能问答系统设计与开发
山东科技大学 计算机科学与工程学院

```
小组名称：“国服路人王”
成    员：陈良、曹广硕、王道远
指导老师：倪维健
```
# 项目文档
## 整体描述
King是一个智能问答系统

由管理系统和移动端两个子项目组成。

系统部署采用分布式提高响应速度。

借助多种算法提高数据挖掘能力以尽可能多和准地提取QA对。
## 系统实现
### 系统部署

![image](https://github.com/dominose/King/blob/master/readme/QQ%E5%9B%BE%E7%89%8720180703212831.png)

系统部署在云服务器中。你可以进入我们的管理平台查看

平台地址[：http://111.231.105.18/main](http://111.231.105.18/main)

### 系统方案
该系统基于Python的Django框架，前端运用jQuery与Bootstrap框架，数据库采用Sqllite，大多数请求基于Ajax异步刷新。
采用的技术主要有：
- Django是一款开源的，基于Python的高级 Web框架，其倾向于快速、整洁与实用的开发风格。Django框架解决了Web开发中大量的琐碎问题，使得开发者可以关注与开发Web应用本身而避免了重复造轮子的痛苦。
- SQLite，是一款轻型的数据库，是遵守ACID的关系型数据库管理系统，它包含在一个相对小的C库中。有ODBC接口，同样比起MySQL、PostgreSQL这两款开源的世界著名数据库管理系统来讲，它的处理速度比他们都快。
- Bootstrap是基于HTML、CSS、JavaScript开发的简洁、直观、强悍的前端开发框架，使得 Web 开发更加快捷。Bootstrap提供了优雅的HTML和CSS规范，它即是由动态CSS语言Less写成。
- Scrapy，Python开发的一个快速、高层次的屏幕抓取和web抓取框架，用于抓取web站点并从页面中提取结构化的数据。Scrapy用途广泛，可以用于数据挖掘、监测和自动化测试。
- Django REST Framework是基于Django的用于创建Web API的一套强大灵活的工具包。本文使用了Django REST Framework并进行了扩展，用以在后台创建一套符合REST规范的Web API。
- SciKit-learn 是老牌的开源 Python 算法框架，始于 2007 年的 Google Summer of Code 项目，最初由 David Cournapeau 开发；它是一个简洁、高效的算法库，提供一系列的监督学习和无监督学习的算法，以用于数据挖掘和数据分析。SciKit-learn 几乎覆盖了机器学习的所有主流算法。
### 系统架构
Django基于MVT的开发模式，如下图所示，其含义为：
- M：即Model，模型层，用于构建和管理Web应用的数据。
- V：即View，视图层，处理用户请求，返回响应信息。
- T：及Template，模板层，渲染响应信息以呈现给用户。
在MVT三层之外，还存在中间件（Middleware）与URL分发器（URL Dispatcher）两部分。其中，URL分发器根据URL配置（URL Conf）调用视图层不同的类或函数来处理请求。中间件作为系统的边界，接收来自Web客户端（如浏览器）的请求，并最终将视图层的响应信息响应给Web客户端。视图层在处理请求时在需要时调用模型层处理数据，调用模板层获得渲染后的响应数据。模型层通过ORM将对模型的操作映射为对数据库的操作。

图。。

Django项目内部以应用（App）为单位将系统划分为不同模块，各模块内拥有独立的MVC结构，URL分发器通过全局的URL配置以及各应用内的URL配置调用特定应用内的视图完成对请求的处理。


### QA对的提取

![image](https://github.com/dominose/King/blob/master/readme/%E6%90%9C%E7%8B%97%E6%88%AA%E5%9B%BE20180703210016.png)


对于一个页面，我们先去除无用信息，然后采用基于启发式规则和无监督学习的网页抽取算法，区分正文与导航，算法思想如下：

基于启发式规则和无监督学习的网页抽取算法（第一类算法）是目前最简单，也是效果最好的方法。且其具有较高的通用性，即算法往往在不同语种、不同结构的网页上都有效。

早期的这类算法大多数没有将网页解析为DOM树，而是将网页解析为一个token序列，例如对于下面这段html源码:


```
<body>
    <div>广告...(8字)</div>
    <div class="main">正文...(500字)</div>
    <div class="foot">页脚...(6字)</div>
</body>
```
程序将其转换为token序列：

```
标签(body),标签(div),文本,文本....(8次),标签(/div),标签(div),文本,文本...(500次),标签(/div),标签(div),文本,文本...(6次),标签(/div),标签(/body)
```

MSS算法(Maximum Subsequence Segmentation)以token序列为基础，算法有多个版本，其中一个版本为token序列中的每一个token赋予一个分数，打分规则如下：
- 一个标签给-3.25分
- 一个文本给1分

根据打分规则和上面的token序列，我们可以获取一个分数序列：


```
-3.25,-3.25,1,1,1...(8次),-3.25,-3.25,1,1,1...(500次),-3.25,-3.25,1,1,1...(6次),-3.25,-3.25
```

MSS算法认为，找出token序列中的一个子序列，使得这个子序列中token对应的分数总和达到最大，则这个子序列就是网页中的正文。从另一个角度来理解这个规则，即从html源码字符串中找出一个子序列，这个子序列应该尽量包含较多的文本和较少的标签，因为算法中给标签赋予了绝对值较大的负分(-3.25)，为文本赋予了较小的正分(1)。



### 智能问答的实现

采用TF-IDF算法，将用户问题与题库中的问题相匹配

TF-IDF（term frequency–inverse document frequency）是一种用于信息检索与数据挖掘的常用加权技术。TF意思是词频(Term Frequency)，IDF意思是逆文本频率指数(Inverse Document Frequency)。

TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降。TF-IDF加权的各种形式常被搜索引擎应用，作为文件与用户查询之间相关程度的度量或评级。除了TF-IDF以外，因特网上的搜索引擎还会使用基于链接分析的评级方法，以确定文件在搜寻结果中出现的顺序。

TFIDF的主要思想是：如果某个词或短语在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。TFIDF实际上是：TF * IDF，TF词频(Term Frequency)，IDF逆向文件频率(Inverse Document Frequency)。TF表示词条在文档d中出现的频率。IDF的主要思想是：如果包含词条t的文档越少，也就是n越小，IDF越大，则说明词条t具有很好的类别区分能力。如果某一类文档C中包含词条t的文档数为m，而其它类包含t的文档总数为k，显然所有包含t的文档数n=m+k，当m大的时候，n也大，按照IDF公式得到的IDF的值会小，就说明该词条t类别区分能力不强。但是实际上，如果一个词条在一个类的文档中频繁出现，则说明该词条能够很好代表这个类的文本的特征，这样的词条应该给它们赋予较高的权重，并选来作为该类文本的特征词以区别与其它类文档。这就是IDF的不足之处. 在一份给定的文件里，词频（term frequency，TF）指的是某一个给定的词语在该文件中出现的频率。这个数字是对词数(term count)的归一化，以防止它偏向长的文件。（同一个词语在长文件里可能会比短文件有更高的词数，而不管该词语重要与否。）对于在某一特定文件里的词语来说，它的重要性可表示为：

![image](https://github.com/dominose/King/blob/master/readme/5ab5c9ea15ce36d3448570f638f33a87e850b177.jpg)

以上式子中分子是该词在文件中的出现次数，而分母则是在文件中所有字词的出现次数之和。

逆向文件频率（inverse document frequency，IDF）是一个词语普遍重要性的度量。某一特定词语的IDF，可以由总文件数目除以包含该词语之文件的数目，再将得到的商取对数得到：

![image](https://github.com/dominose/King/blob/master/readme/a8014c086e061d9552eec4fe79f40ad163d9ca48%20(1).jpg)

具体实现如下：

```
def sim(quest, quest_):
    sents = []
    sents.append(quest_)
    sents.append(quest)
    vectorizer = TfidfVectorizer()
    wget = vectorizer.fit_transform(sents).toarray()
    print("特征向量为：")
    print(vectorizer.get_feature_names())
    va = wget[0]
    vb = wget[1]
    print(va * vb)
    print("句子相似度为：")
    sim = (sum(va * vb) / math.sqrt(sum(va * va) + sum(vb * vb)))
    return sim
```



最后我们筛选出相似性最高的呈现出来，其他则作为可能感兴趣的问题


```
    for qa in qas:
        quest_ = ' '.join(jieba.cut(qa.question))
        sim = bidui(quest, quest_)
        # print(cache)
        if len(cache) < 5:
            cache.append({'sim': sim, 'obj': qa})
            print("目前入队是：", qa.question, "匹配度是：", sim)
        elif len(cache) == 5:
            cache = sorted(cache, key=lambda s: s['sim'])
            if sim > cache[0]['sim']:
                tmp = cache[0]['sim']
                cache.pop(0)
                cache.append({'sim': sim, 'obj': qa})
                print(sim, "替换", tmp)
    cache = sorted(cache, key=lambda s: s['sim'], reverse=True)
```


