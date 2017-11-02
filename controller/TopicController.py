import requests
from bs4 import BeautifulSoup
import re

from controller.QuestionController import QuestionController

class TopicController:

    def __init__(self,url,save_folder):
        """
        :param url:话题路径 
        :param save_folder:保存文件夹 
        """
        self.url = url
        self.folder = float

    def get_html(self,url,data=None):
        headers = {

            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        data = data
        response = requests.get(url, headers=headers)
        html = response.text
        return html

    def get_questions(self,html):
        """

        :param html:
        :return: 问题的地址和名字的list集合
        """
        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.find_all(attrs={'class': 'entry-body'})

        question_list = []
        info = 0
        for item in item_list:
            info +=1
            href = item['href']
            question_name = item.text

            question_item = {
                'info':info,
                'url':'https://www.zhihu.com'+ href,
                'question_name':question_name
            }

            question_list.append(question_item)

        return question_list

    def get_page_nums(self,html):
        soup = BeautifulSoup(html, 'lxml')
        pager_text = soup.find(attrs={'class': 'zm-invite-pager'}).text

        return ''

    def execute(self):
        url = self.url
        data = {
            'page': '1'
        }
        html = self.get_html(url)
        page_nums = self.get_page_nums(html)
        
