import os
from time import strftime, localtime
import qrcode
import numpy as np
from dxfwrite import DXFEngine as dxf

from tkinter import Label, Entry, Button, Tk, END, INSERT
from tkinter import messagebox
from tkinter import filedialog


def QR_dxf(info, path, name):
    Offset_X = txt_offset_X.get().split(',')

    Offset_Y = txt_offset_Y.get().split(',')




    path = os.path.normpath(path)
    draw = dxf.drawing(path+'\\'+name+'.dxf')
    draw.add(dxf.line((0, 0), (66, 0)))
    draw.add(dxf.line((66, 0), (66, 66)))
    draw.add(dxf.line((66, 66), (0, 66)))
    draw.add(dxf.line((0, 66), (0, 0)))

#初始化结束，总循环开始（循环生成二维码）

    for index_x, offset_x in enumerate(Offset_X):
        offset_x = float(offset_x)
        for index_y, offset_y in enumerate(Offset_Y):
            offset_y = float(offset_y)

            information = info + '0' + str(index_x) + str(index_y)


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
                            dxf.line((start_pos[0] * 0.0058 + offset_x, start_pos[1] * 0.0058 + offset_y), (end_pos[0] * 0.0058 + offset_x, end_pos[1] * 0.0058 + offset_y)))
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




window = Tk()
window.title("QR code --> dxf")
window.geometry("550x210")

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

label_code = Label(window, text="code", width=12)
label_code.grid(column=0, row=1)
txt_Article = Entry(window, width=12)
txt_Article.grid(column=1, row=1, padx=0, sticky='W')
txt_Wavelength = Entry(window, width=12)
txt_Wavelength.grid(column=2, row=1)
txt_Type = Entry(window, width=12)
txt_Type.grid(column=3, row=1)
txt_Number = Entry(window, width=12)
txt_Number.grid(column=4, row=1)
txt_Supplier = Entry(window, width=12)
txt_Supplier.grid(column=5, row=1)

label_offset_X = Label(window, text="offset_X", width=12)
label_offset_X.grid(column=0, row=2)
txt_offset_X = Entry(window, width=28)
txt_offset_X.grid(column=1, row=2, columnspan=5, pady=10, sticky='W')
label_eg = Label(window, text="for example:   0,1,2,3")
label_eg.grid(column=3, row=2, columnspan=2, sticky='W')


label_offset_Y = Label(window, text="offset_Y", width=12)
label_offset_Y.grid(column=0, row=3)
txt_offset_Y = Entry(window, width=28)
txt_offset_Y.grid(column=1, row=3, columnspan=5, sticky='W')


label_name = Label(window, text="save name", width=12)
label_name.grid(column=0, row=4)
txt_name = Entry(window, width=12)
txt_name.grid(column=1, row=4, columnspan=5, pady=10, sticky='W')
txt_name.insert(INSERT, 'QR'+strftime('%H%M%S', localtime()))

label_path = Label(window, text="save path")
label_path.grid(column=0, row=5)
txt_path = Entry(window, width=72)
txt_path.grid(column=1, row=5, columnspan=5, sticky='W')
txt_path.bind(' <Double-Button-1> ', changePath)
txt_path.insert(INSERT, os.getcwd())



btn_gene = Button(window, width=20, text="generate", command=qr2dxf)
btn_gene.grid(column=2, row=6, columnspan=2, pady=10)

window.mainloop()
