import duplicateCheck
import tkinter as tk
from tkinter import filedialog as flg
from tkinter import ttk, messagebox
import xlwt

from parameter import Parameter


def selectPath():
    path_ = flg.askdirectory()
    filepath.set(path_)


def startProcess():
    path = original_path_entry.get()  # 得到原始地址
    if path == "":
        result_text.insert('end', '请先选择查重的文件夹')
    else:
        global result
        result_text.delete('1.0', 'end')
        result = duplicateCheck.duplicateCheck(path, para)
        length = len(result)

        for i in range(length):
            result_text.insert('end', str(result[i]) + '\n')
        print(result)


def updateSetting(mode, s_row, s_cell):
    isText = False
    if mode == "扫描文本":
        isText = True
    para.setParameter(isText, s_row, s_cell)


def outputToExcel():
    path_ = flg.askdirectory()
    if path_ != "":
        xls = xlwt.Workbook()
        sht1 = xls.add_sheet('Sheet1')
        global result
        length = len(result)
        for i in range(length):
            for j in range(length):
                sht1.write(i, j, str(result[i][j]))
        xls.save(path_ + '/mydata.xls')
        messagebox.showinfo('提示', '导出成功')


def openSettingWindows():

    setting = tk.Toplevel(root)  # 创建设置窗口

    para_list = para.getParameter()

    # 默认值
    s_row = tk.StringVar(value=para_list[1])
    s_cell = tk.StringVar(value=para_list[2])

    choose_mode = ttk.Combobox(setting, width=10)
    choose_mode.grid(row=0, column=0)
    choose_mode['value'] = ('扫描文本', '扫描表格')
    if para_list[1]:
        choose_mode.current(0)
    else:
        choose_mode.current(1)

    range_frame = tk.Frame(setting)
    range_frame.grid(row=1, column=0)

    text0 = tk.Label(range_frame, text="表格扫描范围")
    text0.grid(row=1, column=0)

    text1 = tk.Label(range_frame, text="第")
    text1.grid(row=2, column=0)

    entry_sx = tk.Entry(range_frame, width=3, textvariable=s_row)
    entry_sx.grid(row=2, column=1)

    text2 = tk.Label(range_frame, text="行的第")
    text2.grid(row=2, column=2)

    entry_sy = tk.Entry(range_frame, width=3, textvariable=s_cell)
    entry_sy.grid(row=2, column=3)

    text3 = tk.Label(range_frame, text="列")
    text3.grid(row=2, column=4)

    confirm_button = tk.Button(range_frame, text="确认",
                               command=lambda: updateSetting(choose_mode.get(), entry_sx.get(), entry_sy.get()))
    confirm_button.grid(row=3, column=0)


if __name__ == "__main__":
    para = Parameter()  # 用于传递参数的对象
    para.setParameter(False, 7, 0)
    root = tk.Tk()

    filepath = tk.StringVar()
    root.resizable = (0, 0)  # 设定不可调节窗口大小
    root.geometry('480x280')  # 设置窗口大小

    text_label_1 = tk.Label(root, text="导入资源库：")
    text_label_1.place(relx=0.1, rely=0.05)

    original_path_entry = tk.Entry(root, width=30, textvariable=filepath)
    original_path_entry.place(relx=0.3, rely=0.05)

    select_button = tk.Button(root, text="选择", width=6, command=selectPath)
    select_button.place(relx=0.75, rely=0.035)

    result_text = tk.Text(root, width=53, height=13)
    result_text.place(relx=0.1, rely=0.15)

    start_button = tk.Button(root, text="查重", width=6, command=startProcess)
    start_button.place(relx=0.75, rely=0.78)

    help_button = tk.Button(root, text="设置", width=6, command=openSettingWindows)
    help_button.place(relx=0.1, rely=0.78)

    output_button = tk.Button(root, text="导出到表格", command=outputToExcel)
    output_button.place(relx=0.23, rely=0.78)

    root.mainloop()
