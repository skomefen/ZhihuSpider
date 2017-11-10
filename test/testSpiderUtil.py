from util import SpiderUtil

s = SpiderUtil
def test_romve_same_dict_with_list():
    list = [
        {'aaa':123,'bbb':234},
        {'aaa':11123,'bbb':454452},
        {'aaa': 123, 'bbb': 235225}
    ]
    print(s.romve_same_dict_with_list('aaa',list))

test_romve_same_dict_with_list()