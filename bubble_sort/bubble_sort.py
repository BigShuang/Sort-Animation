# usr/bin/env python
# -*- coding:utf-8- -*-
from animationgui import BubbleAnimation


def bubble_sort_animation(arr):
    n = len(arr)
    animation = BubbleAnimation(arr)
    for i in range(n):
        animation.update(i=i, j=-1)
        for j in range(0, n - i - 1):
            animation.update(j=j)
            vj0, vj1 = arr[j], arr[j+1]
            if vj0 > vj1:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                animation.bubble_j()

    animation.done()


a = [4, 1, 5, 9, 8, 6, 3, 2, 7]
bubble_sort_animation(a)
