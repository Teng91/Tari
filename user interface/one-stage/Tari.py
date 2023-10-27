############################
# Author: Chiao-Yin Teng   #
# Date: September 28, 2023 #
############################

import tkinter as tk
import os
from PIL import Image, ImageTk, ImageFile
from tkinter import filedialog
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
# 取消最大影像pixel限制
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

def Open_Image():
    global frame1, canvas1
    try:
        global raw_img, w, h, single_img_path
        single_img_path = filedialog.askopenfilename(
            filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('gif', '*.gif')])  # 指定開啟檔案格式
        String_var.set(single_img_path)
        raw_img = Image.open(single_img_path)  # 取得圖片路徑
        img = raw_img.resize((465, 640))
        w, h = img.size  # 取得圖片長寬
        tk_img = ImageTk.PhotoImage(img)  # 轉換成 tk 圖片物件
        canvas1.delete('all')  # 清空 Canvas 原本內容
        canvas1.config(scrollregion=(0, 0, w, h))  # 改變捲動區域
        canvas1.create_image(0, 0, anchor='nw', image=tk_img)  # 建立圖片
        canvas1.tk_img = tk_img  # 修改屬性更新畫面
    except:
        print()

    # 捲動滑鼠滾輪縮放(左側原始影像)
    def do_zoom1(event):
        zoom_n = 10
        factor = 1.001 ** event.delta
        global raw_img, w, h, mx, my

        mx_new = int(mx * factor) / w
        my_new = int(my * factor) / h

        w = int(w * factor)
        h = int(h * factor)

        if w > 465 * zoom_n or h > 640 * zoom_n:
            w = 465 * zoom_n
            h = 640 * zoom_n

        elif w < 465 or h < 640:
            w = 465
            h = 640

        mx_new = mx_new * w
        my_new = my_new * h

        img = raw_img.resize((w, h))
        tk_img = ImageTk.PhotoImage(img)  # 轉換成 tk 圖片物件
        canvas1.delete('all')  # 清空 Canvas 原本內容
        canvas1.config(scrollregion=(0, 0, w, h))  # 改變捲動區域
        if factor > 1:
            canvas1.create_image(mx - mx_new, my - my_new, anchor='nw', image=tk_img)  # 建立圖片
        else:
            canvas1.create_image(mx_new - mx, my_new - my, anchor='nw', image=tk_img)  # 建立圖片
        canvas1.tk_img = tk_img  # 修改屬性更新畫面

    # 滑鼠左鍵移動圖片(左側原始影像)
    def StartMove1(event):
        global first_x, first_y, clickID
        allID = canvas1.find_closest(event.x, event.y)
        if len(allID) > 0:
            clickID = allID[0]
            first_x, first_y = event.x, event.y


    def StopMove1(event):
        global first_x, first_y, clickID
        canvas1.move(clickID, event.x - first_x, event.y - first_y)
        first_x, first_y = event.x, event.y


    def OnMotion1(event):
        global first_x, first_y, clickID
        if clickID != -1:
            canvas1.move(clickID, event.x - first_x, event.y - first_y)
            first_x, first_y = event.x, event.y


    def motion1(event):
        global mx, my
        mx, my = event.x, event.y

    canvas1.bind('<Motion>', motion1)

    clickID = -1
    canvas1.bind("<MouseWheel>", do_zoom1)
    canvas1.bind("<ButtonPress-1>", StartMove1)
    canvas1.bind("<ButtonRelease-1>", StopMove1)
    canvas1.bind("<B1-Motion>", OnMotion1)


# 合併裁切Crop()和辨識Detect()，並顯示結果在畫面右側
def Process():
    # Import Image class from PIL module
    import os
    from PIL import Image
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    Image.MAX_IMAGE_PIXELS = None  # 取消最大像素限制

    input_path = "./1_input"
    dirs = os.listdir(input_path)
    # print(len(dirs))
    count_crop = 0
    for file in range(1, len(dirs) + 1):
        filename = r"./1_input/img" + str(file) + ".jpg"
        img = Image.open(filename)
        size = img.size
        weight = int(size[0] // 4)
        height = int(size[1] // 8)
        Obj_path = './2_crop'
        os.makedirs(Obj_path, exist_ok=True)
        for j in range(8):
            for i in range(4):
                box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
                region = img.crop(box)
                count_crop += 1
                region.save(Obj_path + '/{}.jpg'.format(count_crop))
    print("Complete Segmentation")

    # Yolov7 detect
    script_file = "./yolov7/detect.py"
    os.system(f"python {script_file}")

    # 建立一個8x4的大影像用來合併32張小型影像
    image_width = 3546
    image_height = 2577

    # 設定每行每列的影像數量
    rows = 4
    cols = 8

    # 設定每組影像的數量
    images_per_group = 32

    # 迭代每組影像集合，共1組
    for group_index in range(1, 33, images_per_group):
        # 建立一個4x8的大影像
        big_image = Image.new('RGB', (rows * image_width, cols * image_height))

        # 迭代當前組內的每張小影像
        for i in range(group_index, group_index + images_per_group):
            if i > 33:
                break

            # 讀取影像
            image_path = f"./3_result/{i}.jpg"  # 替換為實際影像的路徑
            img = Image.open(image_path)

            # 計算影像在大影像中的位置
            row = (i - group_index) // rows
            col = (i - group_index) % rows
            x = col * img.width
            y = row * img.height

            # 將影像貼到大影像中
            big_image.paste(img, (x, y))

        # big_image = big_image.rotate(270, PIL.Image.NEAREST, expand=1)
        # 儲存合併後的大影像
        big_image.save(f"./4_merge/merged_image_{group_index // images_per_group + 1}.jpg")
        print('Merge Finish')


        global frame2, canvas2
        try:
            # 注意圖片名稱，後面輸入的影像要更換名字避免覆蓋到前面的影像
            global raw_img2, w, h, path
            path = './4_merge/merged_image_1.jpg'
            # single_img_path = filedialog.askopenfilename(
            #     filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('gif', '*.gif')])  # 指定開啟檔案格式
            String_var.set(path)
            raw_img2 = Image.open(path)  # 取得圖片路徑
            img2 = raw_img2.resize((465, 640))
            w, h = img2.size  # 取得圖片長寬
            tk_img2 = ImageTk.PhotoImage(img2)  # 轉換成 tk 圖片物件
            canvas2.delete('all')  # 清空 Canvas 原本內容
            canvas2.config(scrollregion=(0, 0, w, h))  # 改變捲動區域
            canvas2.create_image(0, 0, anchor='nw', image=tk_img2)  # 建立圖片
            canvas2.tk_img = tk_img2  # 修改屬性更新畫面
        except:
            print()

        # 捲動滑鼠滾輪縮放(右側訓練結果)
        def do_zoom2(event):
            zoom_n = 10
            factor = 1.001 ** event.delta
            global raw_img2, w, h, mx, my

            mx_new = int(mx * factor) / w
            my_new = int(my * factor) / h

            w = int(w * factor)
            h = int(h * factor)

            if w > 465 * zoom_n or h > 640 * zoom_n:
                w = 465 * zoom_n
                h = 640 * zoom_n

            elif w < 465 or h < 640:
                w = 465
                h = 640

            mx_new = mx_new * w
            my_new = my_new * h

            img2 = raw_img2.resize((w, h))
            tk_img2 = ImageTk.PhotoImage(img2)  # 轉換成 tk 圖片物件
            canvas2.delete('all')  # 清空 Canvas 原本內容
            canvas2.config(scrollregion=(0, 0, w, h))  # 改變捲動區域
            if factor > 1:
                canvas2.create_image(mx - mx_new, my - my_new, anchor='nw', image=tk_img2)  # 建立圖片
            else:
                canvas2.create_image(mx_new - mx, my_new - my, anchor='nw', image=tk_img2)  # 建立圖片
            canvas2.tk_img2 = tk_img2  # 修改屬性更新畫面
 
        # 滑鼠左鍵移動圖片(右側訓練結果)
        def StartMove2(event):
            global first_x, first_y, clickID
            allID = canvas2.find_closest(event.x, event.y)
            if len(allID) > 0:
                clickID = allID[0]
                first_x, first_y = event.x, event.y


        def StopMove2(event):
            global first_x, first_y, clickID
            canvas2.move(clickID, event.x - first_x, event.y - first_y)
            first_x, first_y = event.x, event.y


        def OnMotion2(event):
            global first_x, first_y, clickID
            if clickID != -1:
                canvas2.move(clickID, event.x - first_x, event.y - first_y)
                first_x, first_y = event.x, event.y


        def motion2(event):
            global mx, my
            mx, my = event.x, event.y

        canvas2.bind('<Motion>', motion2)

        clickID = -1
        canvas2.bind("<MouseWheel>", do_zoom2)
        canvas2.bind("<ButtonPress-1>", StartMove2)
        canvas2.bind("<ButtonRelease-1>", StopMove2)
        canvas2.bind("<B1-Motion>", OnMotion2)


def Quit():
    # global window
    window.quit()


### GUI ###
window = tk.Tk()
window.title('高解析度害蟲辨識系統')
window.geometry('1080x720')

screen_Width = 1280
screen_height = 720
width = screen_Width//2
height = screen_height//2
root_win_par = '%dx%d+%d+%d' % (width, height, (screen_Width-width)/2, (screen_height-height)/2)
String_var = tk.StringVar()
String_var.set('尚未選擇文件')

frame1 = tk.Frame(window, width=465, height=640, relief='groove', borderwidth=2)  # 放 Canvas 的 Frame
frame1.grid(row=0, column=0, padx=20, pady=40)
canvas1 = tk.Canvas(frame1, width=465, height=640, bg='white')  # Canvas

scrollX = tk.Scrollbar(frame1, orient='horizontal')  # 水平捲軸
scrollX.pack(side='bottom', fill='x')
scrollX.config(command=canvas1.xview)

scrollY = tk.Scrollbar(frame1, orient='vertical')  # 垂直捲軸
scrollY.pack(side='right', fill='y')
scrollY.config(command=canvas1.yview)

canvas1.config(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)  # Canvas 綁定捲軸
canvas1.pack(side='left')

frame2 = tk.Frame(window, width=465, height=640, relief='groove', borderwidth=2)  # 放 Canvas 的 Frame
frame2.grid(row=0, column=1, padx=20, pady=40)
canvas2 = tk.Canvas(frame2, width=465, height=640, bg='white')  # Canvas

scrollX = tk.Scrollbar(frame2, orient='horizontal')  # 水平捲軸
scrollX.pack(side='bottom', fill='x')
scrollX.config(command=canvas2.xview)

scrollY = tk.Scrollbar(frame2, orient='vertical')  # 垂直捲軸
scrollY.pack(side='right', fill='y')
scrollY.config(command=canvas2.yview)

canvas2.config(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)  # Canvas 綁定捲軸
canvas2.pack(side='left')


# 设置窗口是否可变长、宽，True：可变，False：不可变
window.resizable(width=False, height=False)

# 显示路径输入框初始化及放置(禁止写入)
Img_Path_Text = tk.Entry(window, textvariable=String_var, borderwidth=1, state=tk.DISABLED)
Img_Path_Text.place(x=10, y=10, width=width-20-40, height=20)

# 路径选取按钮初始化设置
Img_Path_Button = tk.Button(window, text='選擇', command=Open_Image)
Img_Path_Button.place(x=width-45, y=10, width=40, height=20)

# Merge
button_Merge = tk.Button(window, text="執行", command=Process)
button_Merge.place(x=800, y=10, width=40, height=20)

# Close Window
button_Close = tk.Button(window, text="離開", command=Quit)  # button to close the window
button_Close.place(x=1000, y=10, width=40, height=20)

window.mainloop()
