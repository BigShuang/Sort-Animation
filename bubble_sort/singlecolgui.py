# usr/bin/env python
# -*- coding:utf-8- -*-
import pygame
import random

FPS = 60  # 游戏帧率

WIN_WIDTH = 560  # 窗口宽度
WIN_HEIGHT = 960  # 窗口高度

BUBBLE_SPACE = 40  # 气泡之间的间距
INIT_R = 10  # 气泡初始大小-半径
DR = 3  # 气泡数字值一个单位对应的气泡半径增加量
NUMBER = 10  # 气泡个数

COLORS = {
    "bg": (240, 255, 255),  # 背景颜色
    "bubble": (135, 206, 235),  # 气泡颜色
    "select": (0, 139, 139),  # 被选择的气泡颜色
    "text": (0, 0, 0),  # 文本颜色
}

pygame.init()  # pygame 初始化，必须有，且必须在开头
try:
    # 如果你电脑自带有Arial字体，这里可以直接运行，（一般电脑都会有的）
    font = pygame.font.SysFont("Arial", 20)
except Exception:
    # 如果你本地没有Arial字体，你需要在项目里面建立一个font文件夹存放simkai.ttf字体文件，
    font = pygame.font.Font("./font/simkai.ttf", 20)


class Bubble:
    speed = 2  # 速度
    color = COLORS["bubble"]

    def __init__(self, master, x, y, v, r):
        self._master = master  # 父控件
        self.cx = x  # 气泡中心横坐标 - x
        self.cy = y  # 气泡中心纵坐标 - y
        self.v = v  # 气泡内部数字
        self.radius = r  # 气泡半径

        # 注释说明1-1
        # 由于pygame自己绘制的圆锯齿太大，看起来十分不光滑
        # 想要光滑的圆，只能从png文件中导入圆的图片（图片可前往我的github下载）
        # 这一部分对于单纯的pygame动画学习者而言，并不是非常重要，所以我把与此相关的代码都给注释掉了
        # 有需要的把所有标明注释说明1-1的代码解注释就好
        self.image = pygame.image.load("img/bubble.png")
        self.select_image = pygame.image.load("img/select.png")
        self.resize()

    def up(self):
        # 气泡上浮
        self.cy -= DR

    def down(self):
        # 气泡下沉
        self.cy += DR

    # 绘制气泡
    def draw(self, current=False):
        text = font.render(str(self.v), 1, COLORS["text"])
        if current:
            pygame.draw.circle(self._master, COLORS["select"], (self.cx, self.cy), self.radius)
        else:
            pygame.draw.circle(self._master, self.color, (self.cx, self.cy), self.radius)
        text_width = text.get_width()
        text_height = text.get_height()
        self._master.blit(text, (self.cx - text_width // 2, self.cy - text_height // 2))

    # 见注释说明1-1
    def resize(self):
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.select_image = pygame.transform.scale(self.select_image, (self.radius * 2, self.radius * 2))
    def draw_pic(self, current=False):
        if current:
            self._master.blit(self.select_image, (self.cx - self.radius, self.cy - self.radius))
        else:
            self._master.blit(self.image, (self.cx - self.radius, self.cy - self.radius))

        text = font.render(str(self.v), 1, COLORS["text"])
        text_width = text.get_width()
        text_height = text.get_height()
        self._master.blit(text, (self.cx - text_width // 2, self.cy - text_height // 2))


class BubbleManager:
    def __init__(self, master, x, height, arr=[]):
        self._master = master  # 父控件窗体
        self.bubblelist = []  # bubble列表
        # 数组
        if arr:
            self.arr = arr
        else:
            self.arr = [i for i in range(1, NUMBER)]
            random.shuffle(self.arr)

        # 根据数组中的数字建立Bubble对象，添加到bubblelist中
        # 注意动画界面是从下往上展示数组的元素的
        top_h = 0  # 上一个气泡最高点到底部的距离（即圆心到底的距离加上气泡半径），初始为0
        for i in range(NUMBER-1):
            v = self.arr[i]
            vr = INIT_R + v * DR  # 数字对应的半径大小
            center_h = top_h + BUBBLE_SPACE + vr  # 当前气泡圆心到界面底部的距离
            top_h = center_h + vr  # 记录当前气泡最高点到底部的距离，供下一个使用

            bubble_i = Bubble(master, x, WIN_HEIGHT - center_h, v, vr)
            self.bubblelist.append(bubble_i)

        # 用于记录冒泡排序过程的值
        self.i = 0
        self.j = 0

        # 记录当前气泡j是否正在上浮
        self.bubbling = False

        # 控制动画播放速度
        self.count = 0

    def draw(self):
        # 绘制所有气泡
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw(j==self.j)

    def bubble_done(self):
        # 检查冒泡排序是否完成
        return self.i >= NUMBER - 1

    def bubble_j(self):
        # 气泡j上浮动画
        if not self.bubbling:
            return

        dbj0 = self.bubblelist[self.j]
        dbj1 = self.bubblelist[self.j+1]

        if dbj0.cy - dbj0.radius > dbj1.cy + dbj1.radius:
            # j气泡在下
            dbj0.up()
            dbj1.down()
        elif dbj0.cy > dbj1.cy:
            # 气泡相交
            cy0 = dbj0.cy
            dbj0.cy = dbj1.cy - dbj1.radius + dbj0.radius
            dbj1.cy = cy0 - dbj1.radius + dbj0.radius
        elif (dbj1.cy - dbj1.radius) - (dbj0.cy + dbj0.radius) < BUBBLE_SPACE:
            dbj0.up()
            dbj1.down()
        else:
            self.bubblelist[self.j] = dbj1
            self.bubblelist[self.j+1] = dbj0
            self.bubbling = False
            self.j += 1
            return

    def bubble_once(self):
        # 进行一次冒泡排序
        if self.j >= NUMBER - self.i - 2:
            self.i += 1
            self.j = 0
        else:
            if self.arr[self.j] > self.arr[self.j + 1]:
                if self.count > 5:
                    self.count = 0
                else:
                    self.count += 1
                    return
                self.bubbling = True
                self.arr[self.j], self.arr[self.j + 1] = self.arr[self.j + 1], self.arr[self.j]
                self.bubble_j()
            else:
                if self.count > 10:
                    self.count = 0
                    self.j += 1
                else:
                    self.count += 1

    # 见注释说明1-1
    def draw_pic(self):
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw_pic(j==self.j)


class Gui:
    def __init__(self, width, height, count, fps=FPS, arr=[]):
        self.win = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        pygame.display.set_caption("Bubble sort animation - made by Big Shuang")

        self.bmlist = []
        for i in range(1, count):
            x = WIN_WIDTH // count * i
            bm = BubbleManager(self.win, x, WIN_HEIGHT)
            self.bmlist .append(bm)

        self.start = False

    def loop(self):
        while True:
            # 获取所有事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 判断当前事件是否为点击右上角退出键
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    # 点击任意键开始动画
                    self.start = True

            if self.start:
                for bm in self.bmlist :
                    if bm.bubbling:
                        bm.bubble_j()
                    elif not bm.bubble_done():
                        bm.bubble_once()
                    else:
                        bm.j = -1

            self.win.fill(COLORS["bg"])
            for bm in self.bmlist:
                bm.draw_pic()

            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    gui = Gui(WIN_WIDTH, WIN_HEIGHT, 2)
    gui.loop()
