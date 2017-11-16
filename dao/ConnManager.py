import sqlite3
from conf import dao_config
import os

class DaoManager:
    
    #单例设计
    __instance = None
    _conn = None
    def __init__(self):
        if DaoManager._conn == None:
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
                DaoManager._conn = sqlite3.connect(save_path+sep+database_name)
            except:
                print('连接数据库失败,检查dao_config配置文件')

    def __new__(cls, *args, **kwd):
        if DaoManager.__instance is None:
            DaoManager.__instance = object.__new__(cls, *args, **kwd)
        return DaoManager.__instance

    def get_conn(self):
        """
        :return: 数据库连接
        """
        return DaoManager._conn

    def conn_commit(self):
        DaoManager._conn.commit()

    def conn_close(self):

        if DaoManager._conn.in_transaction:
            DaoManager._conn.commit()

        DaoManager._conn.close()