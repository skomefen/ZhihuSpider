from dao.save_md import save_md

dao = save_md()

def test_save():
    dao.save('aaaaaaaaa')

test_save()