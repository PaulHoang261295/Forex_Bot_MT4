def array(a):
    a_list = []
    for i in a:
        c = i*i
        a_list.append(c)
    return a_list


test= [1,4,5,-3]

b = array(test)
print(b,end='')
