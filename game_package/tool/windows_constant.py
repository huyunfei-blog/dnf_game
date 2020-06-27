#-*- coding:utf-8 -*-
import os

import win32api

'''
关于windows的一些工具和常量定义
'''

#SCREEN ORIGIN in window x = 400,y = 230
SCREEN_ORIGIN_COORDINATE = (400, 230)

#get Windows screen size
WINDOWS_SIZE = (win32api.GetSystemMetrics(0),win32api.GetSystemMetrics(1))

#给一个大图片的大小和坐标，给小图片的大小，返回小图片在大图片居中的x，y坐标
def center_coordinate(self, outside_coordinate,outside_size, inside_size):
    text_x = outside_coordinate[0] + (outside_size[0] - inside_size[0]) // 2
    text_y = outside_coordinate[1] + (outside_size[1] - inside_size[1]) // 2
    return (text_x, text_y)

