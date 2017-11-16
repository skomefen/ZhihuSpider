from dao.ConnManager import ConnManager


class QuestionDao:

    def __init__(self):
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
            print('表已存在')
        finally:
            ConnManager().conn_commit()

    def save_question(self, question):
        try:
            self.find_question(question['id'])
            self.update_question(question)
        except:
            conn = ConnManager().get_conn()
            c = conn.cursor()
            try:
                sql = 'insert into question (id, title,url) values (?,?,?)'
                u = (question['id'], question['title'],question['url'])
                c.execute(sql, u)
            except Exception as e:
                print('保存失败，错误:' + e)
            finally:
                # conn.commit()
                ConnManager().conn_commit()

    def find_question(self, id):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from question where id = ?'
            c.execute(sql, (id,))
            for row in c:
                user = row
        except Exception as e:
            print('查询失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
        return user

    def update_question(self, question):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update question set title = ?,url = ? where id = ?'
            u = (question['title'],question['url'],question['id'])
            c.execute(sql, u)
        except Exception as e:
            print('更新失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
