from dao.ConnManager import ConnManager

class UserDao:
    
    def __init__(self):
        conn = ConnManager().get_conn()
        #表不存在就创建表
        tableIsOK = False
        try:
            if not tableIsOK :
                sql = 'create table user (id text primary key not null,name text not null,url text not null, fans_num integer)'
                c = conn.cursor()
                c.execute(sql)
                tableIsOK = True
        except Exception as e:
            print('表已存在')
        finally:
            ConnManager().conn_commit()

    def save_user(self,user):
        try:
            result = self.find_user(user['id'])
            if result:
                self.update_user(user)
                return 
            conn = ConnManager().get_conn()
            c = conn.cursor()
            
            sql = 'insert into user (id, name,url,fans_num) values (?,?,?,?)'
            u = (user['id'],user['name'],user['url'],user['fans_num'])
            c.execute(sql,u)
        except Exception as e:
            print('保存失败，错误:'+e)
        finally:
            #conn.commit()
            ConnManager().conn_commit()

    def find_user(self,id):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'select * from user where id = ?'
            c.execute(sql,(id,))
            user = None
            for row in c:
                user = row
        except Exception as e:
            print('查询失败，错误:'+e)
        finally:
            #conn.commit()
            ConnManager().conn_commit()
        return user

    def update_user(self,user):
        conn = ConnManager().get_conn()
        c = conn.cursor()
        try:
            sql = 'update user set name = ?,url = ?,fans_num = ? where id = ?'
            u = (user['name'],user['url'],user['fans_num'],user['id'])
            c.execute(sql,u)
        except Exception as e:
            print('更新失败，错误:' + e)
        finally:
            #conn.commit()
            ConnManager().conn_commit()
