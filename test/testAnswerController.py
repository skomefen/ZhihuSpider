from controller.QuestionController import QuestionController
from dao.Dao import Dao
from view.View import View

base_url = 'https://www.zhihu.com/question/20363696'

spider_dao = Dao()

spider_view = View()

c = QuestionController(url=base_url, dao=spider_dao, view=spider_view)


def test_get_html():
    text = c.get_html(base_url)
    print(text)

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

test_get_html()
#test_parse_html()
#test_save_dao()
#test_get_answer_nums()

