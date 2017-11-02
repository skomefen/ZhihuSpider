from controller.QuestionController import QuestionController


def main():

    base_url = 'https://www.zhihu.com/question/34492640'

    spider_controller = QuestionController(url=base_url, dao=spider_dao, view=spider_view)

    # 执行爬虫
    spider_controller.execute()

if __name__ == '__main__':
    main()   