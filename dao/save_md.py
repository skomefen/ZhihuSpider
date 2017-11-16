import json
import os

class Dao:

    def __init__(self):
        return

    def save(self,content,file_name = None):
        '''
        :param content:list 要写入文件的内容
        :param filename:
        '''
        if(file_name == None):
            file_name = 'result.md'

        dirname = os.path.dirname(file_name)
        if dirname.strip()!='':
            if(not os.path.exists(dirname)):
                os.makedirs(dirname)

        with open(file_name, 'a', encoding="utf-8") as f:
            f.write(json.dumps(content, ensure_ascii=False) + "\n")
