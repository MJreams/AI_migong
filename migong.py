#Create by wwx on 2018/12/13
# -*- coding: UTF-8 -*-

import pygame
from tkinter import *
from pygame.locals import *

# 定义二维数组的大小
HEIGHT = 20
WIDTH = 20
# 定义pygame的一些变量
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)

FIELD_SIZE = HEIGHT * WIDTH  # 字段大小等于长乘以宽
board = [0] * FIELD_SIZE  # [0,0,0,......]   一维数组的初始化
#  111111 100001 100001 100001 100001 111111#
# 1111111111 1001000101 1001000101 1000011001 1011100001 1000100001 1010001001 1011101101 1100000001 1111111111#
dirs = [
    lambda x, y: (x, y + 1),  # 右    #lambda 是匿名函数
    lambda x, y: (x + 1, y),  # 下
    lambda x, y: (x, y - 1),  # 左
    lambda x, y: (x - 1, y),  # 上
]

def Z_to_S(stack):#将栈转化成字符串
    st = [str(i) for i in stack]
    s = ' '.join(st)
    return s
def Z(MI):#根据MI确定开辟的列表大小
    z = 0
    for i in MI:
        if i != ' ':
            z += 1
        else:
            break
    return z

def ZH(MI):#转化成二维数组
    z = Z(MI)
    MyList = [[] for i in range(z)]
    j = 0
    for i in MI:
        if j < z and i != ' ' and i != '#':
            MyList[j].append(int(i))
        else:
            j += 1
    return MyList
def py_init(MI):# 创建pygame显示层：
    pygame.init()  # 初始化pygame
    fpsClock = pygame.time.Clock()
    playSurface = pygame.display.set_mode((300, 300))  # 创建一个300*300的窗口
    pygame.display.set_caption('迷宫')  # 游戏的title
    playSurface.fill(blackColor)  # 绘制pygame显示层

    j = 0
    z = Z(MI)
    for i in MI:
        board[j] = i
        j += 1
        p = 0#定义列
        q = 0#定义行
    #画出迷宫的图形
    for i in board:
        if i != '#':
            body = p * WIDTH + q
            if i != ' ':
                q += 1
                if q == 2 and p == 1:
                    pygame.draw.rect(playSurface, greenColor, Rect(18 * (body / WIDTH), 18 * (body % WIDTH), 18,18))  # 迷宫的起点
                elif int(i) > 0:
                    pygame.draw.rect(playSurface, whiteColor, Rect(18 * (body / WIDTH), 18 * (body % WIDTH), 18,18))  # 这里的1和2是垂直排列  数值为1 * WIDTH + 1    第一个1为列，第二个为行
                elif int(i) == 0:
                 pygame.draw.rect(playSurface, redColor, Rect(18 * (body / WIDTH), 18 * (body % WIDTH), 18,18))  # 这里的1和2是垂直排列  数值为1 * WIDTH + 1    第一个1为列，第二个为行

            if i == ' ':
                p += 1
                q = 0
        if i == '#':
            break
    body = (z-2) * WIDTH + (z-2)
    pygame.draw.rect(playSurface, greenColor, Rect(18 * (body / WIDTH), 18 * (body % WIDTH), 18,18))  # 这里的1和2是垂直排列  数值为1 * WIDTH + 1    第一个1为列，第二个为行
    #  刷新pygame显示层
    pygame.display.flip()

    MyList = ZH(MI)
    S = DFS(1, 1, z - 2, z - 2, MyList)#s是一个字符串
    if S !='无路可走':
        #print(len(S))
        #print(S)
        sp = 1
        sq = 4
        while sq < len(S):#1,4,8,11 每次加7
            body = int(S[sp]) * WIDTH + int(S[sq])
            pygame.draw.rect(playSurface, greenColor, Rect(18 * (body / WIDTH), 18 * (body % WIDTH), 18,18))  # 这里的1和2是垂直排列  数值为1 * WIDTH + 1    第一个1为列，第二个为行
            sp += 7
            sq += 7
            pygame.display.flip()
            fpsClock.tick(10)  # 20看上去速度正好
    #return MI

def DFS(x1,y1,x2,y2,MyList):#搜索
    stack = []#列表模拟栈
    stack.append((x1,y1))
    MyList[x1][y1] = 2  # 表示已经走过的路
    while len(stack) > 0:
        cur_node = stack[-1]
        if cur_node == (x2, y2):
            s = Z_to_S(stack)
            return s#将模拟栈返回出来
            #return True
        for d in dirs:
            next_x, next_y = d(*cur_node)
            if MyList[next_x][next_y] == 0:
                stack.append((next_x, next_y))
                MyList[next_x][next_y] = 2
                break
        else:
            stack.pop()
    s = '无路可走'
    return s
def get():#获取数据之后进行的操作
    MI = e.get()  # 获取输入框内的数据，为一个列表[1,1,1,1,1,1,1,1,]
    py_init(MI)#
    z = Z(MI)
    MyList = ZH(MI)
    s = DFS(1, 1, z-2, z-2, MyList)
    p = StringVar()
    text = Entry(width=200, textvariable=p).pack()
    p.set(s)

if __name__ == '__main__':
    #创建python gui 图形化界面
    tk = Tk()
    tk.title("迷宫问题")
    tk.geometry("600x400+200+100")#更改大小和位置。600x400改变大小，200+100改变位置-
    Label(tk,text='迷宫问题求解',font=('Arial',20)).pack()
    e = StringVar()
    Label(tk,text='请在如下位置输入迷宫（1为围墙，0为路径）：',compound='right',font=('Arial',10)).pack()
    text = Entry(width = 200,textvariable = e).pack()
    button = Button(tk, text="提交", command=get).pack()
    Label(tk, text='以下为迷宫的路径：', compound='right', font=('Arial', 10)).pack()
    tk.mainloop()