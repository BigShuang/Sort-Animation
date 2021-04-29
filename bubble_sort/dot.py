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

class BubbleManager:
    def __init__(self, master, x, height):
        self._master = master
        self.bubblelist = []
        self.arr = [i for i in range(1, NUMBER)]
        random.shuffle(self.arr)
        print()

        dy = 0
        for i in range(NUMBER-1):
            v = self.arr[i]
            ir = INIT_R + v * DR
            iy = dy + BUBBLE_SPACE + ir
            dy = iy + ir

            db = DigitalBubble(master, x, WIN_HEIGHT - iy, v, ir)
            self.bubblelist.append(db)

        self.i = 0
        self.iy = 0
        self.j = 0
        self.bubbling = False

        self.count = 0

    def draw(self):
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw(j==self.j)

    def draw_pic(self):
        for j in range(len(self.bubblelist)):
            db = self.bubblelist[j]
            db.draw_pic(j==self.j)

    def draw_text(self):
        if not self.bubble_done():

            info = "i = %s" % self.i + '  ' + '-' * 20
            text_i = bigfont.render(info, 1, COLORS["current"])

            if not self.bubbling:
                self.iy = self.bubblelist[len(self.bubblelist) - 1 - self.i].cy - self.bubblelist[len(self.bubblelist) -1 - self.i].radius \
                          - BUBBLE_SPACE // 2 - text_i.get_height() // 2

            self._master.blit(text_i, (20, self.iy))

            text_j = bigfont.render("j = %s" % self.j, 1, COLORS["current"])
            dbj0 = self.bubblelist[self.j]
            jx = text_i.get_width()
            jy = dbj0.cy - text_j.get_height() // 2
            self._master.blit(text_j, (jx, jy))

    def bubble_done(self):
        return self.i >= NUMBER - 1

    def bubble_j(self):
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