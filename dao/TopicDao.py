from dao.ConnManager import ConnManager


class TopicDao:

    def __init__(self):
        conn = ConnManager().get_conn()
        # 表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK:
                sql = 'create table topic (id text primary key not null,title text not null,url text not null)'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            print('表已存在')
        finally:
            ConnManager().conn_commit()

    def save_topic(self, topic):
        try:
            result = self.find_topic(topic['id'])
            if result:
               self.update_topic(topic)
               return
            
            conn = ConnManager().get_conn()
            c = conn.cursor()
        
            sql = 'insert into topic (id, title,url) values (?,?,?)'
            u = (topic['id'], topic['title'],topic['url'])
            c.execute(sql, u)
        except Exception as e:
            print('保存失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()

    def find_topic(self, id):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from topic where id = ?'
            c.execute(sql, (id,))
            topic = None
            for row in c:
                topic = row
        except Exception as e:
            print('查询失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
        return topic

    def update_topic(self, topic):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update topic set title = ? ,url = ? where id = ?'
            u = (topic['title'],topic['url'], topic['id'])
            c.execute(sql, u)
        except Exception as e:
            print('更新失败，错误:' + e)
        finally:
            # conn.commit()
            ConnManager().conn_commit()
