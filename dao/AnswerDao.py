from dao.ConnManager import DaoManager


class AnswerDao:

    def __init__(self):
        conn = DaoManager().get_conn()
        # 表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK:
                sql = 'create table answer (id text primary key not null,title text not null,context text, voters integer,user_id text,question_id text)'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            print('表已存在')
        finally:
            DaoManager().conn_commit()

    def save_answer(self, answer):
        try:
            self.find_user(answer['id'])
            self.update_user(answer)
        except:
            conn = DaoManager().get_conn()
            c = conn.cursor()
            try:
                sql = 'insert into answer (id, title, context,voters,user_id,question_id) values (?,?,?,?,?,?)'
                u = (answer['id'], answer['title'], answer['context'], answer['voters'], answer['user_id'], answer['question_id'])
                c.execute(sql, u)
            except Exception as e:
                print('保存失败，错误:' + e)
            finally:
                # conn.commit()
                DaoManager().conn_commit()

    def find_answer(self, id):
        conn = DaoManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from answer where id = ?'
            c.execute(sql, (id,))
            for row in c:
                user = row
        except Exception as e:
            print('查询失败，错误:' + e)
        finally:
            # conn.commit()
            DaoManager().conn_commit()
        return user

    def update_answer(self, answer):
        conn = DaoManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update answer set title = ?,context = ?,voters = ?,user_id = ?,question_id = ? where id = ?'
            u = (answer['title'], answer['context'], answer['voters'], answer['user_id'],
                 answer['question_id'],answer['id'] )
            c.execute(sql, u)
        except Exception as e:
            print('更新失败，错误:' + e)
        finally:
            # conn.commit()
            DaoManager().conn_commit()
