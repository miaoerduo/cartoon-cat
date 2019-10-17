# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib2
import logging
import os
from os import path as osp


class Enum(tuple):
    __getattr__ = tuple.index


BrowserType = Enum(['FIREFOX', 'CHROME', 'IE', 'SAFARI', 'PHANTOMJS'])


class CartoonCat:
    def __init__(self, site, begin=0, end=-1, save_folder="download", browser=BrowserType.FIREFOX, driver=None):
        """
        :param site: 漫画的首页面
        :param begin: 章节的开始(含),0表示第一章
        :param end: 章节的结束(含),-1表示到结尾
        :param browser: 浏览器类型
        :param driver: 驱动，如果驱动程序在可访问的位置，这个参数非必须，对于PhantomJs，驱动程序就是改程序的地址
        """

        self.__site = site
        self.__begin = begin
        self.__end = end
        self.__save_folder = save_folder
        self.__chapter_list = []

        if not osp.exists(self.__save_folder):
            os.mkdir(self.__save_folder)

        if BrowserType.FIREFOX == browser:
            self.__browser = webdriver.Firefox()
        elif BrowserType.CHROME == browser:
            self.__browser = webdriver.Chrome(driver)
        elif BrowserType.IE == browser:
            self.__browser = webdriver.Ie(driver)
        elif BrowserType.SAFARI == browser:
            self.__browser = webdriver.Safari(driver)
        elif BrowserType.PHANTOMJS == browser:
            self.__browser = webdriver.PhantomJS(driver)
        else:
            raise TypeError('UNKNOWN BROWSER TYPE: %s' % browser)

        self.__get_chapter_list()

        if self.__begin >= len(self.__chapter_list) \
                or (0 <= self.__end < self.__begin):
            raise Exception('the begin and end index of chapter is illegal')

        logging.basicConfig(format='[%(asctime)s] %(levelname)s::%(module)s::%(funcName)s() %(message)s', level=logging.INFO)

    def __del__(self):
        self.__browser.quit()

    def __get_chapter_list(self):
        """
        获取章节信息
        :return: None
        """

        self.__browser.get(self.__site)
        chapter_elem_list = self.__browser.find_elements_by_css_selector('.comic-chapters .list ul li a')
        for chapter_elem in chapter_elem_list:
            self.__chapter_list.append((chapter_elem.text, chapter_elem.get_attribute('href')))

    @staticmethod
    def __download(url, save_path, try_time=3, timeout=30):
        """
        下载
        :param url:
        :param save_path:
        :param try_time:
        :param timeout:
        :return:
        """
        while try_time > 0:
            try:
                content = urllib2.urlopen(url, timeout=timeout).read()
                with open(save_path, 'wb') as fp:
                    fp.write(content)
                break
            except Exception as et:
                logging.error(et, exc_info=True)
                try_time -= 1
                if try_time == 0:
                    logging.error('cannot download: %s to %s' % (url, save_path))

    def download_chapter(self, chapter_idx, save_folder=None):
        """
        下载章节
        :param chapter_idx: 章节id
        :param save_folder: 保存路径
        :return:
        """

        chapter = self.__chapter_list[chapter_idx]

        save_folder = save_folder if save_folder is not None else self.__save_folder

        chapter_title = chapter[0]
        chapter_url = chapter[1]

        logging.info('#### START DOWNLOAD CHAPTER %d %s ####' % (chapter_idx, chapter_title))

        save_folder = osp.join(save_folder, chapter_title)
        if not osp.exists(save_folder):
            os.mkdir(save_folder)

        image_idx = 1
        self.__browser.get(chapter_url)

        while True:
            image_div = self.__browser.find_element_by_css_selector('mip-img')
            image_url = image_div.get_attribute('src')
            save_image_name = osp.join(save_folder, ('%05d' % image_idx) + '.' + osp.basename(image_url).split('.')[-1])
            self.__download(image_url, save_image_name)

            image_div.click()       # 跳转页面

            # 页面结束会跳回首页，而首页的url不是html结尾，可用于判断章节是否爬取完。
            if not self.__browser.current_url.endswith('html'):
                break
            image_idx += 1

        logging.info('#### DOWNLOAD CHAPTER COMPLETE ####')

    def get_chapter_list(self):

        return self.__chapter_list

    def start(self):
        begin = self.__begin if self.__begin >= 0 else 0
        end = self.__end if self.__end >= 0 else len(self.__chapter_list)

        for chapter_idx in xrange(begin, end):
            self.download_chapter(chapter_idx)
