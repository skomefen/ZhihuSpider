from dao.AnswerDao import AnswerDao

a = AnswerDao()

answer = {
    'id' : 'aaaa',
    'content':'abcabc',
    'url':'aaa',
    'voters':1000,
    'user_id':'abca',
    'question_id':'abcab'
}

def test_save_answer():
    a.save_answer(answer)

def test_update_answer():
    answer['voters']=2000
    a.update_answer(answer)

def test_find_answer():
    print(a.find_answer('aaaa'))

test_save_answer()
test_update_answer()
test_find_answer()