#-*- coding:utf-8 -*-

'''
关于游戏的常量定义

pygame 在windows中(0,0)的坐标  (360,195)

1920*1080  在ps中  1厘米 = 37.78538812785388像素
我们的Pygame窗口一共18.26厘米  上半部分为8.76厘米 下面部分为9.5厘米

1200*690
31.758308 厘米   *
18.261027 厘米
'''

# FPS = 13
FPS = 13


#game Title
WINDOW_TITLE = "三月丛林 v1.0 三月软件·Python组出品"
#game icon
GAME_ICON = '../image_package/images/game_icon.ico'
#Get caption high
SCREEN_SIZE_CAPTION_High = 5
#Get screen wide and high
SCREEN_SIZE = (1200,690)
MOUSE_STYLE = '../image_package/images/mouse_style.png'
MOUSE_STYLE_EMPTY = '../image_package/images/mouse_style_empty.png'
#login background image
LOGIN_BACKGROUND = '../image_package/images_login/background.png'
LOGIN_BACKGROUND_ROLE = '../image_package/images_login/background_role.png'
LOGIN_BACKGROUND_ROLE_COORDINATE = (0, SCREEN_SIZE_CAPTION_High)
#Server select background
LOGIN_SERVER_SELECT = '../image_package/images_login/background_server_select.png'
LOGIN_SERVER_SELECT_COORDINATE = (500,10)

#select area btn_go
BTN_AREA_GO_1 = '../image_package/images_login/btn_area_go_1.png'
BTN_AREA_GO_2 = '../image_package/images_login/btn_area_go_2.png'
BTN_AREA_GO_CLOSE = '../image_package/images_login/btn_area_go_close.png'
BTN_AREA_GO_COORDINATE = (930, 550)
BTN_AREA_GO_SIZE = (232,59)

#area of sanyue btn
BTN_SELECT_AREA_1 = '../image_package/images_login/btn_select_area_1.png'
BTN_SELECT_AREA_2 = '../image_package/images_login/btn_select_area_2.png'
BTN_SELECT_AREA_3 = '../image_package/images_login/btn_select_area_3.png'
#First coordinate of area btn
BTN_SELECT_AREA_COORDINATE = (550,75)
#area btn size
BTN_SELECT_AREA_SIZE = (105,39)

#area named python of sanyue area btn.
BTN_SELECT_SERVER_1 = '../image_package/images_login/btn_select_server_1.png'  #104*39
BTN_SELECT_SERVER_2 = '../image_package/images_login/btn_select_server_2.png'  #104*39
BTN_SELECT_SERVER_3 = '../image_package/images_login/btn_select_server_3.png'  #115*51
#First coordinate of server btn
BTN_SELECT_SERVER_COORDINATE = (550, 326)
BTN_SELECT_SERVER2_COORDINATE = (550+130, 326)
#server btn size
BTN_SELECT_SERVER_SIZE = (105,39)

#Python服务器的文本和size
TEXT_SERVER_PYTHON = '../image_package/images_login/text_server_python.png'
TEXT_SERVER_PYTHON_SIZE = (37, 13)
#Java尖刀服务器
TEXT_SERVER_JIANDAO = '../image_package/images_login/text_server_Java尖刀.png'
TEXT_SERVER_JIANDAO_SIZE = (47,12)
#三月大区的文本和size
TEXT_AREA_SANYUE = '../image_package/images_login/text_area_sanyue.png'
TEXT_AREA_SANYUE_SIZE = (57, 11)

#流畅度图片
FLUENCY_FLUENT = '../image_package/images_login/fluency_fluent.png'
FLUENCY_FLUENT_SIZE = (9,9)

#login button name
SIGNIN_BUTTON_NAME = "Sign in"
SIGNUP_BUTTON_NAME = "Sign up"

#map_background_select_checkpoint_luolan
MAP_SELECT_BACKGROUND_LUOLAN = '../image_package/map_luolan/map_back_select_luolan.png'

MAP_SELECT_LUOLAN = '../image_package/map_luolan/map_luolan.png'
MAP_SELECT_LUOLAN_COORDINATE = (201,381)
MAP_SELECT_LUOLAN_SIZE = (252,110)

MAP_SELECT_LUOLAN_DIFFICULTY = '../image_package/map_luolan/map_luolan_difficulty.png'
MAP_SELECT_LUOLAN_DIFFICULTY_SIZE = (252,110)

# MAP_BACKGROUND_LUOLAN = '../image_package/map_luolan/map_back_luolan_big.png'
MAP_BACKGROUND_LUOLAN = '../image_package/map_luolan/map_back_luolan_small.png'
#不加胡超界面前的地图边界
# LUOLAN_BOUNDARY_RECT = (0,280,1200,685)
LUOLAN_BOUNDARY_RECT = (0,280,1200,500)

MAP_LAND_BARREL = '../image_package/map_luolan/luolan_land_barrel.png'
MAP_LAND_TRUE = '../image_package/map_luolan/luolan_land_true.png'



