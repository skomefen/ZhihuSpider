import os
from controller.TopicController import TopicController
from controller.QuestionController import QuestionController
from threading import Event
from concurrent.futures import ThreadPoolExecutor
import datetime
from dao.DaoManager import DaoManager

def main():

    start = datetime.datetime.now()
    print('开始时间：',start)

    base_url = 'https://www.zhihu.com/topic/20048470/top-answers'

    path_sep = os.path.sep
    topic_controller = TopicController(url=base_url)

    # 执行爬虫
    question_list = topic_controller.execute()

    num = question_list.__len__()
    index = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_list = []
        for question in question_list:
            question_controller = QuestionController(url=question['url'])
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

    end = datetime.datetime.now()
    print('结束时间：',end)
    print('共花费时间：',end-start)

if __name__ == '__main__':
    main()   