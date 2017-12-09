from threading import Thread
from queue import Queue
from dao.UserDao import UserDao
from dao.QuestionDao import QuestionDao
from dao.TopicDao import TopicDao
from dao.Topic_QuestionDao import Topic_QuestionDao
from dao.AnswerDao import AnswerDao
from dao.ConnManager import ConnManager


class DaoManager:
    
    t = None
    q = Queue()
    __thread_flag__ = True
    
    def svae_dao(self,date_type,date):

        if DaoManager.t == None:
            DaoManager.t = Thread(target=self.__run_dao__,kwargs={})
            DaoManager.t.start()

        DaoManager.q.put({'date_type':date_type,'date':date})

    def quit_run(self):
        
        DaoManager.q.join()
        DaoManager.__thread_flag__ = False
        print('quit run')
            
        

    def set_signal_and_Even(self,signal,event):
        DaoManager.signal = signal
        DaoManager.event = event

    def __run_dao__(self):
        user = UserDao()
        topic = TopicDao()
        question = QuestionDao()
        answer = AnswerDao()
        topic_question = Topic_QuestionDao()

        while self.__thread_flag__:
            date_queue = DaoManager.q
            try:
                date_dict = date_queue.get(timeout=5)
            except:
                continue
            
            date_type = date_dict['date_type']
            date = date_dict['date']
            
            if date_type == 'user':
                user.save_user(date)           
            
            if date_type == 'topic':
                topic.save_topic(date)
                
            if date_type == 'question':
                question.save_question(date)
            
            if date_type == 'topic_question':
                topic_question.save_topic_question(date)
                
            if date_type == 'answer':
                answer.save_answer(date)
                
            #print('queue task done ')

            date_queue.task_done()

        #DaoManager.__thread_flag__ = True
        ConnManager().conn_close()
        print('conn close')
            