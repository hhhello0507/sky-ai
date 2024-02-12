from PIL import Image
import os
from pillow_heif import register_heif_opener
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

def browse_folder1():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry1.delete(0, tk.END)
        folder_path_entry1.insert(0, folder_path)

def submit():
    output_name = 'normal' if toggle_var.get() else 'abnormal'

    register_heif_opener()
    lib_name = 'image_resizer'

    join = os.path.join

    # input_path = join(os.getcwd(), lib_name, 'input_image')
    # output_path = join(os.getcwd(), lib_name, 'output_image')

    input_path = folder_path_entry.get()
    output_path = folder_path_entry1.get()

    images_path = os.listdir(input_path)


    for (idx, image_path) in enumerate(images_path):
        # print(image_path)
        image = Image.open(join(input_path, image_path))
        resized_image = image.resize((640, 480))
        resized_image.save(join(output_path, f'{output_name}_{idx}.jpg'))

def update_label(*args):
    toggle_button.config(text='정상' if toggle_var.get() else '불량')


root = tk.Tk()
root.title("image resizer")
screen_width = 480
screen_height = 240
root.geometry(f'{screen_width}x{screen_height}')
# 스타일 설정
style = ttk.Style()
# style.configure('TButton', font=('calibri', 10, 'bold'), foreground='black') # 버튼 스타일 지정
style.configure('TLabel', font=('calibri', 12))

# 프레임 생성
frame = ttk.Frame(root)
frame.pack(padx=20, pady=20)

# 라벨 생성
toggle_var = tk.BooleanVar()
toggle_var.trace_add('write', update_label)

toggle_button = ttk.Checkbutton(frame, text='정상' if toggle_var.get() else '불량', variable=toggle_var, style='Custom.TButton')
toggle_button.grid(row=0, column=0, padx=5, pady=5)

# 입력 창 생성
folder_path_entry = tk.Entry(frame, width=30)
folder_path_entry.grid(row=1, column=0, padx=0)

# 폴더 선택 버튼 생성
browse_button = tk.Button(frame, text="찾아보기", command=browse_folder)
browse_button.grid(row=1, column=1, padx=5)

folder_path_entry1 = tk.Entry(frame, width=30)
folder_path_entry1.grid(row=2, column=0, padx=0)

# 폴더 선택 버튼 생성
browse_button = tk.Button(frame, text="찾아보기", command=browse_folder1)
browse_button.grid(row=2, column=1, padx=5)

# 제출 버튼 생성
submit_button = ttk.Button(frame, text="이미지 변환", command=submit)
submit_button.grid(row=3, column=0, padx=5, columnspan=2, pady=5)

# Tkinter 윈도우 실행
root.mainloop()