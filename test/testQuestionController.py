from controller.QuestionController import QuestionController
from dao.save_md import save_md
from view.View import View
from bs4 import BeautifulSoup

base_url = 'https://www.zhihu.com/question/31361871'

spider_dao = save_md()

spider_view = View()

c = QuestionController(url=base_url)


def test_get_html():
    text = c.get_html(base_url)
    soup = BeautifulSoup(text, 'lxml')
    print(soup.prettify())

def test_parse_html():
    text = c.get_html(base_url)
    list = c.parse_html(text)
    print(list)

def test_save_dao():
    c.save_dao('aaaaaaa')

def test_get_answer_nums():
    nums = c.get_answer_num(base_url)
    print(nums)
    print(type(nums))

def test_execute():
    c.execute()

#test_get_html()
#test_parse_html()
#test_save_dao()
#test_get_answer_nums()
test_execute()
