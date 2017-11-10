
def ip_proxy():
    
    return ''

def romve_same_dict_with_list(key,list):

    new_list = []
    new_list.append(list[0])
    for dict in list:
        index = 0
        len_num = len(new_list)
        for item in new_list:
            if dict[key] != item[key]:
                index +=1
            else:
                break
            if index == len_num:
                new_list.append(dict)

    return  new_list