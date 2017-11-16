from dao.ConnManager import ConnManager


class AnswerDao:

    def __init__(self):
        conn = ConnManager().get_conn()
        # 表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK:
                sql = 'create table answer (id text primary key not null,title text not null,url text not null,context text, voters integer,user_id text,question_id text)'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            print('表已存在')
        finally:
            ConnManager().conn_commit()

    def save_answer(self, answer):
        try:
            self.find_answer(answer['id'])
            self.update_answer(answer)
        except:
            conn = ConnManager().get_conn()
            c = conn.cursor()
            try:
                sql = 'insert into answer (id, title, url,context,voters,user_id,question_id) values (?,?,?,?,?,?,?)'
                u = (answer['id'], answer['title'], answer['url'], answer['context'],answer['voters'], answer['user_id'], answer['question_id'])
                c.execute(sql, u)
            except Exception as e:
                print('保存失败，错误:' + e)
            finally:
                # conn.commit()
                ConnManager().conn_commit()

    def find_answer(self, id):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from answer where id = ?'
            c.execute(sql, (id,))
            for row in c:
                answer = row
        except Exception as e:
            print('查询失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
        return answer

    def update_answer(self, answer):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update answer set title = ?,url = ?,context = ?,voters = ?,user_id = ?,question_id = ? where id = ?'
            u = (answer['title'], answer['url'],  answer['context'],answer['voters'], answer['user_id'],
                 answer['question_id'],answer['id'] )
            c.execute(sql, u)
        except Exception as e:
            print('更新失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
