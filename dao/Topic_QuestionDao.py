from dao.ConnManager import DaoManager


class Topic_QuestionDao:

    def __init__(self):
        conn = DaoManager().get_conn()
        # 表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK:
                sql = 'create table topic_question (topic_id text not null,question_id text not null,primary key (topic_id,question_id))'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            print('表已存在')
        finally:
            DaoManager().conn_commit()

    def save_topic_question(self, topic_question):

        conn = DaoManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'insert into topic_question (topic_id, question_id) values (?,?)'
            u = (topic_question['topic_id'], topic_question['question_id'])
            c.execute(sql, u)
        except Exception as e:
            print('保存失败,或者该数据已存在，错误:' + e)
        finally:
            # conn.commit()
            DaoManager().conn_commit()


