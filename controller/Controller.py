import requests
from bs4 import BeautifulSoup

import dao.Dao
import view.View
import datetime
import time

class Controller:

    def __init__(self,url,view,dao):
        self.url = url
        self.view = view
        self.dao = dao

    def get_html(self,url,data=None):
        """
        :param url:请求的url地址
        :param data: 请求的参数
        :return: 返回网页的源码html

        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        respon = requests.get(url, data,headers = headers)
        return respon.text

    def parse_html(self,html_text):
        soup = BeautifulSoup(html_text, 'lxml')

        # print(soup.prettify())
        answer_list_item = []

        list_item = soup.find_all(attrs={'class': 'List-item'})

        for item in list_item:
            user_name = item.find(attrs={'class': 'UserLink-link'}).img['alt']
            user_icon = item.find(attrs={'class': 'UserLink-link'}).img['src']
            user_home_page = item.find(attrs={'class': 'UserLink-link'})['href']
            user_introduce = item.find(attrs={'class': 'AuthorInfo-badgeText'}).text
            answer = item.find(attrs={'itemprop': 'text'}).text

            answer_item = {
                'user_name': user_name,
                'user_icon': user_icon,
                'user_home_page': user_home_page,
                'user_introduce': user_introduce,
                'answer': answer
            }
            answer_list_item.append(str(answer_item))

        return answer_list_item

    def parse_URL(self,url):
        return ''

    def save_URL(self):
        return ''

    def save_dao(self,content):
        self.dao.save(content)

    def get_answer_nums(self):
        return 1

    def execute(self):

        bash_url = self.url
        answer_nums = self.get_answer_nums()

        html = self.get_html(bash_url)
        answer_list = self.parse_html(html)

        for answer in  answer_list:
            self.save_dao(answer)
