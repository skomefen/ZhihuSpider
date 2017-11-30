from dao.TopicDao import TopicDao
from dao.ConnManager import ConnManager

t = TopicDao()

topic = {
    'id': '123',
    'title': 'aaaa',
    'url': 'aaa'
}


def test_save_topic():
    t.save_topic(topic=topic)


def test_find_topic():
    print(t.find_topic('12322'))


def test_update_topic():
    topic['title'] = '12322'
    t.update_topic(topic)


#test_save_topic()
test_find_topic()
#test_update_topic()
