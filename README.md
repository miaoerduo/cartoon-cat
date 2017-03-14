# cartoon-cat

漫画喵

使用selenium + PhantomJs搭建的简单漫画爬虫工具。

博客地址: http://www.miaoerduo.com/python/爬虫-漫画喵的100行逆袭.html

可以用于抓取 http://www.tazhe.com 的漫画资源。

需要selenium和浏览器的支持。想试用的童鞋可以看看上述的博客，里面介绍了具体的环境要求。

使用：

在 http://www.tazhe.com 上搜索漫画，例如：*犬夜叉*

找到相应的漫画，进入。记住漫画的首页地址，这里是：http://www.tazhe.com/mh/8155/

参考demo.py，设置相应的参数：

```python
#-*- coding: utf-8 -*-

import cartoon_cat as cc

if __name__ == '__main__':

    site = 'http://www.tazhe.com/mh/8155/'

    crawler = cc.CartoonCat(
        site=site,                                  # 漫画首页
        begin=0,                                    # 起始章节
        end=-1,                                     # 结束章节，为负数表明不设结束章节
        save_folder='/path/to/download',            # 保存路径，不存在会自动创建
        browser=cc.BrowserType.PHANTOMJS,           # 浏览器类型：FIREFOX，CHROME，SAFARI，IE，PHANTOMJS
        driver='path/to/phantomjs'                  # 驱动程序路径，firefox不需要
                                                    #   其他的可以从 https://pypi.python.org/pypi/selenium 下载
    )
    crawler.start()

```

