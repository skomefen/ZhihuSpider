from dao.DaoManager import DaoManager
from threading import Thread

m = DaoManager()
answer = {
    'id' : 'asd',
    'content':'abcabc',
    'url':'aaa',
    'voters':1000,
    'user_id':'abca',
    'question_id':'abcab'
}
question = {
    'id': 'asd',
    'title': 'aaa',
    'url': 'aaa'
}
topic = {
    'id': 'asd',
    'title': 'aaaa',
    'url': 'aaa'
}
user = {
    'id' : 'asd',
    'name' : 'xiaoming',
    'fans_num' : 1000,
    'url': 'aaa',
}
topic_question ={
    'topic_id':'asd',
    'question_id':'asd'
}

def test_save_dao():
    Thread(target=m.svae_dao,args=('user',user)).start()
    Thread(target=m.svae_dao,args=('answer',answer)).start()
    Thread(target=m.svae_dao,args=('question',question)).start()
    Thread(target=m.svae_dao,args=('topic',topic)).start()
    Thread(target=m.svae_dao,args=('topic_question',topic_question)).start()


test_save_dao()
m.quit_run()