#-*- coding:utf-8 -*-
from turtledemo import clock

import pygame

from game_package.game.map import SelectMap

'''
登陆进来后的入口。
游戏内的事情，在这里写，地图也好，进入地下城也好，交流也好，在这里调用。
'''
class Game(object):

    def __init__(self):
        # self.screen = GameTool.frame_init()
        self.run()

    def run(self):
        # TODO Fight_map()是打开洛兰的地图，想办法封装一下，可以做到我在赛利亚房间，出去的时候，再调用这个地图，自动生成怪物。
        #TODO 如果进入到一个门里，进入到洛兰地图
        SelectMap()