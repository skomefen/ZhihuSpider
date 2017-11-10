import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import datetime
import time
import config
from view.View import View
from dao.Dao import Dao

class QuestionController:

    def __init__(self,url,save_file_name=None):
        self.url = url
        self.dao = Dao()
        self.view = View()
        self.save_file_name = save_file_name

    def get_html(self,url=None):
        #driver = webdriver.PhantomJS()

        if url == None:
            url = self.url
        try:
            begin = datetime.datetime.now()
            print('start get page',begin)

            driver = webdriver.PhantomJS()
            driver.get(url)

            page_answer_num = 0
            all_answer_num = self.get_answer_num(url)

            except_num = 0
            while page_answer_num<all_answer_num and except_num < 10:
                try:
                    try:
                        button = driver.find_element_by_class_name('QuestionMainAction')
                        button.click()
                    except Exception as e:
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

                    page_answer_num = driver.find_elements_by_class_name('CopyrightRichText-richText').__len__()

                    print('加载回答数：',page_answer_num,',总回答数：',all_answer_num,',',datetime.datetime.now())
                except Exception as e:
                    print('e:',e,',',datetime.datetime.now(),'等待10分钟')
                    except_num +=1
                    time.sleep(config.ANSWER_ERROR_TIME)
                    
            #留时间加载页面
            time.sleep(3)
            text = driver.page_source

        finally:
            end = datetime.datetime.now()
            print('end get page',end)
            print('花费时间',end-begin)
            driver.close()

        return text

    def parse_html(self,html_text):
        
        start = datetime.datetime.now()
        print('start parse page ',start)
        soup = BeautifulSoup(html_text, 'lxml')
        answer_list_item = []

        list_item = soup.find_all(attrs={'class': 'List-item'})

        info = 0
        for item in list_item:
            info = info +1
            try:
                user_name = item.find(attrs={'class': 'UserLink-link'}).img['alt']
            except Exception as e:
                user_name = '匿名用户' 
                
            try:
                user_icon = item.find(attrs={'class': 'UserLink-link'}).img['src']
            except Exception as e:
                user_icon = 'null'
                
            try:   
                user_home_page = item.find(attrs={'class': 'UserLink-link'})['href']
            except Exception as e:
                user_home_page = 'null'
                
            try:    
                user_introduce = item.find(attrs={'class': 'AuthorInfo-badgeText'}).text
            except Exception as e:
                user_introduce = 'null'
                
            try:    
                answer = item.find(attrs={'itemprop': 'text'}).text
            except Exception as e:
                answer = 'null'

            answer_item = {
                'info':info,
                'user_name': user_name,
                'user_icon': user_icon,
                'user_home_page': user_home_page,
                'user_introduce': user_introduce,
                'answer': answer
            }
            answer_list_item.append(answer_item)
            end = datetime.datetime.now()
            
        print('end parse page',end)
        print('花费时间',end-start)
        return answer_list_item

    def parse_URL(self,url):
        return ''

    def save_URL(self):
        return ''

    def save_dao(self,content,file_name = None):
        self.dao.save(content,file_name)

    def get_answer_num(self, url):

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        text = soup.find(attrs={'class': 'List-headerText'}).span.text
        result = re.match('\d*',text)
        return int(result.group())

    def execute(self):

        bash_url = self.url

        html = self.get_html(bash_url)
        answer_list = self.parse_html(html)

        for answer in  answer_list:
            self.save_dao(answer,self.save_file_name)
