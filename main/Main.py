from controller.TopicController import TopicController
from controller.QuestionController import QuestionController
from concurrent.futures import ThreadPoolExecutor
import datetime
from dao.DaoManager import DaoManager
from log import LogCenter
import logging
import os

def main():

    seq = os.path.sep
    path = ".."+seq+"log"+seq+"logging.json."
    LogCenter.setup_logging(default_path=path)
    start = datetime.datetime.now()
    
    logger = logging.getLogger(__name__)
    logger.info('开始爬虫')
    #print('开始时间：',start)

    base_url = 'https://www.zhihu.com/topic/20044913/top-answers'
    topic_controller = TopicController(url=base_url)

    # 执行爬虫
    question_list = topic_controller.execute()

    num = question_list.__len__()
    index = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        for question in question_list:
            question_controller = QuestionController(url=question['url'],name=question['title'])
            future = executor.submit(question_controller.execute)
            future_list.append(future)

        for future in future_list:
            while True:
                if future.done():
                    index += 1
                    break

    while True:
        if index == num:
            DaoManager().quit_run()
            break

    logger.info('结束爬虫')
    end = datetime.datetime.now()
    #print('结束时间：',end)
    #print('共花费时间：',end-start)
    logger.info('爬虫共花费时间：%s',end-start)

if __name__ == '__main__':
    main()   