#-*- coding: utf-8 -*-

import cartoon_cat as cc

if __name__ == '__main__':

    site = 'https://m.manhuagui.com/comic/3383/'

    crawler = cc.CartoonCat(
        site=site,                                  # 漫画首页
        begin=0,                                    # 起始章节
        end=-1,                                     # 结束章节
        save_folder='./download',                   # 保存路径，不存在会自动创建
        browser=cc.BrowserType.CHROME,              # 浏览器类型：FIREFOX，CHROME，SAFARI，IE，PHANTOMJS
        driver='./chromedriver'                 # 驱动程序路径，firefox不需要
    )
    crawler.start()

