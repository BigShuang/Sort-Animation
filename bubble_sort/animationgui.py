#usr/bin/env python
#-*- coding:utf-8- -*-
import pygame
import random

from constants import *


pygame.init()  # pygame初始化，必须有，且必须在开头
font = pygame.font.Font("./font/simkai.ttf", 20)
bigfont = pygame.font.Font("./font/simkai.ttf", 30)

class DigitalBubble:
    speed = 2  # 速度
    color = COLORS["bubble"]

    def __init__(self, master, x, y, v, r):
        self._master = master  # 父控件
        self.cx = x
        self.cy = y
        self.v = v
        self.on = True
        self.radius = r

        self.image = pygame.image.load("img/bubble.png")
        self.select_image = pygame.image.load("img/select.png")
        self.resize()

    def resize(self):
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.select_image = pygame.transform.scale(self.select_image, (self.radius * 2, self.radius * 2))

    # 更新子弹位置，移动子弹
    def up(self):
        self.cy -= DR

    def down(self):
        self.cy += DR

    # 绘制
    def draw(self, current=False):
        text = font.render(str(self.v), 1, COLORS["current"])
        if current:
            # pygame.draw.circle(self._master, self.color, (self.cx, self.cy), self.radius)
            pygame.draw.circle(self._master, COLORS["select"], (self.cx, self.cy), self.radius)
        else:
            pygame.draw.circle(self._master, self.color, (self.cx, self.cy), self.radius)
        text_width = text.get_width()
        text_height = text.get_height()
        self._master.blit(text, (self.cx - text_width // 2, self.cy - text_height // 2))

    def draw_pic(self, current=False):
        if current:
            self._master.blit(self.select_image, (self.cx - self.radius, self.cy - self.radius))
        else:
            self._master.blit(self.image, (self.cx - self.radius, self.cy - self.radius))

        text = font.render(str(self.v), 1, COLORS["current"])
        text_width = text.get_width()
        text_height = text.get_height()
        self._master.blit(text, (self.cx - text_width // 2, self.cy - text_height // 2))

import os

class BubbleAnimation:
    def __init__(self, arr):
        pygame.init()  # pygame初始化，必须有，且必须在开头
        # 创建主窗体
        self.clock = pygame.time.Clock()  # 用于控制循环刷新频率的对象

        pos_x, pos_y = 20, 40
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (pos_x, pos_y)
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

        pygame.display.set_caption("Bubble sort animation - made by Big Shuang")

        self.bubblelist = []
        self.arr = arr
        self.number = len(self.arr)

        dy = 0
        for i in range(self.number):
            v = self.arr[i]
            ir = INIT_R + v * DR
            iy = dy + BUBBLE_SPACE + ir
            dy = iy + ir

            db = DigitalBubble(self.win, WIN_WIDTH // 2, WIN_HEIGHT - iy, v, ir)
            self.bubblelist.append(db)

        self.i = -1
        self.iy = 0
        self.j = -1
        self.jy = 0
        self.bubbling = False

        self.count = 0
        self.display()

    def draw(self):
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw(j==self.j)

    def draw_pic(self):
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw_pic(j==self.j)

    def draw_line(self):
        if not self.bubble_done():
            if self.i >= 0:
                 pygame.draw.line(self.win, COLORS['line'], (0, self.iy), (WIN_WIDTH, self.iy))

    def draw_text(self):
        if not self.bubble_done():
            if self.i >= 0:
                info = "i = %s" % self.i
                text_i = bigfont.render(info, 1, COLORS["current"])

                if not self.bubbling:
                    self.iy = self.bubblelist[- (1 + self.i)].cy - self.bubblelist[- (1 + self.i)].radius \
                              - BUBBLE_SPACE // 2

                self.win.blit(text_i, (20, WIN_HEIGHT - text_i.get_height()*2))
                if self.j >= 0:
                    text_j = bigfont.render("j = %s" % self.j, 1, COLORS["current"])
                    if not self.bubbling:
                        self.jy = self.bubblelist[self.j].cy
                    jx = text_i.get_width()+100
                    self.win.blit(text_j, (jx, self.jy- text_j.get_height() // 2))

    def bubble_done(self):
        return self.i > self.number - 1

    def bubble_j(self):
        self.bubbling = True
        while self.bubbling:
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

            self.display(True)

    def update(self, i=None, j=None):
        if i is not None:
            self.i = i
        if j is not None:
            self.j = j

        self.display()

    def display(self, quick=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()
        self.win.fill(COLORS["bg"])
        self.draw_pic()
        self.draw_text()
        self.draw_line()
        pygame.display.update()
        if quick:
            self.clock.tick(FPS)
        else:
            self.clock.tick(SLOWFPS)

    def done(self):
        self.clock.tick(SLOWFPS)
        self.i = -1
        self.display()
        while True:
            # 获取所有事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # 判断当前事件是否为点击右上角退出键
                    pygame.quit()

            self.clock.tick(FPS)
            pygame.display.update()