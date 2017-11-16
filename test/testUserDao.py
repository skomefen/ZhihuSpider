from dao.UserDao import UserDao
from dao.ConnManager import ConnManager

u = UserDao()

user = {
    'id' : '12',
    'name' : 'xiaoming',
    'fans_num' : 1000,
    'url': 'aaa',

}

def test_save_user():
    u.save_user(user=user)

def test_find_user():
    print(u.find_user('12'))
    
def test_update_user():
    user['fans_num'] =555
    u.update_user(user)

test_save_user()
test_find_user()
test_update_user()
