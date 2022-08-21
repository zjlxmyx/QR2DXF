import tkinter as tk
import re

def readTXT(path):
    # 读取txt，一共三行
    # --------------------------
    # size = 60
    # x60
    # cutline_x = [10, 20, 30, 40, 50]
    # cutline_y = [12, 24, 36, 48]
    # --------------------------
    txt = open(path, encoding="utf-8")
    lines = txt.readlines()

    # 用正则表达式提取关键信息
    pattern1 = re.compile(r'\d+x\d+')
    result1 = pattern1.findall(lines[0])
    size = re.split(r'x', result1[0])
    size = list(map(float, size))

    pattern2 = re.compile(r'\[(.+)\]')
    drowLineX = pattern2.findall(lines[1])
    drowLineX = re.split(r'[,;\s*]\s*', drowLineX[0])
    drowLineX = list(map(float, drowLineX))
    drowLineY = pattern2.findall(lines[2])
    drowLineY = re.split(r'[,;\s*]\s*', drowLineY[0])
    drowLineY = list(map(float, drowLineY))

    QRcodeX = [i - 1.5 for i in drowLineX]
    QRcodeX.append(QRcodeX[-1] + 1.5 + 0.9)
    QRcodeY = [i - 1.5 for i in drowLineY]
    QRcodeY.append(QRcodeY[-1] + 1.5 + 0.9)
    # 得坐标size, drowlineX, drowlineY, QRcodeX, QRcodeY后关闭txt
    txt.close()

    # 把坐标转化成canvas输入格式(x1,y1,x2,y2)
    drowLineX.insert(0, 0)
    drowLineX.append(size[0])
    drowLineY.insert(0, 0)
    drowLineY.append(size[1])
    drowLines = []
    for i in drowLineX:
        drowLines.append([i, 0, i, size[1]])
    for j in drowLineY:
        drowLines.append([0, j, size[0], j])

    # QRcode 就简化成一个0.6x0.6的小方块
    drowQR = []
    for k in QRcodeX:
        for l in QRcodeY:
            drowQR.append([k, l, k+0.6, l+0.6])

    print(drowQR,'\n')


    return drowLines, drowQR


def scaling(inputList):
    outputList = [i*3+7 for i in inputList]
    outputList[1] = 210-outputList[1]
    outputList[3] = 210 - outputList[3]
    return outputList



path = r'ttt.txt'



window = tk.Tk()
window.title('')
window.geometry('300x300')

canvas = tk.Canvas(window, bg='white', height=210, width=210)
canvas.pack()

drowLines, drowQR = readTXT(path)
for i in drowLines:
    canvas.create_line(scaling(i), fill='lime')
for j in drowQR:
    canvas.create_rectangle(scaling(j), fill='limeGreen', outline='limeGreen')


window.mainloop()