# cartoon-cat

> 小喵发现 tazhe.com 这个网站访问不了了。不知道之后会不会重新开放。那么这么项目暂时就不能正常工作了。。。
> 不过其他的漫画网站的结构其实和 **tazhe漫画** 是差不多的。大家可以参考博客，做一些小的修改就能爬取其他的网站了。
> 
> **补充：**
> 最近又发现了一个网站 36mh.com，正好有想看的一拳超人，于是乎就又改了一下这个工具，居然还可以用，哈哈。
> 只需要修改一下css选择器和结束判断，很爽！


漫画喵

使用selenium + PhantomJs搭建的简单漫画爬虫工具。

博客地址: http://www.miaoerduo.com/python/爬虫-漫画喵的100行逆袭.html

可以用于抓取 https://m.36mh.com 的漫画资源。(这个是手机版的页面，比较容易分析)

需要selenium和浏览器的支持。想试用的童鞋可以看看上述的博客，里面介绍了具体的环境要求。

使用：

在 https://m.36mh.com 上搜索漫画，例如：*一拳超人*

找到相应的漫画，进入。记住漫画的首页地址，这里是：https://m.36mh.com/manhua/yiquanchaoren/

参考demo.py，设置相应的参数：

```python
#-*- coding: utf-8 -*-

import cartoon_cat as cc

if __name__ == '__main__':

    site = 'https://m.36mh.com/manhua/yiquanchaoren/'

    crawler = cc.CartoonCat(
        site=site,                                  # 漫画首页
        begin=0,                                    # 起始章节
        end=-1,                                     # 结束章节，为负数表明不设结束章节
        save_folder='/path/to/download',            # 保存路径，不存在会自动创建
        browser=cc.BrowserType.PHANTOMJS,           # 浏览器类型：FIREFOX，CHROME，SAFARI，IE，PHANTOMJS
        driver='path/to/phantomjs')                 # 驱动程序路径，firefox不需要
                                                    #   其他的可以从 https://pypi.python.org/pypi/selenium 下载
    crawler.start()

```

