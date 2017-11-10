from controller.TopicController import TopicController

base_url = 'https://www.zhihu.com/topic/20018196/top-answers'

c = TopicController(url=base_url,save_folder='aaa')

def test_get_html():
    print(c.get_html(url=base_url))

def test_get_questions():
    html = c.get_html()
    print(c.get_questions(html))

def test_get_page_nums():
    html = c.get_html()
    print(c.get_page_nums(html))

def test_save_questions_dao():
    c.save_questions_dao("aaaa","aaaa.md")

def test_get_Topic_name():
    html = c.get_html()
    print(c.get_Topic_name(html))

def test_execute():
    c.execute()
#test_get_html()
#test_get_questions()
#test_get_page_nums()
#test_save_questions_dao()
#test_get_Topic_name()
test_execute()
