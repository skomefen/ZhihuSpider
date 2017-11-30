import requests
import re
import datetime
import time
import uuid

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf import config
from view.View import View
from dao.save_md import save_md
from dao.DaoManager import DaoManager


class QuestionController:

    def __init__(self,url,save_file_name=None):
        '''
        
        :param url: 
        :param save_file_name: 如果不为空则保存为md文件，为空就保存在数据库
        '''
        
        self.url = url
        self.save_md = save_md()
        self.dao_manager = DaoManager()
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
            max_answer_num = self.get_answer_num(url)
            #限制爬取回答数量
            if max_answer_num > config.MAX_ANSWER_NUM:
                max_answer_num = config.MAX_ANSWER_NUM

            except_num = 0
            while page_answer_num<max_answer_num and except_num < 10:
                try:
                    flag = False
                    try:
                        button = driver.find_element_by_class_name('QuestionMainAction')
                        button.click()
                    except Exception as e:
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

                    #显示等待10s，等待这个元素加载完毕，页面应该就加载完了
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "CornerAnimayedFlex"))
                    )

                    page_answer_num = driver.find_elements_by_class_name('CopyrightRichText-richText').__len__()

                    print('加载回答数：',page_answer_num,',总回答数：',max_answer_num,',',datetime.datetime.now())
                except Exception as e:
                    print('e:',e,',',datetime.datetime.now(),'等待',config.ANSWER_ERROR_TIME,'秒')
                    flag = True

                finally:
                    #貌似python错误处理之后就直接while下一个了，所以把等待时间丢到finally里
                    if flag:
                        except_num +=1
                        time.sleep(config.ANSWER_ERROR_TIME)

            text = driver.page_source

        finally:
            end = datetime.datetime.now()
            print('end get page',end)
            print('花费时间',end-begin)
            driver.quit()

        return text

    def parse_html(self,html_text):
        
        start = datetime.datetime.now()
        print('start parse page ',start)
        soup = BeautifulSoup(html_text, 'lxml')
        result_list_item = []

        list_item = soup.find_all(attrs={'class': 'List-item'})

        for item in list_item:

            try:
                result = item.find(attrs={'class': 'UserLink-link'})['href']
                user_id = re.match('^/people/(.+)$', result).group(1)
            except Exception as e:
                user_id = '匿名用户_' + str(uuid.uuid1())

            try:
                user_name = item.find(attrs={'class': 'UserLink-link'}).img['alt']
            except Exception as e:
                user_name = '匿名用户'

            #要获取粉丝数得进入用户主页，省内存，没获取之前就-1
            fans_num = -1

            try:   
                user_url = item.find(attrs={'class': 'UserLink-link'})['href']
            except Exception as e:
                user_url = 'null'

            try:
                answer_url = item.find(attrs={'class':'ContentItem-time'}).a['href']

                result = re.match('^/question/(\d+)/answer/(\d+)$', answer_url)

                answer_id = result.group(1)+'_'+result.group(2)
                question_id = result.group(1)

            except Exception as e:
                print('读取回答出错,没有获取answer_url')
                continue

            try:
                content = item.find(attrs={'itemprop': 'text'}).text
            except Exception as e:
                print('读取回答出错，没有获取content')
                continue

            try:
                result = item.find(attrs={'class': 'Voters'}).text
                voters = re.match('^(\d+).+', result).group(1)
            except Exception as e:
                voters = 0
                
            user = {
                'id': user_id,
                'name': user_name,
                'fans_num': fans_num,
                'url': 'https://www.zhihu.com' + user_url,
            }

            answer = {
                'id': answer_id,
                'content': content,
                'url': 'https://www.zhihu.com' + answer_url,
                'voters': voters,
                'user_id': user_id,
                'question_id': question_id
            }

            result_list_item.append({'user':user,'answer':answer})

            end = datetime.datetime.now()
            
        print('end parse page',end)
        print('花费时间',end-start)
        return result_list_item

    def parse_URL(self,url):
        return ''

    def save_URL(self):
        return ''

    def save_md(self,content,file_name = None):
        self.save_md.save(content,file_name)


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
        result_list = self.parse_html(html)
        
        if self.save_file_name:
            for item in  result_list:
                self.save_md(item['answer'],self.save_file_name)
            return 
                
        for item in  result_list:   
            self.dao_manager.svae_dao('user',item['user'])
            self.dao_manager.svae_dao('answer',item['answer'])


        
