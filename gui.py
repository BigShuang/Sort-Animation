import pygame
import sys


from bubble_sort.dot import DigitalBubble, BubbleManager
from bubble_sort.constants import *


pygame.init()  # pygame初始化，必须有，且必须在开头
# 创建主窗体
clock = pygame.time.Clock()  # 用于控制循环刷新频率的对象
font = pygame.font.Font("./font/simkai.ttf", 20)


win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Bubble sort animation - made by Big Shuang")

def together():
    bmlist = []
    for i in range(1, 10):
        x = WIN_WIDTH // 10 * i
        bm = BubbleManager(win, x, WIN_HEIGHT)
        bmlist.append(bm)
    start = False
    while True:
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start = True

        if start:
            if any(bm.bubbling for bm in bmlist):
                for bm in bmlist:
                    bm.bubble_j()
            elif not all(bm.bubble_done() for bm in bmlist):
                for bm in bmlist:
                    bm.bubble_once()
            else:
                for bm in bmlist:
                    bm.j = -1

        win.fill(COLORS["bg"])
        for bm in bmlist:
            bm.draw()
        if any(bm.bubbling for bm in bmlist):
            clock.tick(QUICKFPS)
        else:
            clock.tick(SLOWFPS)
        pygame.display.update()


def in_order():
    bmlist = []
    count = 15
    for i in range(1, count):
        x = WIN_WIDTH // count * i
        bm = BubbleManager(win, x, WIN_HEIGHT)
        bmlist.append(bm)
    start = False
    while True:
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start = True

        if start:
            for bm in bmlist:
                if bm.bubbling:
                    bm.bubble_j()
                elif not bm.bubble_done():
                    bm.bubble_once()
                else:
                    bm.j = -1

        win.fill(COLORS["bg"])
        for bm in bmlist:
            bm.draw_pic()

        clock.tick(FPS)
        pygame.display.update()


def contrast():
    bm = BubbleManager(win, WIN_WIDTH//2, WIN_HEIGHT)
    start = False
    while True:
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start = True

        if start:
            if bm.bubbling:
                bm.bubble_j()
            elif not bm.bubble_done():
                bm.bubble_once()
            else:
                bm.j = -1

        win.fill(COLORS["bg"])
        bm.draw_pic()
        bm.draw_text()

        clock.tick(FPS)
        pygame.display.update()


def sortone():
    bm = BubbleManager(win, WIN_WIDTH//2, WIN_HEIGHT)
    start = False
    while True:
        # 获取所有事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 判断当前事件是否为点击右上角退出键
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                start = True

        if start:
            if bm.bubbling:
                bm.bubble_j()
            elif not bm.bubble_done():
                bm.bubble_once()
            else:
                bm.j = -1

        win.fill(COLORS["bg"])
        bm.draw()

        clock.tick(FPS)
        pygame.display.update()


in_order()
# sortone()