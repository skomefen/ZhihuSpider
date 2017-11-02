import json

class Dao:

    def __init__(self):
        return

    def save(self,content,file_name = None):
        '''
        :param content:list 要写入文件的内容
        '''
        content_with_str = str(content)
        if(file_name == None):
            file_name = 'result.txt'

        with open(file_name, 'a', encoding="utf-8") as f:
            f.write(json.dumps(content_with_str, ensure_ascii=False) + "\n")
