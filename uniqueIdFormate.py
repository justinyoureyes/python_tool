import tkinter as tk
from PIL import Image, ImageTk

# welcome image
window = tk.Tk()
window.title('格式化uniqueId')
canvas = tk.Canvas(window, height=600, width=800,
                   bd=0, highlightthickness=0)  # 创建画布
image_file = Image.open(r'C:\Users\user\Pictures\123.jpg')  # 加载图片文件
img = ImageTk.PhotoImage(image_file)
image = canvas.create_image(0, 0, anchor='nw', image=img)  # 将图片置于画布上

# 设置文本框
t = tk.Text(window, height=10)
t.pack()
# canvas.pack()
canvas.pack(side=tk.TOP)  # 放置画布（为上端）


canvas.create_window(400, 100, width=600, height=200,
                     window=t)


unique_id_text = tk.Text(window, height=15)
unique_id_text.pack()


def format_uniqeuId1():
    unique_id_list = t.get('0.0', 'end')
    chedan = unique_id_list.split('\n')
    b = ''
    for unique_id in chedan:

        a = unique_id
        if a.strip() != '':
            a = "'"+unique_id+"'"
            if b == '':
                b = b+a
            else:
                b = b+','+a
    unique_id_text.delete('0.0', 'end')
    unique_id_text.insert(tk.END, b)


def format_uniqeuId0():
    unique_id_list = t.get('0.0', 'end')
    chedan = unique_id_list.split('\n')
    b = ''
    for unique_id in chedan:

        if unique_id.strip() != '':
            if b == '':
                b = b+unique_id
            else:
                b = b+','+unique_id
    unique_id_text.delete('0.0', 'end')
    unique_id_text.insert(tk.END, b)


def clear_input():
    t.delete('0.0', 'end')


btn_login = tk.Button(window, text='格式化uniqueId', command=format_uniqeuId1)
btn_login.place(x=130, y=230)

btn_format_uniqueid0 = tk.Button(
    window, text='格式化uniqueId不带引号', command=format_uniqeuId0)
btn_format_uniqueid0.place(x=330, y=230)

btn_clean = tk.Button(window, text='清空', command=clear_input)
btn_clean.place(x=570, y=230)


window.mainloop()
