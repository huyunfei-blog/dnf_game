#-*- coding:utf-8 -*-
import sys
import time

import pygame
from pygame.time import delay

from game_package.client.login_client import Login
from game_package.tool import game_constant, monster_constant, sword_man_constant, sword_constant
from game_package.tool.game_sprites import *

'''
幽暗密林图内的东西

sprite_map_cataclysm_granflores_mirkwood_tile.NPK
sprite_map_cataclysm_granflores_mirkwood_pathgate.NPK
sprite_map_cataclysm_granflores_mirkwood_object.NPK
sprite_map_cataclysm_granflores_mirkwood_background.NPK


洛兰地图选择
sprite_worldmap_act1.NPK

哥布林
sprite_monster_goblin.NPK

sprite_character_common_8thrare_effect.NPK          时装特效
sprite_character_common_aura.NPK                            时装光环

sprite_character_common_teleport_after.NPK                  传送后特效
sprite_character_common_teleport_before.NPK                 传送前特效
sprite_character_common_teleport_wait.NPK                   传送时特效
sprite_character_common_weaponavatar_1.NPK            名称装饰卡
sprite_character_common_weaponavatar_2.NPK            时装特效
sprite_character_common_weaponavatar_3.NPK                8bit特效
sprite_character_common_weaponavatar_pr13.NPK            某魔法特效
sprite_character_common_weaponavatar_rose13.NPK         某切野特效
sprite_character_common_weaponavatar_xmas13.NPK        某翻转特效
sprite_character_challenge2nd_                        决斗场光环

sprite_item_avatar_common.NPK                               通用时装图标
sprite_item_avatar_swordman.NPK                             鬼剑士时装图标

sprite_item_common.NPK                                      装备图标（地雷和落石机关）

sprite_character_common_footprint.NPK  穿着天空7时的移动效果
sprite.NPK                                                  登陆界面
sprite_character.NPK                                        默认角色头像和角色轮廓
sprite_character_common.NPK                                 通用技能图标

天11翅膀
sprite_character_common_chn_9thrare_effect
天9翅膀
sprite_creature_chn_p1event.NPK

装备修理
sprite_interface_chn_convenience.NPK                       修理按X提示

里面有一些等级数字可以利用
sprite_interface_common_digit.NPK                           地图推荐等级的数字
游戏的数字素材
sprite_interface_digit.NPK                                  一些数字
'''

'''
洛兰地图的绘制，不过目前，怪物的移动和绘制，以及人物的移动和绘制，和技能，都在这里面，还没有进行封装 
'''

class SelectMap(object):
    '''
    洛兰选择地图界面
    '''
    def __init__(self):
        #frame init
        self.screen = GameTool.frame_init(self)
        #create sprite
        self.__create_sprite()
        #让默认的鼠标不显示
        pygame.mouse.set_visible(False)
        #run
        self.__run()

    def __run(self):
        self.visible = True
        self.click_luolan = 0
        fpsClock = pygame.time.Clock()

        while self.visible:
            fpsClock.tick(30)

            self.__event_handler()
            self.__update_sprite()
            pygame.display.update()

        if self.visible == False:
            FightMap()

    def __create_sprite(self):
        '''
        创建精灵
        '''
        self.select_back_luolan = GameSpriteTransform(game_constant.MAP_SELECT_BACKGROUND_LUOLAN,(game_constant.SCREEN_SIZE))
        self.select_map_luolan = GameSpriteTransform( game_constant.MAP_SELECT_LUOLAN,game_constant.MAP_SELECT_LUOLAN_SIZE)
        self.select_map_luolan.rect.topleft = game_constant.MAP_SELECT_LUOLAN_COORDINATE
        self.luolan_difficulty = GameSpriteTransform(game_constant.MAP_SELECT_LUOLAN_DIFFICULTY,game_constant.MAP_SELECT_LUOLAN_DIFFICULTY_SIZE)
        self.luolan_difficulty.rect.topleft = game_constant.MAP_SELECT_LUOLAN_COORDINATE
        self.mouse_style = MouseSprite(game_constant.MOUSE_STYLE)

        self.background = pygame.sprite.Group(self.select_back_luolan)
        self.select_map = pygame.sprite.Group(self.select_map_luolan)
        self.luolan_map_difficulty = pygame.sprite.Group()
        self.mouse = pygame.sprite.Group(self.mouse_style)

    def __update_sprite(self):
        '''
        更新精灵组
        :return:
        '''
        self.background.draw(self.screen)
        self.select_map.draw(self.screen)
        self.luolan_map_difficulty.draw(self.screen)
        self.mouse.update()
        self.mouse.draw(self.screen)

    def __event_handler(self):
        '''
        事件监听，有一个点击事件的判断，当点击两次地图之后，关闭本页面，进入对应地图，因为还没有其它地图，所以直接进入了洛兰地图
        :return:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos_down = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pos_up = pygame.mouse.get_pos()
                for sprite in self.select_map:
                    if GameTool.check_click( self,self.mouse_pos_down, self.mouse_pos_up, sprite.rect):
                        self.luolan_map_difficulty.add(self.luolan_difficulty)
                        self.click_luolan += 1

                if self.click_luolan == 2:
                    self.visible = False

class FightMap(object):

    def __init__(self):
        '''
        洛兰地图选择后的跳转页面
        '''
        #让默认的鼠标不显示
        pygame.mouse.set_visible(False)
        self.screen = GameTool.frame_init(self)
        self.__create_sprite()
        self.__run()

    def __run(self):
        '''
            The father class of this class can use run method，overwrite this class run method
        :return:
        '''
        self.visible = True
        self.__variable_init()
        #设置重复事件定时器
        pygame.time.set_timer( ADD_SPRITE_EVENT, monster_constant.LUOLAN_MONSTER_UPDATE_TIMER )

        while self.visible:
            self.fpsClock.tick( game_constant.FPS )
            self.__event_handler()
            GameTool.collide_group_sword( self, self.sword, self.monster )
            self.__update_sprite()
            GameTool.monster_blood_trough( self, self.screen, self.monster, 10 )
            pygame.display.update()

    def __variable_init(self):
        '''
        All variable init in their
        :return:
        '''
        #fps
        self.fpsClock = pygame.time.Clock()
        #map boundary squre
        self.map_rect = pygame.Rect( *game_constant.LUOLAN_BOUNDARY_RECT )

    def __create_sprite(self):
        '''
        创建所有精灵，背景，英雄，怪物
        :return:
        '''
        self.map_back_luolan = GameSprite( game_constant.MAP_BACKGROUND_LUOLAN )
        self.sword_man = SwordMan( sword_man_constant.STAY_IMAGE, *sword_man_constant.SWORD_MAN_ATTRIBUTE)
        self.sword_man.rect.topleft = (189,224)

        self.gebulin1 = LuolanMonster( monster_constant.GEBULIN1_WALK_IMAGE, *monster_constant.GEBULIN1_ATTRIBUTE, self.sword_man )
        self.gebulin1.rect.topleft = monster_constant.MONSTER_SECOND_DOOR_COORDINATE

        self.sword_body = Sword(sword_constant.beamswd0300_STAY_IMAGE,*sword_constant.beamswd0300_ATTRIBUTE,self.sword_man,0)
        self.sword_decorate = Sword( sword_constant.beamswd0300_STAY_DECORATE_IMAGE, *sword_constant.beamswd0300_ATTRIBUTE,
                            self.sword_man, 1 )
        self.sword_handle = Sword( sword_constant.beamswd0300_STAY_HANDLE_IMAGE, *sword_constant.beamswd0300_ATTRIBUTE, self.sword_man ,2)
        self.mouse_style = MouseSprite(game_constant.MOUSE_STYLE)

        self.skill_Bar = GameSprite( "../image_package/frame/blood_trough/skillBar.png" )
        self.blood_trough = GameSprite( '../image_package/frame/blood_trough/hp100.png' )
        self.mp_trough = GameSprite( "../image_package/frame/blood_trough/mp.png" )
        self.Lv_trough = GameSprite( "../image_package/frame/blood_trough/Lv.png" )
        self.z1 = GameSprite( "../image_package/frame/blood_trough/z1.png" )
        self.z2 = GameSprite( "../image_package/frame/blood_trough/z2.png" )
        self.z3 = GameSprite( "../image_package/frame/blood_trough/z3.png" )
        self.blood_trough.rect.topleft = (63,558)
        self.skill_Bar.rect.topleft = (50,538)
        self.mp_trough.rect.topleft = (1030,558)
        self.Lv_trough.rect.topleft = (89,672)
        self.z1.rect.topleft = (198,630)
        self.z2.rect.topleft = (250,630)
        self.z3.rect.topleft = (305,630)

        self.background = pygame.sprite.Group( self.map_back_luolan,self.skill_Bar,self.blood_trough,self.mp_trough,self.Lv_trough,self.z1,self.z2,self.z3 )
        self.person = pygame.sprite.Group(self.sword_man)
        self.monster = pygame.sprite.Group(self.gebulin1)
        self.sword = pygame.sprite.Group(self.sword_body,self.sword_decorate,self.sword_handle)
        self.mouse = pygame.sprite.Group(self.mouse_style)

    def __update_sprite(self):

        self.background.update()
        self.background.draw(self.screen)
        self.monster.update()
        self.monster.draw(self.screen)
        #传update参数一个map_rect 也就是地图多大的地方可以让人去行走
        self.person.update(self.map_rect)
        self.person.draw(self.screen)
        self.sword.update()
        self.sword.draw(self.screen)
        self.mouse.update()
        self.mouse.draw(self.screen)

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == ADD_SPRITE_EVENT:
                #if monster sprites list __len__ <= 6, create a sprite in monster second door
                if(self.monster.sprites().__len__() <= 12):
                    #create a new object
                    self.gebulin1 = LuolanMonster( monster_constant.GEBULIN1_WALK_IMAGE,
                                                   *monster_constant.GEBULIN1_ATTRIBUTE, self.sword_man )
                    self.gebulin1.rect.topleft = monster_constant.MONSTER_SECOND_DOOR_COORDINATE
                    self.monster.add( self.gebulin1 )
                #create sprite in First door six sprite
                if (self.monster.sprites().__len__() <= 12):
                    # create a new sprite,set sprite topleft. insert the list
                    self.gebulin1 = LuolanMonster( monster_constant.GEBULIN1_WALK_IMAGE,
                                                   *monster_constant.GEBULIN1_ATTRIBUTE, self.sword_man )
                    self.gebulin1.rect.topleft = monster_constant.MONSTER_FIRST_DOOR_COORDINATE
                    self.monster.add( self.gebulin1 )

