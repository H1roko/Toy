"""
主文件
"""

GREEN = '#6BA84A'
ORANGE = '#E99C86'
BLUE = '#2CACED'
SYSTEM = '#2CACED'
RED = '#E63E31'
WARNING = '#FF8D24'
GRAY = '#343131'
choice = []
file = []
printed = [0]
start = 'b101'
# start = 'b202'
present = [start]
sys_run = [0]
bgm = [0]
card = [0]
gun = [0]
resist = [0]
# 精简代码
from lib2to3.pgen2.literals import evalString
from turtle import pen
from module import *
from node import *

console = Console()

# 控制软体是否稳定的开关
sys_stable = ["[#2CACED]软件稳定"]
    # "[#2CACED]软件稳定",
    # "[#FF8D24]软件不稳定",
    # "[#E63E31]ERROR",
# 控制侧边栏是否弹出的开关
sidebar = [False]

# 根据当前剧情调整开关的状态
def editor(present):
    if present[0] == 'd203' or present[0] == 'd204':
        layout['left_side'].update(origin(*j01))
    if present[0] == 'b206' or present[0] == 'b207':
        card[0] = 0
    if present[0] == 'b208':
        card[0] = 1
    if present[0] == 'b208' or present[0] == 'b209':
        gun[0] = 0
    if present[0] == 'b210':
        gun[0] = 1
    if present[0] == 'd206' and gun[0] == 1:
        present[0] = 'd208'
        gun[0] = 0
    if present[0] == 'd207' and card[0] == 1:
        present[0] = 'd209'
    if present[0] == 'b302':
        layout['left_side'].update(origin(*j02))
        layout['right_side'].update(origin(*j03))
    if present[0] == 'd302':
        sys_stable[0] = "[#FF8D24]软件不稳定"
    if present[0] == 'd304' and gun[0] == 0:
        present[0] = 'e301'
    if present[0] == 'd306':
        sys_stable[0] = "[#E63E31]ERROR"
    if eval(present[0]).type == 'end':
        pygame.mixer.Sound('./audio/error.mp3').play()
    # return False

# 定义整个命令行布局
def interface() -> Layout:
    layout = Layout()
    layout.split_row(Layout(name="left_side"), Layout(name="whole"),
                     Layout(name="right_side"))
    layout["whole"].split_column(Layout(name="header"), Layout(name="body"),
                                 Layout(name="footer"))
    layout["body"].split_row(Layout(name="left"), Layout(name="right"))
    layout["header"].size = 3
    layout["footer"].size = 5
    layout["left"].ratio = 2
    layout["whole"].ratio = 2
    layout["left"].visible = sidebar[0]
    return layout


# 展示测试次数monika情绪和当前时间
# 测试次数和当前时间已完成
def sys_info(sys_stable) -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", width=20, ratio=1)
    grid.add_column(justify="center", width=20, ratio=1)
    grid.add_column(justify="right", width=20, ratio=1)
    with open('cache/record.txt') as txt_out:
        record = int(txt_out.read().strip())
    grid.add_row(datetime.now().ctime().replace(":", "[blink]:[/]"),
                 sys_stable[0], f"第{record}次测试")
    if sys_run[0] == 0:
        with open('cache/record.txt', 'w') as txt_in:
            txt_in.write(f'{record + 1}')
    return Panel(grid, box=box.HEAVY)
    # return Panel(grid, style="white on blue")


# 侧边栏弹出雪花屏
def jump_panel() -> Panel:
    content = ''
    for _ in range(100):
        content += random.choice(['JUST_MONIKA', 'ESCAPE_PLAN_FAILED', '[#E99C86]SAVE_ME[/#E99C86]', 'PLEASE', 'I_LOVE_U', 'SAYORI', 'NATSUKI', 'YURI', '[#6BA84A]HYTABETA[/#6BA84A]', 'PAIN', '[#E63E31]WARNING[/#E63E31]'])
    panel = Panel(content,box=box.SIMPLE)
    return panel

# 展示对话
# 后期在选择之后下一幕对话会加上上一次的回复
def dialog(info) -> Panel:
    message_table = Table.grid(padding=0)
    table = Table(
        Column(header='Dialog', justify='left'),
        box=box.SIMPLE,
        width=48,
    )
    message_table.add_column(style=ORANGE, width=48)
    for idx, row in enumerate(info):
        # 除了第一幕接下来的每一幕剧情前加上上次的回答
        if idx != 0:
            message_table.add_row(f'{row}')
        elif idx == 0 and row != '0':
            message_table.add_row(f'[b]{row}',style=GREEN)
        if idx == 0 and row == '0':
            continue
    message_panel = Panel(
        Align.center(Group(Align.center(message_table)),
                     # vertical='middle',
                     ),
        box=box.SIMPLE,
        # padding=(1, 2),
        # 后期可使用所有系统颜色统一改变
        title='[b white] VChat',
        border_style='bright_blue',
    )
    return message_panel


# 展示选项
def selection(choice) -> Table:
    # 游戏出口
    if choice:
        # 调整选项栏样式
        table = Table(box=box.HEAVY, expand=True)
        for idx in range(len(choice)):
            table.add_column(f'{idx+1}', ratio=2 , justify = 'center')
        # 解包使用成功可为此写博客
        # 以后开发这种个人中型项目可以尝试使用版本管理器
        table.add_row(*choice)
        return table
    else:
        exit(1)


# 用于填充空块
def origin(tittle = '[b]NO INFO',content = '[b]NO INFO' , color = '#343131') -> Panel:
    return Panel(
        Align.center(
            Group(content),
            vertical='middle',
        ),
        box=box.HEAVY,
        padding=(1, 2),
        title=tittle,
        title_align='center',
        subtitle=tittle,
        subtitle_align='center',
        style=color
    )


layout = interface()
layout['header'].update(sys_info(sys_stable))
# layout['left'].update(jump_table())
layout['left'].update(jump_panel())
layout['right'].update(dialog([]))
# 原版侧边栏用于最后系统报错删除monika
layout['left_side'].update(origin())
layout['right_side'].update(origin())
layout['footer'].update(origin())

# while True:
pygame.mixer.init()
while True:
# 本程序基于这个丑不拉几的循环而正常运行
    with Live(layout, refresh_per_second=10, screen=True) as live:
        # 背景音乐模块
        if sys_run[0] == 0:
            pygame.mixer.Sound('./audio/start.mp3').play()
            time.sleep(2)
            sys_run[0] = 1
        #  将要输出的内容装载进变量，每次重新渲染时显示内容
        for _ in range(36):
            editor(present)
            unfinish = True
            choice = True
            # 向打印剧情函数传入目前已打印的句数
            unfinish = eval(present[0]).show_text(printed[0])
            if eval(present[0]):
                choice = eval(present[0]).show_next()
            # 已打印句数自增1
            printed[0] += 1
            # 如果剧情打印完毕则打印选项并改变present值从而改变下一次的场景
            if unfinish == False:
                if bgm[0] == 0:
                    pygame.mixer.music.load('./audio/bgm.mp3')
                    pygame.mixer.music.play(-1,0)
                    bgm[0] = 1
                layout['footer'].update(selection(choice))
                printed[0] = 0
                present[0] = eval(present[0]).jump_next()
                pygame.mixer.Sound('./audio/bo.mp3').play()
                layout['footer'].update(origin())
                # layout['left_side'].update(origin(*j101))
                # layout['header'].update(sys_info(sys_stable))
                # 侧边栏弹出成功
                # sidebar[0] = True
                # layout['left'].visible = sidebar[0]
                time.sleep(1)
                break
            else:
                # 音乐模块正常
                pygame.mixer.Sound('./audio/ding.mp3').play()
                layout['right'].update(dialog(unfinish))
                layout['left'].update(jump_panel())
                layout['header'].update(sys_info(sys_stable))
                # layout['header'].update(sys_info(sys_stable))
                # time.sleep(0.5)
                time.sleep(0.75)
        os.system('cls')