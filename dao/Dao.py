import json

class Dao:

    def __init__(self):
        return

    def save(self,content):
        '''
        :param content:要写入文件的内容
        '''
        with open("result.txt", 'a', encoding="utf-8") as f:
            f.write(json.dumps(content, ensure_ascii=False) + "\n")
