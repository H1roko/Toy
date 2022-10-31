# 可以改变pygame的窗口图标
# 可以设计一个控制器界面
# 可以将控制器的输入类型设置为鼠标点击和按钮
from module import *


def controller():

    pygame.init()

    # 创建窗口
    controller_window = pygame.display.set_mode((320, 160))
    # 设置窗口标题
    pygame.display.set_caption('Monika Controller')
    # 加载资源图片，返回图片对象
    image = pygame.image.load('images/favicon.ico')
    # 设置窗口图标
    pygame.display.set_icon(image)

    background = pygame.image.load('images/panel.png')
    button_1 = pygame.image.load('images/button_1.png')
    button_2 = pygame.image.load('images/button_2.png')
    button_3 = pygame.image.load('images/button_3.png')
    button_4 = pygame.image.load('images/button_4.png')
    #将背景图片贴到窗口里去
    controller_window.blit(background,(0,0))
    controller_window.blit(button_1,(160,24))
    controller_window.blit(button_2,(232,24))
    controller_window.blit(button_3,(160,84))
    controller_window.blit(button_4,(232,84))

    corner_1 = (160,24)  #Top Left corner of button_1
    corner_2 = (232,24)  #Top Left corner of button_2
    corner_3 = (160,84)  #Top Left corner of button_1
    corner_4 = (232,84)  #Top Left corner of button_2

    image_length = 60 #length of the buttons
    image_height = 50 #height of the buttons

    clock = pygame.time.Clock()
    crashed = False
    # 后期利用一些常量提升可读性
    while not crashed:
        pygame.event.clear()
        event = pygame.event.wait()
        #判断事件类型
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                return 1
            elif event.key == pygame.K_2:
                return 2
            elif event.key == pygame.K_3:
                return 3
            elif event.key == pygame.K_4:
                return 4
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                if (mouse_x >= corner_1[0]) and (mouse_x <= corner_1[0]+image_length) and (mouse_y >= corner_1[1]) and (mouse_y <= corner_1[1]+image_height):
                    return 1
                if (mouse_x >= corner_2[0]) and (mouse_x <= corner_2[0]+image_length) and (mouse_y >= corner_2[1]) and (mouse_y <= corner_2[1]+image_height):
                    return 2
                if (mouse_x >= corner_3[0]) and (mouse_x <= corner_3[0]+image_length) and (mouse_y >= corner_3[1]) and (mouse_y <= corner_3[1]+image_height):
                    return 3
                if (mouse_x >= corner_4[0]) and (mouse_x <= corner_4[0]+image_length) and (mouse_y >= corner_4[1]) and (mouse_y <= corner_4[1]+image_height):
                    return 4
            # 猜想输入溢出后会据此对后面的结点自动选择的原因
            # 在return后controller函数不再执行
            # 但并没有消除创建的pygame窗口
            # pygame窗口会继续监视输入活动并将其放入pygame.event.get()
            # 下次再次调用controller函数时则会从pygame函数中获取之前的输入活动
            # 目前的解决方案猜想是每次调用controller函数时清空

            # 每次return伴随着pygame视窗的关闭是可行的

            # 在while循环前进行event清空后问题仍然存在
            # 推测是return后controller函数未被销毁
            # 目前的解决猜想是在return前清空event队列
            # 以后读到经典的用于学习的example要保存下来避免未来找不到

            # 难道溢出的操作被放进了某个输入流中？

            # 并非是进入某个输入流，事实上先clear再wait就可以
            # wait不会让接收进入下一次循环
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()