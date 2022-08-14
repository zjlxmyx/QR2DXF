import time
import os
import qrcode
import numpy as np
from dxfwrite import DXFEngine as dxf

from tkinter import Label, Entry, Button, Tk, END, INSERT
from tkinter import messagebox
from tkinter import filedialog


def QR_dxf(info, path, name):

    path = os.path.normpath(path)
    draw = dxf.drawing(path+'\\'+name+'.dxf')
    draw.add(dxf.line((0, 0), (60, 0)))
    draw.add(dxf.line((60, 0), (60, 60)))
    draw.add(dxf.line((60, 60), (0, 60)))
    draw.add(dxf.line((0, 60), (0, 0)))



    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=5,
        border=0
    )

    qr.add_data(info)
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
                    dxf.line((start_pos[0] * 0.0058, start_pos[1] * 0.0058), (end_pos[0] * 0.0058, end_pos[1] * 0.0058)))
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
#        QR_dxf(txt_info.get(), txt_path.get(), txt_name.get())
        messagebox.showinfo("", "finished")
    else:
        messagebox.showinfo("", "Code Error!")

def changePath(event):

    dir = filedialog.askdirectory()
    txt_path.delete(0, END)
    txt_path.insert(INSERT, dir)




window = Tk()
window.title("QR code --> dxf")
window.geometry("550x150")

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
txt_Article.grid(column=1, row=1, padx=0)
txt_Wavelength = Entry(window, width=12)
txt_Wavelength.grid(column=2, row=1)
txt_Type = Entry(window, width=12)
txt_Type.grid(column=3, row=1)
txt_Number = Entry(window, width=12)
txt_Number.grid(column=4, row=1)
txt_Supplier = Entry(window, width=12)
txt_Supplier.grid(column=5, row=1)



label_name = Label(window, text="save name", width=12)
label_name.grid(column=0, row=2)
txt_name = Entry(window, width=72)
txt_name.grid(column=1, row=2, columnspan=5, pady=10)
txt_name.insert(INSERT, 'QR'+time.strftime('%H%M%S', time.localtime()))

label_path = Label(window, text="save path")
label_path.grid(column=0, row=3)
txt_path = Entry(window, width=72)
txt_path.grid(column=1, row=3, columnspan=5)
txt_path.bind(' <Double-Button-1> ', changePath)
txt_path.insert(INSERT, os.getcwd())



btn_gene = Button(window, width=20, text="generate", command=qr2dxf)
btn_gene.grid(column=2, row=4, columnspan=2, pady=10)

window.mainloop()
