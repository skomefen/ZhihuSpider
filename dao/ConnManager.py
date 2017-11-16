import sqlite3
from conf import dao_config
import os

class ConnManager:
    
    #单例设计
    __instance = None
    _conn = None
    def __init__(self):
        if ConnManager._conn == None:
            try:
                if dao_config.DATABASE_SAVE_PATH == None:
                    save_path = ''
                else:
                    save_path = dao_config.DATABASE_SAVE_PATH

                if dao_config.DATABASE_NAME == None:
                    database_name = 'ZhihuSpider.db'
                else:
                    database_name = dao_config.DATABASE_NAME
                sep = os.path.sep
                #_conn等于None的时候重新获取
                ConnManager._conn = sqlite3.connect(save_path + sep + database_name)
            except:
                print('连接数据库失败,检查dao_config配置文件')

    def __new__(cls, *args, **kwd):
        if ConnManager.__instance is None:
            ConnManager.__instance = object.__new__(cls, *args, **kwd)
        return ConnManager.__instance

    def get_conn(self):
        """
        :return: 数据库连接
        """
        return ConnManager._conn

    def conn_commit(self):
        ConnManager._conn.commit()

    def conn_close(self):

        try:
            if ConnManager._conn.in_transaction:
                ConnManager._conn.commit()
        finally:
            ConnManager._conn.close()
            ConnManager._conn = None
        