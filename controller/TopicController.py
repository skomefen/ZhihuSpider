import requests
from bs4 import BeautifulSoup
import re
import threading
import os
import datetime
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

from util.Signal import signal
from dao.Dao import Dao
from util import SpiderUtil


class TopicController:
    def __init__(self, url, save_folder):
        """
        :param url:话题路径 
        :param save_folder:保存文件夹 
        """
        self.url = url
        self.save_folder = save_folder
        self.dao = Dao()

    def get_html(self, url=None, data=None):
        headers = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        if url == None:
            url = self.url
        response = requests.get(url=url, headers=headers, data=data)
        html = response.text
        return html

    def get_questions(self, html):
        """

        :param html:
        :return: 问题的地址和名字的list集合
        """
        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.find_all(attrs={'class': 'question_link'})
        soup.f
        question_list = []
        info = 0
        for item in item_list:
            try:
                href = item['href']
            except KeyError as e:
                continue
            question_name = item.text

            question_item = {
                'info': 0,
                'url': 'https://www.zhihu.com' + href,
                'question_name': question_name.strip()
            }

            question_list.append(question_item)

        return question_list

    def get_page_nums(self, html=None):

        if html == None:
            html = self.get_html(url=self.url)

        soup = BeautifulSoup(html, 'lxml')
        pager_text = soup.find(attrs={'class': 'zm-invite-pager'}).text
        num = int(re.search(".*...\s(\d+)\s", pager_text, re.S).group(1))
        return num

    def save_questions_dao(self, content, save_file_name):

        self.dao.save(content=content, file_name=save_file_name)

    def get_Topic_name(self, html=None):

        if html == None:
            html = self.get_html(url=self.url)

        soup = BeautifulSoup(html, 'lxml')
        topic_name = soup.find(attrs={'class': 'zm-editable-content'}).text
        return topic_name

    def parse_page_question(self,signal,question_queue,page_num):
        data = {
            'page': page_num + 1
        }

        html = self.get_html(url=self.url, data=data)
        question_queue.put(self.get_questions(html))
        signal.signal_num_change(-1)

        print("第 ", page_num + 1, " 页问题爬取完毕：", datetime.datetime.now())

    def join_all_question_list(self,signal, question_list, question_queue, even):
        while True:
            num = signal.get_signal_num()

            if num <= 0 and question_queue.empty():
                break
            question_list.extend(question_queue.get())

        even.set()

    def execute(self):

        start = datetime.datetime.now()
        print('开始爬虫：',start)

        url = self.url
        # 获取话题精华第一页
        html = self.get_html(url)

        # 获取话题精华分页
        page_nums = self.get_page_nums(html)
        # 获取话题名字
        topic_name = self.get_Topic_name(html)


        s = signal(page_nums)

        question_list = []
        question_queue = Queue()
        even = threading.Event()

        with ThreadPoolExecutor(max_workers=10) as executor:

            for num in range(page_nums):
                executor.submit(self.parse_page_question,s,question_queue,num)

            #得到所有页面的问题
            executor.submit(self.join_all_question_list,s, question_list, question_queue, even)

        #等待t1线程完成
        even.wait()
        #去重复
        question_list = SpiderUtil.romve_same_dict_with_list('question_name',question_list)

        index = 0
        for question in question_list:
            index += 1
            question['info'] = index
            print(question)
            self.save_questions_dao(content=question,
                        save_file_name=self.save_folder + os.path.sep + topic_name + '.md')

        end = datetime.datetime.now()
        print("爬虫结束：",end)
        print('花费了：',end-start)

        return question_list