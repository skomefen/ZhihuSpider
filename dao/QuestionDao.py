import logging

from dao.ConnManager import ConnManager


class QuestionDao:

    def __init__(self):
        logger = logging.getLogger(__name__)

        conn = ConnManager().get_conn()
        # 表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK:
                sql = 'create table question (id text primary key not null,title text not null,url text not null)'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            logger.debug("question表已存在")
            #print('表已存在')
        finally:
            ConnManager().conn_commit()

    def save_question(self, question):
        logger =  logging.getLogger(__name__)

        try:
            result = self.find_question(question['id'])
            if result:
                self.update_question(question)
                return 
            
            conn = ConnManager().get_conn()
            c = conn.cursor()
            
            sql = 'insert into question (id, title,url) values (?,?,?)'
            u = (question['id'], question['title'],question['url'])
            c.execute(sql, u)
        except Exception as e:
            logger.debug('保存失败，错误:%s',e)
            #print('保存失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()

    def find_question(self, id):
        logger =  logging.getLogger(__name__)

        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from question where id = ?'
            c.execute(sql, (id,))
            question = None
            for row in c:
                question = row
        except Exception as e:
            logger.debug('查询失败，错误:%s',e)
            #print('查询失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
        return question

    def update_question(self, question):
        logger =  logging.getLogger(__name__)

        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update question set title = ?,url = ? where id = ?'
            u = (question['title'],question['url'],question['id'])
            c.execute(sql, u)
        except Exception as e:
            logger.debug('更新失败，错误:%s',e)
            #print('更新失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
