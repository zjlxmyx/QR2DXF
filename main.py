import os
import re
from time import strftime, localtime
import qrcode
import numpy as np
from dxfwrite import DXFEngine as dxf
from tkinter import Label, Entry, Button, Tk, END, INSERT, Canvas
from tkinter import messagebox
from tkinter import filedialog

global g_size, g_QRcodeX, g_QRcodeY
def readTXT(path):
    global g_size, g_QRcodeX, g_QRcodeY

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
    g_size = size

    pattern2 = re.compile(r'\[(.+)\]')
    drowLineX = pattern2.findall(lines[1])
    drowLineX = re.split(r'[,;\s*]\s*', drowLineX[0])
    drowLineX = list(map(float, drowLineX))
    drowLineY = pattern2.findall(lines[2])
    drowLineY = re.split(r'[,;\s*]\s*', drowLineY[0])
    drowLineY = list(map(float, drowLineY))

    QRcodeX = [i - 1.5 for i in drowLineX]
    QRcodeX.append(QRcodeX[-1] + 1.5 + 0.9)
    g_QRcodeX = QRcodeX
    QRcodeY = [i - 1.5 for i in drowLineY]
    QRcodeY.append(QRcodeY[-1] + 1.5 + 0.9)
    g_QRcodeY = QRcodeY
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

    return size, drowLines, drowQR, drowLineX, drowLineY


def scaling(inputList):
    outputList = [i*5+10 for i in inputList]
    outputList[1] = 350-outputList[1]
    outputList[3] = 350-outputList[3]
    return outputList


def showDXF():

    canvas.delete("all")
    path = filedialog.askopenfilename()
    size, drowLines, drowQR, drowLineX, drowLineY= readTXT(path)

    txt_size.config(state='normal')
    txt_size.delete(0, 'end')
    txt_size.insert(INSERT, str(size[0])+' x '+str(size[1]))
    txt_size.config(state='readonly')

    txt_cutline_X.config(state='normal')
    drowLineX.pop(0)
    drowLineX.pop(-1)
    txt_cutline_X.delete(0, 'end')
    txt_cutline_X.insert(INSERT, str(drowLineX))
    txt_cutline_X.config(state='readonly')

    txt_cutline_Y.config(state='normal')
    drowLineY.pop(0)
    drowLineY.pop(-1)
    txt_cutline_Y.delete(0, 'end')
    txt_cutline_Y.insert(INSERT, str(drowLineY))
    txt_cutline_Y.config(state='readonly')


    for i in drowLines:
        canvas.create_line(scaling(i), fill='lime')
    for j in drowQR:
        canvas.create_rectangle(scaling(j), fill='limeGreen', outline='limeGreen')


def QR_dxf(info, path, name):
    global g_size, g_QRcodeX, g_QRcodeY

    path = os.path.normpath(path)
    draw = dxf.drawing(path+'\\'+name+'.dxf')
    draw.add(dxf.rectangle((0, 0), g_size[0], g_size[1]))

#初始化结束，总循环开始（循环生成二维码）

    for index_x, QR_x in enumerate(g_QRcodeX):
        #cutline_X = float(cutline_X)
        for index_y, QR_y in enumerate(g_QRcodeY):
            #cutline_Y = float(cutline_Y)

            information = info + '%02d' % index_x + '%02d' % index_y


            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_Q,
                box_size=5,
                border=0
            )

            qr.add_data(information)
            qr.make()
            img = qr.make_image()

            qr_array = np.asarray(img)




            row, col = qr_array.shape
            start_pos = []
            end_pos = []

            for j in range(row):
                # 来回画线
                if j % 2 == 1:
                    start = col - 1
                    stop = -1
                    step = -1
                else:
                    start = 0
                    stop = col
                    step = 1

                for i in range(start, stop, step):
                    #判断是否是画线起点
                    if len(start_pos) == 0 and qr_array[j, i] == False:
                        start_pos = [i, j]

                    #判断是否是画线终点
                    if len(start_pos) != 0:
                        if qr_array[j, i] == True:
                            end_pos = [i - step, j]
                        elif i == stop - step:
                            end_pos = [i, j]

                    #如果有终点了就开始画，并重置
                    if len(end_pos) != 0:
                        # print(start_pos, end_pos)
                        draw.add(
                            dxf.line((start_pos[0] * 0.0058 + QR_x, start_pos[1] * 0.0058 + QR_y), (end_pos[0] * 0.0058 + QR_x, end_pos[1] * 0.0058 + QR_y)))
                        start_pos = []
                        end_pos = []
    draw.save()


def qr2dxf():
    code = txt_Article.get()+txt_Wavelength.get()+txt_Type.get()+txt_Number.get()+txt_Supplier.get()
    if len(txt_Article.get()) == 6 \
            and len(txt_Wavelength.get()) == 4 \
            and len(txt_Type.get()) == 4 \
            and len(txt_Number.get()) == 4 \
            and len(txt_Supplier.get()) == 3:
        QR_dxf(code, txt_path.get(), txt_name.get())
        messagebox.showinfo("", "finished")
    else:
        messagebox.showinfo("", "Code Error!")


def changePath(event):

    dir = filedialog.askdirectory()
    txt_path.delete(0, END)
    txt_path.insert(INSERT, dir)


def func_focus(event, entryID):
    if entryID == 1:
        if len(txt_Article.get()) == 6:
            txt_Wavelength.focus_set()
    elif entryID == 2:
        if len(txt_Wavelength.get()) == 4:
            txt_Type.focus_set()
    elif entryID == 3:
        if len(txt_Type.get()) == 4:
            txt_Number.focus_set()
    elif entryID == 4:
        if len(txt_Number.get()) == 4:
            txt_Supplier.focus_set()





window = Tk()
window.title("QR code --> dxf")
window.geometry("680x420")

label_Article = Label(window, width=12, text="Article Nr.")
label_Article.grid(column=1, row=0)
label_Wavelength = Label(window, width=12, text="Wavelength")
label_Wavelength.grid(column=2, row=0)
label_Type = Label(window, width=12, text="Type")
label_Type.grid(column=3, row=0)
label_Number = Label(window, width=12, text="Number")
label_Number.grid(column=4, row=0)
label_Supplier = Label(window, width=12, text="Supplier")
label_Supplier.grid(column=5, row=0)
label_position = Label(window, width=12, text="position")
label_position.grid(column=6, row=0)

label_code = Label(window, text="code", width=12)
label_code.grid(column=0, row=1)
txt_Article = Entry(window, width=12, justify='center')
txt_Article.grid(column=1, row=1, padx=0, sticky='W')
txt_Article.bind('<KeyRelease>', lambda event, entryID=1: func_focus(event, entryID))
txt_Wavelength = Entry(window, width=12, justify='center')
txt_Wavelength.grid(column=2, row=1)
txt_Wavelength.bind('<KeyRelease>', lambda event, entryID=2: func_focus(event, entryID))
txt_Type = Entry(window, width=12, justify='center')
txt_Type.grid(column=3, row=1, padx=8, sticky='W')
txt_Type.bind('<KeyRelease>', lambda event, entryID=3: func_focus(event, entryID))
txt_Number = Entry(window, width=12, justify='center')
txt_Number.grid(column=4, row=1, padx=1, sticky='W')
txt_Number.bind('<KeyRelease>', lambda event, entryID=4: func_focus(event, entryID))
txt_Supplier = Entry(window, width=12, justify='center')
txt_Supplier.grid(column=5, row=1, padx=8, sticky='W')
txt_position = Entry(window, width=10, justify='center')
txt_position.insert(INSERT, 'xxyy')
txt_position.config(state='readonly')
txt_position.grid(column=6, row=1, padx=8, sticky='W')

label_size = Label(window, text="size", width=12)
label_size.grid(column=0, row=2, pady=10, sticky='WS')
txt_size = Entry(window, width=10)
txt_size.config(state='readonly')
txt_size.grid(column=1, row=2, columnspan=2, sticky='W')

label_cutline_X = Label(window, text="cutline_X", width=12)
label_cutline_X.grid(column=0, row=3)
txt_cutline_X = Entry(window, width=28)
txt_cutline_X.config(state='readonly')
txt_cutline_X.grid(column=1, row=3, columnspan=2, sticky='W')

#label_eg = Label(window, borderwidth=0, relief="ridge", bg='lightgray', text="for example:   0,1,2,3")
#label_eg.grid(column=3, row=2, columnspan=2, sticky='W')

label_cutline_Y = Label(window, text="cutline_Y", width=12)
label_cutline_Y.grid(column=0, row=4)
txt_cutline_Y = Entry(window, width=28)
txt_cutline_Y.config(state='readonly')
txt_cutline_Y.grid(column=1, row=4, columnspan=2, pady=10, sticky='W')

canvas = Canvas(window, bg='white', height=350, width=350)
#canvas.grid(column=3, row=2, columnspan=5, rowspan=5, pady=0)
canvas.place(x=298, y=52)


btn_load = Button(window, width=10, text="load", command=showDXF)
btn_load.grid(column=1, row=5, columnspan=2, pady=10)


label_name = Label(window, text="save name", width=12)
label_name.grid(column=0, row=6)
txt_name = Entry(window, width=12)
txt_name.grid(column=1, row=6, columnspan=5, pady=15, sticky='W')
txt_name.insert(INSERT, 'QR'+strftime('%H%M%S', localtime()))

label_path = Label(window, text="save path")
label_path.grid(column=0, row=7)
txt_path = Entry(window, width=28)
txt_path.grid(column=1, row=7, columnspan=2, sticky='W')
txt_path.bind(' <Double-Button-1> ', changePath)
txt_path.insert(INSERT, os.getcwd())



btn_gene = Button(window, width=20, text="generate", command=qr2dxf)
btn_gene.grid(column=0, row=8, columnspan=3, pady=15)

window.mainloop()
