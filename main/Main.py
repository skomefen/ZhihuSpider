import os
from controller.TopicController import TopicController
from controller.QuestionController import QuestionController
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

def main():

    base_url = 'https://www.zhihu.com/topic/20018196/top-answers'

    path_sep = os.path.sep
    topic_controller = TopicController(url=base_url,save_folder='..'+path_sep+'result_file')

    topic_name = topic_controller.get_Topic_name()
    # 执行爬虫
    question_list = topic_controller.execute()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for question in question_list:
            save_file_name = '..'+path_sep+'result_file'+path_sep+topic_name+path_sep+str(question.get('info'))+'_'+question.get('question_name')+'.md'
            question_controller = QuestionController(url=question['url'],save_file_name=save_file_name)
            executor.submit(question_controller.execute)



if __name__ == '__main__':
    main()   