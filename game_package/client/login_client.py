#-*- coding:utf-8 -*-

"""
@time = 2019.11.4
@author = Jacob
@version = 1.0

form set of my fighting game

"""
#系统内置模块
import sys
import os

#第三方模块,如果是同模块，要从大到小排列
import pygame.locals

#自己的模块

from game_package.tool.game_sprites import *

#TODO 设置任务栏图标


class Login(object):
    '''
    游戏选择大区的界面和逻辑主体
    '''
    def __init__(self):
        '''
        frame_init()
        创建精灵——按钮精灵和背景精灵
        '''
        # self.frame_init()
        self.screen = GameTool.frame_init(self)
        # create sprite button
        self.__create_sprite_button()
        # create sprite background
        self.__create_sprite_background()
        #run
        self.__run()

    def __run(self):
        '''
        程序入口，不停的更新图片，以及判断事件
        '''

        # The variable can record the previous focus btn. Then update new btn before restore the previous btn
        self.prev_click_server = 0
        self.prev_click_area = 0

        # set show frame.  True = visible  False = not visible
        self.visible = True

        #Create fps object
        fpsClock = pygame.time.Clock()

        while self.visible == True:
            #set fps 30fps/s
            fpsClock.tick(30)
            #update all sprite
            self.__update_sprites()
            #handler all event
            self.__event_handler()

            #display screen
            pygame.display.update()

    def __create_sprite_button(self):
        '''
        创建按钮精灵
        '''

        self.area_sanyue = ButtonSprite(game_constant.BTN_SELECT_AREA_1,1)
        self.area_sanyue.rect.topleft = game_constant.BTN_SELECT_AREA_COORDINATE
        self.server_python = ButtonSprite( game_constant.BTN_SELECT_SERVER_1, 1 )
        self.server_python.rect.topleft = game_constant.BTN_SELECT_SERVER_COORDINATE
        self.server_jiandao = ButtonSprite( game_constant.BTN_SELECT_SERVER_1 )
        self.server_jiandao.rect.topleft = game_constant.BTN_SELECT_SERVER2_COORDINATE
        self.select_go = ButtonSprite(game_constant.BTN_AREA_GO_1)
        self.select_go.rect.topleft = game_constant.BTN_AREA_GO_COORDINATE

        self.text_area_sanyue = GameSprite( game_constant.TEXT_AREA_SANYUE )
        self.text_area_sanyue.rect.center = self.area_sanyue.rect.center
        self.text_server_python = GameSprite( game_constant.TEXT_SERVER_PYTHON )
        self.text_server_python.rect.center = self.server_python.rect.center
        self.text_server_jiandao = GameSprite( game_constant.TEXT_SERVER_JIANDAO )
        self.text_server_jiandao.rect.center = self.server_jiandao.rect.center

        self.fluency_fluent_python = GameSprite( game_constant.FLUENCY_FLUENT )
        self.fluency_fluent_python.rect.center = (self.server_python.rect.left + (self.text_server_python.rect.left - self.server_python.rect.left) // 2,self.server_python.rect.centery)
        self.fluency_fluent_jiandao = GameSprite( game_constant.FLUENCY_FLUENT )
        self.fluency_fluent_jiandao.rect.center = (self.server_jiandao.rect.left + (self.text_server_jiandao.rect.left - self.server_jiandao.rect.left) // 2,self.server_jiandao.rect.centery)

        #TODO 缺一个利剑区和强化班，家族，核心
        # 流畅度 TODO 根据热度自动切换 还做不到，需要到时候server服务器配合
        self.areas = pygame.sprite.Group( self.area_sanyue )
        self.servers = pygame.sprite.Group( self.server_python, self.server_jiandao )
        self.go = pygame.sprite.Group(self.select_go)
        self.texts = pygame.sprite.Group(self.text_area_sanyue,self.text_server_jiandao,self.text_server_python)
        self.fluents = pygame.sprite.Group(self.fluency_fluent_jiandao,self.fluency_fluent_python)

    def __create_sprite_background(self):
        '''
        创建背景精灵，那些背景中不动的，都放在这里面
        '''
        self.background = GameSprite( game_constant.LOGIN_BACKGROUND )
        self.background.rect.topleft = (0,0)
        self.background_role = GameSprite( game_constant.LOGIN_BACKGROUND_ROLE )
        self.background_role.rect.topleft = game_constant.LOGIN_BACKGROUND_ROLE_COORDINATE
        self.background_select_area = GameSprite( game_constant.LOGIN_SERVER_SELECT )
        self.background_select_area.rect.topleft = game_constant.LOGIN_SERVER_SELECT_COORDINATE

        self.background_list = pygame.sprite.Group(self.background,self.background_role,self.background_select_area)

    def __update_sprites(self):
        '''
        更新所有精灵
        '''
        self.background_list.update()
        self.background_list.draw( self.screen )

        self.areas.update()
        self.areas.draw( self.screen )

        self.servers.update()
        self.servers.draw( self.screen )

        self.go.update()
        self.go.draw( self.screen )

        self.texts.draw( self.screen )

        self.fluents.draw(self.screen)

    def  __event_handler(self):
        '''
        事件监听,如果事件之间用if来判断的话，会很灵敏
        '''

        # scan all event
        for event in pygame.event.get():
            # quit game while you click the cross
            if event.type == pygame.locals.QUIT:
                sys.exit()
            # if you press the mouse left key,will trigger this event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # event.button == 1 decision press left key
                if event.button == 1:
                    # get mouse position when press it
                    self.mouse_pos_down = pygame.mouse.get_pos()
            # if you lift the mouse left key,will trigger this event
            elif event.type == pygame.MOUSEBUTTONUP:
                # event.button == 1 decision lift left key
                if event.button == 1:
                    # get mouse position when decision it
                    self.mouse_pos_up = pygame.mouse.get_pos()
                    index = 0
                    #all server button event handler
                    for sprite in self.servers:
                        #if click it
                        if GameTool.check_click( self, self.mouse_pos_down, self.mouse_pos_up, sprite.rect ):
                            #update previous click button state 0. set current click button state 1
                            self.servers.sprites()[self.prev_click_server].state = 0
                            self.prev_click_server = index
                            sprite.state = 1

                        index += 1

                    index = 0
                    for sprite in self.areas:
                        if GameTool.check_click( self, self.mouse_pos_down, self.mouse_pos_up, sprite.rect ):
                            self.areas.sprites()[self.prev_click_area].state = 0
                            self.prev_click_area = index
                            sprite.state = 1

                        index += 1

                    for sprite in self.go:
                        if GameTool.check_click( self, self.mouse_pos_down, self.mouse_pos_up, sprite.rect ):
                            #if click the button,close the py.
                            self.visible = False


