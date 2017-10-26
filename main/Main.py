from controller.Controller import Controller
from view.View import View
from dao.Dao import Dao

def main():

    base_url = 'https://www.zhihu.com/question/20363696'

    spider_dao = Dao()

    spider_view = View()

    spider_controller = Controller(url=base_url, dao=spider_dao, view=spider_view)

    # 执行爬虫
    spider_controller.execute()

if __name__ == '__main__':
    main()