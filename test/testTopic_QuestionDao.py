from dao.Topic_QuestionDao import Topic_QuestionDao

dao = Topic_QuestionDao()
topic_question ={
    'topic_id':'aaa',
    'question_id':'bbbb'
}

def test_save_topic_question():
    
    dao.save_topic_question(topic_question)


test_save_topic_question()