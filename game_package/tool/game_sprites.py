#-*- coding:utf-8 -*-

'''
管理游戏的所有精灵，以及关于游戏的工具
'''

import os

import pygame

from game_package.tool import windows_constant, game_constant, sword_man_constant, monster_constant, \
    sword_constant

ADD_SPRITE_EVENT = pygame.USEREVENT + 1

class GameTool(object):
    '''
    游戏用到的各种工具封装
    '''
    def frame_init(self):
        '''
        对界面框架的初始化，窗口大小，窗口初始位置，图标，标题
        '''
        pygame.init()
        #set screen default position
        game_x = (windows_constant.WINDOWS_SIZE[0] - game_constant.SCREEN_SIZE[0]) // 2
        game_y = (windows_constant.WINDOWS_SIZE[1] - game_constant.SCREEN_SIZE[1]) // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (game_x, game_y)
        # set game_window
        screen = pygame.display.set_mode( (game_constant.SCREEN_SIZE), 0, 32 )
        # set game_caption
        pygame.display.set_caption( game_constant.WINDOW_TITLE )
        # set game_icon
        icon = pygame.image.load( game_constant.GAME_ICON )
        pygame.display.set_icon( icon )

        return screen

    def check_pos(self, rect):
        '''
        检测当前鼠标是否在rect区域内。 传入矩形参数
        '''
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #get rect topleft x and y, and get rect bottomright x and y
        sprite_topleftx, sprite_toplefty = rect.topleft
        sprite_bottomrightx, sprite_bottomrighty = rect.bottomright
        #if mouse_x and mouse_y in rect,return True,else return False.
        if mouse_x >= sprite_topleftx and mouse_x <= sprite_bottomrightx and \
                mouse_y >= sprite_toplefty and mouse_y <= sprite_bottomrighty:
            return True

        else:
            return False

    def check_click(self, mouse_down, mouse_up, rect):
        '''
        鼠标点击在区域内,传入鼠标按下和抬起的坐标，判断是否在rect内
        '''
        mouse_down_x, mouse_down_y = mouse_down
        mouse_up_x, mouse_up_y = mouse_up

        sprite_topleftx, sprite_toplefty = rect.topleft
        sprite_bottomrightx, sprite_bottomrighty = rect.bottomright

        if mouse_down_x >= sprite_topleftx and mouse_down_x <= sprite_bottomrightx and \
                mouse_down_y >= sprite_toplefty and mouse_down_y <= sprite_bottomrighty and \
                mouse_up_x >= sprite_topleftx and mouse_up_x <= sprite_bottomrightx and \
                mouse_up_y >= sprite_toplefty and mouse_up_y <= sprite_bottomrighty:

            return True

        else:
            return False

    def check_map_boundary(self,map_rect,person_rect):
        '''
        地图边界检测，传入矩形边界参数，传入需要做界限的精灵
        '''

        #四位分别代表上下左右，为1代表碰到界限，为0代表没有碰到
        self.boundary = [0,0,0,0]

        #上边界  当人物的y坐标小于矩形的y坐标再减人物的高度和人物高度除以2
        if person_rect.y <= map_rect.y - person_rect.h + person_rect.h // 2:
            self.boundary[0] = 1

        # 下边界 窗体长度
        if person_rect.y >= map_rect.h - person_rect.h:
            self.boundary[1] = 1

        #左边界
        if person_rect.x <= map_rect.x :
            self.boundary[2] = 1

        #右边界  1900 + 1200(窗体长度) = 3100
        if person_rect.x >= map_rect.w - person_rect.w:
            self.boundary[3] = 1

        return self.boundary

    def cartoon_image(self,image_path,index,num):
        '''
        传出一个图片的地址，传入一个index，传入一个num
        :param image_path:图片地址
        :param index:下标
        :param num:取余的数
        :return:返回这个image
        '''
        image = pygame.image.load( (image_path
                                         [
                                         0:image_path.__len__() - 5] + "%s.png") % (
                                                index % num) )
        return image

    def cartoon_flip_image(self,image_path,index,num):
        '''
        传出一个图片的地址，传入一个index，传入一个num，返回这个图片的水平翻转
        :param image_path:图片地址
        :param index:下标
        :param num:取余的数
        :return:返回这个image
        '''
        image = pygame.image.load( (image_path
                                    [
                                    0:image_path.__len__() - 5] + "%s.png") % (
                                           index % num) )

        return pygame.transform.flip(image,True,False)

    def remove_sprite(self,sprite_group):
        '''
        传入一个精灵组，检测这个精灵组的里精灵的can_remove属性，如果为True，删除这个精灵。
        :param sprite_group:
        :return:
        '''
        if(sprite_group.sprites().__len__() != 0):
            for i in range(0,sprite_group.sprites().__len__()):
                if sprite_group.sprites()[i].can_remove == True:
                    sprite_group.remove(sprite_group.sprites()[i])

    def collide_group_sword(self, main_group, from_group):
        '''
        传入一个主精灵组，传入一个副精灵组，一个主精灵组可以和副精灵组中的多个精灵碰撞。
        :param main_group:
        :param from_group:
        :return:如果主精灵组的人物碰到人副精灵组中的人物，还进行了攻击，就让对应的精灵hp减少
        '''
        #碰撞检测字典列表。
        collide_dict = pygame.sprite.groupcollide(main_group , from_group, False,False )
        #一个英雄对多个精灵  对应 一个key对应多个value
        for i in range(0,collide_dict.__len__()):
            #key存的是对象，所以可以直接用，而values列表存的是字符串，但是通过key来获取的value就是对象
            #   dict.values()   # 返回可迭代的视图对象，而不是列表
            #   dict.keys()  返回的是列表
            collide_key = ((list(collide_dict.keys()))[i])
            collide_value = collide_dict[collide_key]

            for j in range(0,collide_value.__len__()):
                #因为一个key可以有多个value，即一个人物可能会和很多怪物碰到一起
                #人打怪物，如果怪物的hp不到0血之下，减血，如果到了0血之下，把精灵的is_die设置为True。
                if collide_key.person.is_attack == True :
                    if collide_key.person.is_do_attack == False :
                        #攻击 = 人物的攻击减去怪物的防御力
                        ad = collide_key.person.ad - collide_value[j].dp
                        if ad > 0:
                            collide_value[j].hp -= ad
                        if collide_value[j].hp < 0:
                            #播放倒地动画
                            collide_value[j].is_die = True
                        else:
                            collide_value[j].is_be_attack = True
                # #如果怪物打人，会设置怪物正在打为True，当轮播到第四张图片的时候，is_do_attack才为False，就会生效
                if collide_value[j].is_attack == True:
                    if collide_value[j].is_do_attack == False:
                        ad = collide_value[j].ad - collide_key.person.dp
                        if ad > 0 :
                            collide_key.person.hp -= ad

    def monster_blood_trough(self, screen, sprite_group, sprite_hp):
        '''
        因为怪物在打的时候，坐标会变，所以在怪物打的时候，获取到怪物的第一张图的坐标和大小，后面挥刀等不再改变坐标。
        :param screen:血条画的图像
        :param sprite_group:精灵组
        :param sprite_hp:精灵的hp上限
        :return:void
        '''
        self.blood_trough_coordinate = (0,0)
        for sprite in sprite_group:
            # 画这个精灵的血条，在sprite的头顶  并根据sprite的hp大小画不同的血条
            hp = sprite.hp / sprite_hp

            if sprite.attack_index > 0 :
                if sprite.is_face_left:
                        self.blood_trough_coordinate = sprite.first_coordinate[0] - sprite.first_size[0],\
                                              sprite.first_coordinate[1]
                else:
                        self.blood_trough_coordinate = sprite.first_coordinate[0], \
                                              sprite.first_coordinate[1]
                pygame.draw.rect( screen, (0, 0, 0), (*self.blood_trough_coordinate, 40, 8) )
                if sprite.hp > 0:
                    pygame.draw.rect( screen, (245, 0, 0), (*self.blood_trough_coordinate, 40 * hp, 8) )
            else:
                pygame.draw.rect( screen, (0, 0, 0), (sprite.rect.x + 5, sprite.rect.y, 40, 8) )
                if sprite.hp > 0:
                    pygame.draw.rect( screen, (245, 0, 0), (sprite.rect.x + 5, sprite.rect.y , 40 * hp, 8) )

    def arithmetic_deviation(self,first_coordinate,curren_list):
        '''
        :return:返回list中的数相对于first_coordinate的偏移量存在list2中。
        '''

        deviation_list = []

        for i in range( 0, curren_list.__len__() ):
            if i % 2 == 0:
                deviation_list.append( curren_list[i] - first_coordinate[0] )
            else:
                deviation_list.append( curren_list[i] - first_coordinate[1] )

        return list(deviation_list)

class GameSprite( pygame.sprite.Sprite ):
    '''
    游戏精灵类，基础精灵类，
    '''
    def __init__(self,image_path):
        super().__init__()
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()

class GameSpriteTransform( GameSprite ):
    '''
    游戏精灵类的transform，可以缩大缩小版本
    '''
    def __init__(self,image_path,size):
        super().__init__(image_path)
        self.image = pygame.transform.smoothscale(self.image,size)
        self.rect = self.image.get_rect()

class MouseSprite(GameSprite):
    '''
    鼠标精灵，悬浮两秒会自动消失
    '''
    def __init__(self,image_path):
        super().__init__(image_path)
        #鼠标是否显示
        self.visible = True
        #循环，用来判断当前是单次，还是双次
        self.index = 0
        #用来计数
        self.count = 0
        #记录以前的鼠标位置
        self.previous_pos = (0,0)
        #记录现在的鼠标位置
        self.current_pos = (0,0)

    def update(self):
        #检查鼠标是否该显示
        self.check_mouse()
        #如果显示，让图片换一下，坐标等于现在鼠标的坐标，否则，把图片换成空图片
        if self.visible:
            self.image = pygame.image.load(game_constant.MOUSE_STYLE)
            self.rect.topleft = pygame.mouse.get_pos()
        else:
            self.image = pygame.image.load(game_constant.MOUSE_STYLE_EMPTY)

        self.index += 1

    def check_mouse(self):
        #如果第一次，获取当前鼠标位置，第二次再获取当前的位置，这样就有了现在和上一次的鼠标位置
        if self.index % 2 == 0:
            self.previous_pos = pygame.mouse.get_pos()
        else:
            self.current_pos = pygame.mouse.get_pos()
        #如果现在的鼠标位置和上一次的鼠标位置相同，而且鼠标是显示的，就让count加1，如果一直位置相同，让count加到帧率*2，也就是
        #2秒的时候，让鼠标不显示，count = 0，如果动了，就让鼠标显示为True。
        if self.previous_pos[0] == self.current_pos[0] and self.previous_pos[1] == self.current_pos[1] :
            if self.visible:
                self.count += 1

            if self.count == game_constant.FPS * 2:
                self.visible = False
                self.count = 0
        else:
            self.visible = True

class ButtonSprite( GameSprite ):
    '''
    按钮精灵，具有状态属性。  当图片的状态为0时，如果把鼠标划上去，可以变成_2状态。当图片的状态为1时，如果
    把鼠标点击这个图片，会把图片切换为_3状态
    '''
    def __init__(self,image_path,state = 0):
        super().__init__(image_path)
        self.state = state

    def update(self):
        if self.state == 1:
            self.image_path = self.image_path[0:self.image_path.__len__() - 5] + "3.png"
            self.image = pygame.image.load( self.image_path )
            self.image = pygame.transform.smoothscale( self.image, self.rect.size )
        elif self.state == 0:
            if GameTool.check_pos( self, self.rect ):
                self.image_path = self.image_path[0:self.image_path.__len__() - 5] + "2.png"
                self.image = pygame.image.load( self.image_path )
                self.image = pygame.transform.smoothscale( self.image, self.rect.size )
            else:
                self.image_path = self.image_path[0:self.image_path.__len__() - 5] + "1.png"
                self.image = pygame.image.load( self.image_path )

#TODO 现在的人物行走不流畅，还是帧率和图片刷新的问题。 让帧率高一点，行走的速度小一点，让图片的轮播降低
#TODO 可以通过一种简单的方式实现上面的效果，即改变图片的后缀名，比如说两张图片之间隔50个图片，就让第一张图片为50.png，第二张图片为100.png
#TODO 然后让index % 100 的时候轮播即可。  也可以再加一个delay_index 只有这个index % 一个数 == 0 的时候，才能播放下一张图片
class Person(GameSprite):
    '''
    人物基本类 lv 等级  hp 血量  mp 魔法值  ad攻击力 dp防御力
    '''
    def __init__(self,image_path,lv,hp,mp,ad,dp):
        super().__init__(image_path)
        self.lv = lv
        self.hp = hp
        self.mp = mp
        self.ad = ad
        self.dp = dp
        self.variable_init()

    def variable_init(self):
        #走路图片的index
        self.walk_index = 0
        #死亡图片的index
        self.die_index = 0
        #攻击图片的index
        self.attack_index = 0
        #不动的图片的index
        self.stay_index = 0
        #被打图片轮播
        self.be_attack_index = 0
        #前突图片轮播
        self.protrusion_index = 0

        #游戏计时器
        self.timer = 0
        #按右键的时间
        self.current_right_time = 0
        self.previous_right_time = 0
        # 按左键的时间
        self.current_left_time = 0
        self.previous_left_time = 0

        self.first_coordinate = []
        self.first_size = ()

        #面向左边右边的状态
        self.is_face_left = True
        #是攻击的状态
        self.is_attack = False
        #是正在攻击
        self.is_do_attack = False
        #是死亡
        self.is_die = False
        #是正在死亡（图片播放）
        self.is_do_die = False
        #be attack 是被打
        self.is_be_attack = False
        #是跑的
        self.is_run = False
        #是否是第一次按右键或左键
        self.is_first_down_right = False
        self.is_first_down_left = False
        #前突动作
        self.is_protrusion = False


        #ex中body81100这个皮肤的三段攻击，第一张图片的坐标是189,224。  然后就可以通过一个函数来计算这个相对坐标，这样即使换皮肤了，只需要把
        #对应的初始坐标换一下即可
        self.body81100_attack = (189,224)
        self.body81100_run = (162,223)
        self.body81100_protrusion = (195,237)

    def coordinate_deviation(self, index, first_coordinate, num_list_right, is_face_left, right_image, is_person):
        '''
        第一个参数是图片的轮播index，第二个参数是第一张图片的coordinate，获取到这个坐标才能把后面的图片定位。
        第三个参数是后面的图片相对于第一张图片的坐标列表，右边图片。 左边图片的只需要把加上偶数下标减去偶数下标
        第四个参数是判断左边还是右边，第五个参数是获取向右的图片地址
        用这个函数的前提是已经有first_coordinate了，first_coordinate由人物获得，其它依附人物的可以直接用这个函数获取位置
        但人物不行
        如果是人物的话，num_list_right的第一个参数设置为0，因为其它图片都是它的基础上计算的，只需要让它加0，就回到了原点
        :param index:图片轮播的下标
        :param first_coordinate:给一个变量存第一个图片的坐标
        :param num_list_right:给一个图片偏移的列表
        :param is_face_left:判断当前人物的面向
        :param right_image:面向右边的图片
        :param is_person:是否是人物
        :return:
        '''
        #因为一个图片右两个坐标，那么num_list_right.__len__() // 2 就是用户传进来的图片数。
        image_count = num_list_right.__len__() // 2
        #这个是存当前图片坐标的下标，当index为0的时候，当前x_index的坐标就是0，当index为1的时候，当前x_index的坐标就是2。
        x_index = index % image_count * 2
        #如果是面向右边的
        if not is_face_left:
            #播放图片
            self.image = GameTool.cartoon_image( self, right_image, index, image_count )
            #获取图片大小
            self.rect.size = self.image.get_rect().size
            #如果是一组图第一次轮播的话
            if index % image_count == 0:
                #如果是人物，在第一次的时候需要存一下first_coordinate。  因为人物的坐标都是根据第一张图片来变化的，而
                #不是人物，比如剑，配饰，这些依附人物的产物，都是根据人物的变化而变化，所以不需要存取
                if is_person:
                    if index != 0:
                        self.rect.topleft = (
                            first_coordinate[0] + num_list_right[0], first_coordinate[1] + num_list_right[1])
                    else:
                        self.first_size = self.rect.size
                        self.first_coordinate = [*self.rect.topleft]
                else:
                    self.rect.topleft = (
                        first_coordinate[0] + num_list_right[0], first_coordinate[1] + num_list_right[1])
            else:
                #如果不是第一张，那么就正常进行，第一张的话，设置第一张为list的0号和1号下标的坐标，第二张设置第二张为list的2号和3号下标的坐标。
                self.rect.topleft = (first_coordinate[0] + num_list_right[x_index],first_coordinate[1] + num_list_right[x_index+1])
        #否则就是面向左边，和上面相同，只是把topleft换成topright，把坐标相加变成相减
        else:
            self.image = GameTool.cartoon_flip_image( self, right_image, index, image_count )
            self.rect.size = self.image.get_rect().size
            if index % image_count == 0:
                if is_person:
                    if index != 0:
                        self.rect.topright = (
                            first_coordinate[0] - num_list_right[0], first_coordinate[1] + num_list_right[1])
                    else:
                        self.first_size = self.rect.size
                        self.first_coordinate = [*self.rect.topright]
                else:
                    self.rect.topright = (
                        first_coordinate[0] - num_list_right[0], first_coordinate[1] + num_list_right[1])
            else:
                self.rect.topright = (first_coordinate[0] - num_list_right[x_index],first_coordinate[1] + num_list_right[x_index+1])

        image_count = num_list_right.__len__() // 2
        x_index = index % image_count * 2
        if not is_face_left:
            self.image = GameTool.cartoon_image( self, right_image, index, image_count )
            self.rect.size = self.image.get_rect().size
            if index % image_count == 0:
                if is_person:
                    if index != 0:
                        self.rect.topleft = (
                            first_coordinate[0] + num_list_right[0], first_coordinate[1] + num_list_right[1])
                    else:
                        self.first_coordinate = [*self.rect.topleft]
                else:
                    self.rect.topleft = (
                        first_coordinate[0] + num_list_right[0], first_coordinate[1] + num_list_right[1])
            else:
                self.rect.topleft = (first_coordinate[0] + num_list_right[x_index],first_coordinate[1] + num_list_right[x_index+1])

        else:
            self.image = GameTool.cartoon_flip_image( self, right_image, index, image_count )
            self.rect.size = self.image.get_rect().size
            if index % image_count == 0:
                if is_person:
                    if index != 0:
                        self.rect.topright = (
                            first_coordinate[0] - num_list_right[0], first_coordinate[1] + num_list_right[1])
                    else:
                        self.first_size = self.rect.size
                        self.first_coordinate = [*self.rect.topright]
                else:
                    self.rect.topright = (
                        first_coordinate[0] - num_list_right[0], first_coordinate[1] + num_list_right[1])
            else:
                self.rect.topright = (first_coordinate[0] - num_list_right[x_index],first_coordinate[1] + num_list_right[x_index+1])

#TODO 人物击打怪物后，怪物有僵直和停顿图片，还没做
#FIXME：当人物和怪物接触，人物离开怪物的时候，怪物坐标会出现瞬移，不知道为什么
#TODO 现在人物穿的是时装，时装是一体的。
class LuolanMonster(Person):
    '''
    洛兰的怪物属性
    可以根据传进来的精灵，实现对其坐标的追踪
    '''
    def __init__(self,image_path,lv,hp,mp,ap,dp,person):
        super().__init__(image_path,lv,hp,mp,ap,dp)
        self.person = person
        self.speed = 3

    def update(self):
        '''
        怪物的主逻辑
        :return:
        '''
        # 如果死亡了，运行死亡函数
        if self.is_die:
            self.do_die()
        else:
            # 如果被打了，就播放被打动画
            if self.is_be_attack:
                self.image = GameTool.cartoon_flip_image( self, monster_constant.GEBULIN1_FALL_DOWN_IMAGE, self.be_attack_index,
                                                          1 )
                self.be_attack_index += 1
                # 1/4秒之后，恢复状态（僵直）
                if self.be_attack_index >= game_constant.FPS // 4:
                    self.is_be_attack = False
            else:
                # 如果不是在攻击的状态，就去找人
                if not self.is_attack:
                    self.find()
                # 如果到了攻击范围，把时攻击设置为True，和正在攻击设置为True，进入攻击函数
                if self.rect.bottomleft[0] < self.person.rect.bottomright[0] + 3 and self.rect.bottomright[0] > \
                        self.person.rect.bottomleft[
                            0] - 3 and self.rect.bottom <= self.person.rect.bottom and self.rect.bottom >= self.person.rect.bottom - self.person.rect.h // 4 or self.is_attack:
                    self.is_attack = True
                    self.is_do_attack = True
                    self.attack()
                # 如果是面向左边的，就播放左边走的动画，否则播放右边走的动画，这个timer的判断是用来控制图片轮播的速度
                elif self.is_face_left:
                    self.image = GameTool.cartoon_flip_image( self, monster_constant.GEBULIN1_WALK_IMAGE, self.walk_index, 4 )
                    self.walk_index += 1
                    self.attack_index = 0
                elif not self.is_face_left:
                    self.image = GameTool.cartoon_image( self, monster_constant.GEBULIN1_WALK_IMAGE, self.walk_index, 4 )
                    self.walk_index += 1
                    self.attack_index = 0
            #TODO 怪物的走路姿势很别扭。

            # else:
            #     num_list_right = (3,0,3,2,0,-1)  #3,0,3,2,0,-1
            #     right_image = monster_constant.GEBULIN1_WALK_IMAGE
            #     self.coordinate_deviation( self.walk_index, self.first_coordinate, num_list_right, self.is_face_left,
            #                                right_image, True )
            #
            #     self.walk_index += 1
            #     self.attack_index = 0

    def attack(self):
        '''
        怪物的攻击逻辑
        :return:
        '''
        #把怪物的攻击方法封装出来，然后定时使用这个方法。。
        #update会去找英雄，然后每隔一秒发起一个事件，获取一个事件，
        num_list_right = (0, -2, -2, -1, -17, -35, -9, 2, 0, 2)
        right_image = monster_constant.GEBULIN1_HIT_IMAGE
        self.coordinate_deviation(self.attack_index,self.first_coordinate,num_list_right,self.is_face_left,right_image,True)

        #attack over  如果打完了把do attack 设置为false
        if self.attack_index % 5 == 4:
            self.is_do_attack = False
        # 如果 == 0 就把is_attack = False
        if self.attack_index % 5 == 0:
            self.is_attack = False
        else:
            self.is_attack = True

        self.attack_index += 1

        self.walk_index = 0

    def do_die(self):
        '''
        怪物死亡的时候的逻辑，换图和换状态
        :return:
        '''
        #TODO 复用self.cartoon.deviation()
        if self.is_do_die == False:
            # 如果怪物没有播放死亡图片，就播放死亡图片
            if not self.is_face_left:
                self.image = GameTool.cartoon_image( self, monster_constant.GEBULIN1_FALL_DOWN_IMAGE,
                                                     self.die_index, 5 )
            else:
                self.image = GameTool.cartoon_flip_image( self, monster_constant.GEBULIN1_FALL_DOWN_IMAGE,
                                                     self.die_index, 5 )
            self.rect.size = self.image.get_rect().size
        # 当死亡图片为4的时候，说明图片播放完了，怪物也就真死了
        if self.die_index == 4:
            self.is_do_die = True

        self.die_index += 1

        # 3s后后删除精灵
        if (self.die_index == game_constant.FPS * 3):
            self.kill()

    def find(self):
        '''
        怪物自己找人
        :return:
        '''
        # 自动追踪
        if self.rect.bottomright[0] <= self.person.rect.bottomleft[0] - 3:
            # if self.first_coordinate.__len__() != 0:
            #     self.first_coordinate[0] += self.speed
            self.rect.x += self.speed
            self.is_face_left = False

        elif self.rect.bottomleft[0] >= self.person.rect.bottomright[0] + 3:
            # if self.first_coordinate.__len__() != 0:
            #     self.first_coordinate[0] -= self.speed
            self.rect.x -= self.speed
            self.is_face_left = True

        if self.rect.bottom < self.person.rect.bottom - self.person.rect.h // 4:
            # if self.first_coordinate.__len__() != 0:
            #     self.first_coordinate[1] += self.speed
            self.rect.y += self.speed
        elif self.rect.bottom > self.person.rect.bottom:
            # if self.first_coordinate.__len__() != 0:
            #     self.first_coordinate[1] -= self.speed
            self.rect.y -= self.speed

class SwordMan(Person):
    '''
    鬼剑士的初始化类，有一个方向属性，第一位为1代表是不动的，为0代表是动的。
    第二位为1代表往上走，第三位为1代表往下走，第四位为1代表往左走，第五位为1代表往右走
    '''
    def __init__(self,image_path,lv,hp,mp,ap,dp,xp,sword_code = "beamswd0300",direction = [1,0,0,0,0 ]):
        super().__init__(image_path,lv,hp,mp,ap,dp)
        # 0 : stay 1 : up 2 : down 3 : left 4 : right
        self.dir = direction

        #face == 1  面向左  face == 2 面向右
        self.is_face_left = False
        self.xp = xp
        self.sword_code = sword_code
        #可以使用一个字典来保存装备  TODO 后期如果想提高，可以再加。  默认是body0000，然后默认显示鬼剑士的装备，换装，就把对应的字典值换了。
        # self.game_fashion = {"sword" : "beamswd0300","hair" : "0000"}


    def update(self,map_rect):
        #速度，检查按键
        self.check_key()
        #检查地图边界
        self.boundary = GameTool.check_map_boundary(self,map_rect,self.rect)
        # 如果死亡了，播放死亡动画
        if self.is_die:
            print("die")
            pass
            #没做
            # GameTool.cartoon_image()
        else:
            if not self.is_attack:
                self.attack_index = 0
                self.move()
            else:
                self.walk_index = 0
                if self.is_protrusion:
                    self.skill()
                else:
                    self.protrusion_index = 0
                    self.attack()
        self.timer += 1

    def attack(self):
        '''
        人物攻击逻辑
        :return:
        '''

        #第一排是第一段相对于第一张图片的坐标，第二排是第二段相对于第一段第一张图片的坐标，第三排是第三段相对于第一段第一张图片的坐标
        num_list_right = (0,0,0, 0, -1, 1, -21, 13, -17, 16, -12, 16, -11, 16, 2, 17, 2, 17, 2, 17,\
                          10, 15, 12, 14, 12, 14, 1, 16, -23, 15, -44, 16, -32, 16, -14, 16, -7, 16, -2, 16, -2, 16 , \
                          -10, 21, -8, 23, 17, 21, 19, 4, 20, 1, 34, 0, 46, 1, 46, 1, 46, 1
                          )

        right_image = sword_man_constant.ATTACK1_IMAGE
        self.coordinate_deviation(self.attack_index ,self.first_coordinate,num_list_right,self.is_face_left,right_image,True)

        self.attack_index += 1

    def skill(self):
        if self.is_protrusion:
            num_list_right = (0, 0, -18, 0, -9, 4, 5, 7, 3, 8, 11, 9, 28, 9, 29, 9, 29, 9, 29, 9)
            right_image = sword_man_constant.PROTRUSION_IMAGE
            self.coordinate_deviation( self.protrusion_index, self.first_coordinate, num_list_right,
                                       self.is_face_left, right_image, True )
        if self.protrusion_index % 10 == 9:
            self.is_protrusion = False
            self.is_run = False
            self.is_attack = False

        self.protrusion_index += 1

    def check_walk(self):
        speed = sword_man_constant.SPEED

        # 默认让人物的状态为不动
        self.dir[0] = 1
        # 如果发现人物是向上走的，并且没有碰到边界，让不动的那个数值设为0。
        if self.dir[1] == 1 and self.boundary[0] == 0:
            self.dir[0] = 0
            if self.first_coordinate.__len__() != 0:
                self.first_coordinate[1] -= speed
        elif self.dir[2] == 1 and self.boundary[1] == 0:
            self.dir[0] = 0
            if self.first_coordinate.__len__() != 0:
                self.first_coordinate[1] += speed
        # 如果按了上键，并且碰到边界，保持不动。 但是人物走的动画还是会有
        elif self.dir[1] == 1 and self.boundary[0] == 1:
            self.dir[0] = 0
        elif self.dir[2] == 1 and self.boundary[1] == 1:
            self.dir[0] = 0

        if self.dir[3] == 1 and self.boundary[2] == 0:
            # 转向的时候重置一下walk_index
            if self.is_face_left == False:
                self.walk_index = 0
            self.is_face_left = True
            self.dir[0] = 0
            if self.first_coordinate.__len__() != 0:
                self.first_coordinate[0] -= speed
        elif self.dir[4] == 1 and self.boundary[3] == 0:
            # 转向的时候重置一下walk_index
            if self.is_face_left == True:
                self.walk_index = 0
            self.is_face_left = False
            self.dir[0] = 0
            if self.first_coordinate.__len__() != 0:
                self.first_coordinate[0] += speed

        elif self.dir[3] == 1 and self.boundary[2] == 1:
            self.is_face_left = True
            self.dir[0] = 0
        elif self.dir[4] == 1 and self.boundary[3] == 1:
            self.is_face_left = False
            self.dir[0] = 0

    def move(self):
        '''
        人物移动逻辑
        :return:
        '''

        self.check_walk()

        # 如果是不动的情况，将走的坐标重置，播放动画
        if self.dir[0] == 1:
            self.walk_index = 0

            num_list_right = (0, 0, -1, 0, -2, 1, -2, 2, -1, 1, 0, 0)
            right_image = sword_man_constant.STAY_IMAGE
            self.coordinate_deviation( self.stay_index, self.first_coordinate, num_list_right,
                                       self.is_face_left, right_image, True )
            self.stay_index += 1
        # 如果是上下左右走的情况，如果面向右边，播放右边动画，如果面向坐标，播放左边动画。 让不动的图片坐标为0
        else:
            '''
            只有上下左右都为0的时候，才不跑。
            否则按左右的时候，才不跑
            '''
            self.stay_index = 0

            if not self.is_run:
                num_list_right = (0,0,1,-1,1,-1,1,1,-2,0,5,-1,3,-1,4,1)
                right_image = sword_man_constant.WALK_IMAGE
                self.coordinate_deviation( self.walk_index, self.first_coordinate, num_list_right, \
                                           self.is_face_left, right_image, True )

            else:
                num_list_right = (0, 0, 0, 2, 5, -4, -4, 0, 1, 0, 0, 2, 5, -4, -4, 0)
                right_image = sword_man_constant.RUN_IMAGE
                self.coordinate_deviation( self.walk_index, self.first_coordinate, num_list_right, \
                                           self.is_face_left, right_image, True )

            self.walk_index += 1

    def check_key(self):
        '''
        人物按键监听
        :return:
        '''
        keys = pygame.key.get_pressed()
        # TODO 上下左右 人物移动，地图的移动，以及边界限定，先不做
        # TODO 现在这里有一个问题就是当同时按左右或上下的时候，会出现不和谐的情况
        #TODO 改造思想是做一个事件循环，获取键盘按下，当按下右键的时候，把当前方向设置为右。
        #TODO 当按下右键后又按了下左键的时候，把当前方向设置为左，就实现了和dnf一样的效果

        if not keys[pygame.K_UP]:
            self.dir[1] = 0
        if not keys[pygame.K_DOWN]:
            self.dir[2] = 0
        if not keys[pygame.K_LEFT]:
            self.dir[3] = 0
            self.is_first_down_left = True
            #下面这句话说明之前跑步是往左边跑的
            if self.is_run == True and self.is_face_left:
                self.is_run = False

        if not keys[pygame.K_RIGHT]:
            self.dir[4] = 0
            self.is_first_down_right = True
            if self.is_run == True and not self.is_face_left:
                self.is_run = False

        if not keys[pygame.K_x]:
            if self.attack_index % 30 == 9 or self.attack_index % 30 == 20 or self.attack_index % 30 == 29:
                self.is_attack = False

        if keys[pygame.K_UP]:
            self.dir[1] = 1
            self.dir[2] = 0

        elif keys[pygame.K_DOWN]:
            self.dir[2] = 1
            self.dir[1] = 0

        if keys[pygame.K_LEFT]:
            # 如果你一直按左键的话，这句话的作用就是，只存第一次
            if self.is_first_down_left:
                # 如果左键现在的时间为0，就让以前的时间和现在的时间都存一下现在的时间
                if self.current_left_time == 0:
                    self.current_left_time = self.timer
                    self.previous_left_time = self.timer
                # 说明已经不是第一次按下了
                else:
                    # 存下现在的时间，此时的previous_left_time就是上一次按键的时间了，如果两次按键时间小于0.5秒，就让跑步为True。
                    # 如果大于0.5秒，就再存一下现在的时间，等待下一次计算
                    self.current_left_time = self.timer
                    if self.current_left_time - self.previous_left_time <= game_constant.FPS * 0.5:
                        self.is_run = True
                    self.previous_left_time = self.current_left_time
                self.is_first_down_left = False

            self.dir[3] = 1
            self.dir[4] = 0

        elif keys[pygame.K_RIGHT]:
            #如果你一直按右键的话，这句话就是只存第一次按键的时间
            if self.is_first_down_right == True:
                if self.current_right_time == 0:
                    self.current_right_time = self.timer
                    self.previous_right_time = self.timer
                else:
                    self.current_right_time = self.timer
                    if self.current_right_time - self.previous_right_time <= game_constant.FPS * 0.5:
                        self.is_run = True
                    self.previous_right_time = self.current_right_time
                self.is_first_down_right = False

            self.dir[3] = 0
            self.dir[4] = 1

        # 如果按下了x，就让人物攻击。
        # 攻击就是换图片   需要设置一下人物的 攻击状态，如果人物在攻击的话，不能移动
        # TODO 当人物攻击的时候，僵直先不做。 怪物打人，有一点僵直时间，先不做。  这个得想想怎么控制单个精灵的更新速度
        # TODO pygame 有一个可以只控制某一片区域的函数，所以可能需要那个函数来实现
        if keys[pygame.K_x]:
            if self.is_run:
                self.is_protrusion = True
                self.is_attack = True
            else:
                self.is_attack = True

class Sword(Person):
    '''
    这是一个精灵，具备自己移动的能力，当人物穿装备的时候，只需要把这个人物精灵对应的sword的精灵的image更换一下即可
    在创建剑精灵的时候，需要绑定一个英雄
    一把剑分为三部分，一部分是剑的中间部分，一部分是剑的装饰或外形，一部分是剑的把手,所有有个shape属性。
    shape == 0 是剑，shape == 1 是装饰，shape == 2 是把手
    '''
    def __init__(self,image_path,lv,hp,mp,ad,dp,person,shape):
        super().__init__(image_path,lv,hp,mp,ad,dp)

        self.person = person
        self.shape = shape

    def update(self):
        if self.person.is_die:
            # 没做
            GameTool.cartoon_image()
        else:
            if not self.person.is_attack:
                self.move()
            else:
                if self.person.is_protrusion:
                    self.skill()
                else:
                    self.attack()

    def attack(self):
        if self.person.sword_code == "beamswd0300":
            if self.shape == 0:

                num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_attack),(
                                               149, 258, 147, 258, 141, 254, 235, 230, 208, 269, 182, 280, 177, 280, 164,
                                               269, 166, 270, 164, 269, \
                                               187, 255, 192, 250, 293, 254, 163, 265, 127, 256, 125, 243, 109, 241, 111,
                                               243, 109, 241, 111, 243, 109, 241, \
                                               111, 255, 125, 262, 200, 273, 314, 209, 311, 173, 311, 170, 311, 170,
                                               311, 170, 311, 170) ))
                right_image = sword_constant.beamswd0300_ATTACK_IMAGE
                self.coordinate_deviation( self.person.attack_index, self.person.first_coordinate, num_list_right, \
                                           self.person.is_face_left, right_image, False )
            elif self.shape == 1:
                #后面的0意思这个图片为空
                num_list_right = (GameTool.arithmetic_deviation(self,(self.person.body81100_attack),(
                    172,249,172,249,180,248,0,0,0,0,225,275,225,275,225,275,225,275,225,275,\
                    246,271,261,258,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, \
                    0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,

                )))
                right_image = sword_constant.beamswd0300_ATTACK_DECORATE_IMAGE
                self.coordinate_deviation( self.person.attack_index, self.person.first_coordinate, num_list_right, \
                                           self.person.is_face_left, right_image, False )
            elif self.shape == 2:
                num_list_right = (GameTool.arithmetic_deviation(self,(self.person.body81100_attack),(
                    191,233,191,233,208,231,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                    0,0,0,0,0,0,0,0,172,246,172,246,172,246,172,246,172,246,172,246,172,246,\
                    170,263,184,270,0,0,0,0,301,209,301,209,301,209,301,209,301,209
                )))
                right_image = sword_constant.beamswd0300_ATTACK_HANDLE_IMAGE
                self.coordinate_deviation( self.person.attack_index, self.person.first_coordinate, num_list_right, \
                                           self.person.is_face_left, right_image, False )
            # 在挥刀的那一瞬间判定，如果击中，掉血
            if self.person.attack_index % 30 == 3 or self.person.attack_index % 30 == 12 or self.person.attack_index % 30 == 24:
                self.person.is_do_attack = False
            else:
                self.person.is_do_attack = True

    def skill(self):

        if self.person.is_protrusion:
            if self.person.sword_code == "beamswd0300":
                if self.shape == 0:

                    num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_protrusion), (
                        236,247,238,249,269,257,242,240,238,255,222,248,225,245,344,250,340,250,344,250
                        )))
                    right_image = sword_constant.beamswd0300_PROTRUSION_IMAGE
                    self.coordinate_deviation( self.person.protrusion_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
                elif self.shape == 1:
                    # 后面的0意思这个图片为空
                    num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_protrusion), (
                        205,258,207,258,238,262,0,0,0,0,316,256,316,256,316,256,316,256,316,256
                    ) ))
                    right_image = sword_constant.beamswd0300_PROTRUSION_DECORATE_IMAGE
                    self.coordinate_deviation( self.person.protrusion_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
                elif self.shape == 2:
                    num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_protrusion), (
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                    ) ))
                    right_image = sword_constant.beamswd0300_PROTRUSION_HANDLE_IMAGE
                    self.coordinate_deviation( self.person.protrusion_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
                # 在挥刀的那一瞬间判定，如果击中，掉血
                if self.person.protrusion_index % 10 == 3:
                    self.person.is_do_attack = False
                else:
                    self.person.is_do_attack = True

    def move(self):

        if self.person.sword_code == "beamswd0300":
            if self.person.dir[0] == 1:
                if self.shape == 0:
                    num_list_right = (23, 50, 23, 51, 23, 52, 23, 53, 23, 52, 23, 51)
                    right_image = sword_constant.beamswd0300_STAY_IMAGE
                    self.coordinate_deviation( self.person.stay_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
                elif self.shape == 1:
                    num_list_right = (17, 45, 17, 46, 17, 46, 17, 46, 17, 46, 17, 46)
                    right_image = sword_constant.beamswd0300_STAY_DECORATE_IMAGE
                    self.coordinate_deviation( self.person.stay_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
                elif self.shape == 2:
                    num_list_right = (5, 33, 5, 34, 5, 34, 5, 34, 5, 34, 5, 34)
                    right_image = sword_constant.beamswd0300_STAY_HANDLE_IMAGE
                    self.coordinate_deviation( self.person.stay_index, self.person.first_coordinate, num_list_right, \
                                               self.person.is_face_left, right_image, False )
            else:
                if self.person.is_run:

                    if self.shape == 0:
                        num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_run), (
                            154,274,157,273,159,274,157,274,154,274,156,271,156,272,157,274
                            ) ))
                        right_image = sword_constant.beamswd0300_RUN_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate,
                                                   num_list_right, \
                                                   self.person.is_face_left, right_image, False )

                    elif self.shape == 1:
                        num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_run), (
                            195,269,198,268,198,269,196,269,195,269,197,266,197,267,196,269
                        ) ))
                        right_image = sword_constant.beamswd0300_RUN_DECORATE_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate,
                                                   num_list_right, \
                                                   self.person.is_face_left, right_image, False )
                    elif self.shape == 2:
                        num_list_right = (GameTool.arithmetic_deviation( self, (self.person.body81100_run), (
                            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
                        ) ))
                        right_image = sword_constant.beamswd0300_RUN_HANDLE_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate,
                                                   num_list_right, \
                                                   self.person.is_face_left, right_image, False )
                else:
                    if self.shape == 0:
                        # 目前没有HouseStay 所以先不判断，如果有HouseStay，可以在后面加一个HouseStay
                        num_list_right = (40, 69, 38, 69, 37, 70, 38, 70, 40, 69, 43, 69, 44, 70, 43, 70)
                        right_image = sword_constant.beamswd0300_WALK_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate, num_list_right, \
                                                   self.person.is_face_left, right_image, False )
                    elif self.shape == 1:
                        num_list_right = (35, 64, 33, 64, 32, 65, 33, 65, 35, 64, 37, 64, 38, 65, 37, 65)
                        right_image = sword_constant.beamswd0300_WALK_DECORATE_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate, num_list_right, \
                                                   self.person.is_face_left, right_image, False )
                    elif self.shape == 2:
                        num_list_right = (23, 52, 21, 52, 20, 53, 21, 53, 23, 52, 26, 52, 27, 53, 28, 53)
                        right_image = sword_constant.beamswd0300_WALK_HANDLE_IMAGE
                        self.coordinate_deviation( self.person.walk_index, self.person.first_coordinate, num_list_right, \
                                                   self.person.is_face_left, right_image, False )