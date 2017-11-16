from dao.QuestionDao import QuestionDao
from dao.ConnManager import DaoManager

q = QuestionDao()

question = {
    'id': '12',
    'title': 'aaa',
    'url': 'aaa'
}


def test_save_question():
    q.save_question(question)


def test_find_question():
    print(q.find_question('12'))


def test_update_question():
    question['title'] = '22222'
    q.update_question(question)


test_save_question()
test_find_question()
test_update_question()
