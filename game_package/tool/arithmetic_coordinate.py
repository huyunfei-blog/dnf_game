#-*- coding:utf-8 -*-

if __name__ == '__main__':
    first_coordinate = (195,237)
    list = (195,237,177,237,186,241,200,244,198,245,206,246,223,246,224,246,224,246,224,246)
    list2 = []

    for i in range(0,list.__len__()):
        if i % 2 == 0:
            list2.append(list[i] - first_coordinate[0])
        else:
            list2.append(list[i] - first_coordinate[1])

    print(list2)