#$LAN=PYTHON$
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox as tkb
import math
import sys
import copy

class Canv:
    def __init__(self, window):
        sys.setrecursionlimit(1000000)
        window.title("M073040090")
        global cv, x_val, y_val, out_str, E1, E2, in_file, d_index, divide_l, divide_r
        x_val = []  # 讀入數據x軸坐標
        y_val = []  # 讀入數據y軸坐標
        out_str = ""  # 保存輸出數據
        in_file = []  # 存放讀入數據
        d_index = 0  # 儲存divide-and-conquer層數
        divide_l = {}  # 存儲左側數據
        divide_r = {}  # 存儲右側數據
        global xs_in, ys_in, line, start_x, start_y, end_x, end_y, con_line, RG
        xs_in = []  # x_s對應的index集：x_s[xs_in[i]]即為i點x軸坐標
        ys_in = []  # y_s對應的index集
        line = []  # 已繪製的直線集合，二維數組
        con_line = [] # 繪製的convex hull的直線集合，二維數組
        start_x = {}  # line對應的起點坐標
        start_y = {}  # line對應的起點坐標
        end_x = {}  # line對應的終點坐標
        end_y = {}  # line對應的終點坐標
        RG = 1 # 用來為左右側畫出不同顏色voronoi diagram
        # 打開畫布
        cv = tk.Canvas(window, bg='white', width=600, height=600)
        cv.pack()
        # 點擊輸入
        cv.focus_set()
        cv.bind("<Button-1>", self.MounseEvent)
        # Run按鈕
        R = tk.Button(window, text="Divide", command=self.Run)
        R.pack()
        # Clear按鈕
        Cl = tk.Button(window,text='清空畫布',command=self.Clear)
        Cl.pack()
        # read按鈕
        # count_read = 0
        C4 = tk.Button(window, text='執行一行讀入檔案', command=self.read)
        C4.pack()
        # step by step 操作
        C5 = tk.Button(window, text='step by step', command=self.step)
        C5.pack()
        # 讀入檔案
        C2 = tk.Button(window, text='讀入檔案', command=self.read_file)
        C2.pack(side="right")
        E1 = tk.Entry(window, bd=5)
        E1.pack(side="right")
        L1 = tk.Label(window, text="輸入檔案：")
        L1.pack(side="right")

        # 輸出文字檔
        L2 = tk.Label(window, text="輸出檔案：")
        L2.pack(side="left")
        E2 = tk.Entry(window, bd=5)
        E2.pack(side="left")
        C3 = tk.Button(window, text='輸出文字檔', command=self.out_file)
        C3.pack(side="left")

    # ===================實現點擊后顯示該點===============================================
    def MounseEvent(self,event):
        # print(event.x, event.y)
        x1, y1 = (event.x - 0), (event.y - 0)
        x2, y2 = (event.x - 5), (event.y - 5)
        cv.create_oval(x1,y1,x2,y2,fill="red")
        x_val.append(event.x)
        y_val.append(event.y)
    # ===================實現點擊后顯示該點===============================================

    # ========================================清空畫布====================================
    def Clear(self):
        cv.delete(tk.ALL)
        del x_val[0:]
        del y_val[0:]
        tk.messagebox.showinfo(title='Hello', message='畫布已清空！')
    # ========================================清空畫布====================================

    # ================================序列排序 冒泡排序==================================
    def Sort(self,xa,ya):
        for i2 in range(0,len(xa)):
            maxi = 0
            max_p = -1
            count = len(xa) - i2
            for j in range(0,count):
                if xa[j] > maxi:
                    maxi = xa[j]
                    max_p = j
            cache = xa[len(xa) - i2 - 1]
            xa[len(xa) - i2 - 1] = xa[max_p]
            xa[max_p] = cache
            cache = ya[len(ya) - i2 - 1]
            ya[len(ya) - i2 - 1] = ya[max_p]
            ya[max_p] = cache
        for i3 in range(0, len(xa)-1):
            if xa[i3] == xa[i3+1]:
                count_eq = 1
                un_eq = 0
                while un_eq == 0:
                    if i3 == len(xa)-1:
                        count_eq = 2
                        break
                    elif i3 == len(xa)-count_eq:
                        un_eq = 1
                    elif xa[i3] == xa[i3+count_eq]:
                        count_eq += 1
                    else:
                        un_eq = 1
                for i4 in range(0,count_eq):
                    maxi = 0
                    max_p = -1
                    count2 = count_eq - i4
                    for i5 in range(0, count2):
                        if ya[i3+i5] > maxi:
                            maxi = ya[i3+i5]
                            max_p = i3+i5
                    cache = ya[i3 + count_eq - i4 - 1]
                    ya[i3 + count_eq - i4 - 1] = ya[max_p]
                    ya[max_p] = cache
        print("xa,ya: ",xa,ya)
        return xa,ya
    # ================================序列排序 冒泡排序===========================

    # ================================輸出文字檔 append===========================
    def out_file(self):
        # file_out = open("out.txt", "w+")
        path2 = E2.get()
        if path2 =="":
            print("路徑為空，請重新輸入路徑")
        file_out = open(path2, "a")
        file_out.write(out_str)
        file_out.close()
        tk.messagebox.showinfo(title='Hello', message='文字檔已輸出至：'+path2)
    # ================================輸出文字檔==================================
    # =================================divide======================================
    def divide(self, point):
        # file_out = open("out.txt", "w+")
        global d_index, divide_l, divide_r
        if len(point) == 2:
            divide_l[d_index] = point[0:1]
            divide_r[d_index] = point[1:]
            d_index += 1
        elif len(point) == 3:
            divide_l[d_index] = point[0:2]
            divide_r[d_index] = point[2:]
            d_index += 1
            self.divide(point[0:2])
        elif len(point) == 1:
            tk.messagebox.showinfo(title='Hello', message='點集只有單點，本次結束')
            return -1
        else:
            chang = len(point)
            half_len = int(chang / 2)
            divide_l[d_index] = point[0:half_len]
            divide_r[d_index] = point[half_len:]
            d_index += 1
            self.divide(point[0:half_len])
            self.divide(point[half_len:])
        return d_index
    # ===================================divide======================================

    # ================================Run按鈕======================================
    def Run(self):
        global x_s, y_s, d_index, divide_l, divide_r, d_1th
        d_index = 0
        divide_l = {}
        divide_r = {}
        d_1th = 1
        global xs_in, ys_in,line, start_x, start_y, end_x, end_y, con_line
        xs_in = []  # x_s對應的index集：x_s[xs_in[i]]即為i點x軸坐標
        ys_in = []  # y_s對應的index集
        line = []  # 已繪製的直線集合，二維數組
        con_line = []
        start_x = {}  # line對應的起點坐標
        start_y = {}  # line對應的起點坐標
        end_x = {}  # line對應的終點坐標
        end_y = {}  # line對應的終點坐標
        # ========sort x and y==========
        if len(x_val) == 0:
            print("點集為空，請在畫布點擊或讀入文檔")
            return 0
        x_s, y_s = self.Sort(x_val, y_val)
        # check and store the index /initialize the line
        for i in range(0, len(x_s)):
            print(x_s[i],y_s[i])
            xs_in.append(i)
            ys_in.append(i)
            line += [[]]
            con_line += [[]]
            for j in range(0, len(x_s)):
                line[i].append(-1)
                con_line[i].append(-1)
        # =====divide操作===============
        single = self.divide(xs_in)
        if single == -1:
            return 0
        else:
            tk.messagebox.showinfo(title='Hello', message='已存儲點集，請點擊step逐步執行！' )
            return 1
        # ================================Run按鈕====================================

    # ================================step by step=======================================
    def step(self):
        global x_s, y_s, line, start_x, start_y, end_x, end_y, divide_l, divide_r, d_index, d_1th, con_line
        # ==========恢復上一次標識點的顏色========
        if d_1th == 0:
            for i in divide_l[d_index]:
                x1, y1 = (x_s[i] - 0), (y_s[i] - 0)
                x2, y2 = (x_s[i] - 5), (y_s[i] - 5)
                cv.create_oval(x1, y1, x2, y2, fill="red")
            for i in divide_r[d_index]:
                x1, y1 = (x_s[i] - 0), (y_s[i] - 0)
                x2, y2 = (x_s[i] - 5), (y_s[i] - 5)
                cv.create_oval(x1, y1, x2, y2, fill="red")
        # ============執行voronoi算法============
        # 標識本次合併兩側點集
        # 紅色為未處理點；綠色為左側點；黃色為右側點
        d_index -= 1
        for i in divide_l[d_index]:
            x1, y1 = (x_s[i] - 0), (y_s[i] - 0)
            x2, y2 = (x_s[i] - 5), (y_s[i] - 5)
            cv.create_oval(x1, y1, x2, y2, fill="green")
        for i in divide_r[d_index]:
            x1, y1 = (x_s[i] - 0), (y_s[i] - 0)
            x2, y2 = (x_s[i] - 5), (y_s[i] - 5)
            cv.create_oval(x1, y1, x2, y2, fill="yellow")
        # 進行merge操作
        self.Voronoi(divide_l[d_index], divide_r[d_index])
        d_sum = copy.deepcopy(divide_l[d_index])
        d_sum += divide_r[d_index]
        # 繪出convex hull
        self.convex(d_sum)
        if d_1th == 1:
            d_1th = 0

        # ======保存結果至out_str========
        if d_index <= 0:
            global out_str
            out_str = ""
            for j in range(0, len(xs_in)):
                out_str += "P " + str(x_s[xs_in[j]]) + " " + str(y_s[ys_in[j]]) + "\n"
            out_line = []
            for l1 in line:
                for l2 in l1:
                    if l2 != -1:
                        if l2 in out_line:
                            continue
                        out_str += "E "
                        out_str += str(start_x[l2]) + " "
                        out_str += str(start_y[l2]) + " " + str(end_x[l2]) + " " + str(end_x[l2]) + "\n"
                        out_line.append(l2)
            tk.messagebox.showinfo(title='Hello', message='本次合併已結束，可點擊輸出檔案')
    # ================================step by step=======================================

    # ========================================讀入檔案=================================
    def read_file(self):
        path = E1.get()
        print(path)
        if path == "":
            print("路徑為空，請重新輸入路徑")
        file = open(path, "r+", errors='ignore')
        global in_file, h_r
        in_file = []
        h_r = 0
        stop = 0
        # 讀入數據，跳過注釋和空行，直到讀到0后停止
        while stop == 0:
            in_str = file.readline()
            if in_str[0] == '#' or in_str == "\n":
                continue
            elif in_str[0] == '0':
                in_file.append(in_str)
                stop = 1
                break
            else:
                in_file.append(in_str)
        file.close()
        tk.messagebox.showinfo(title='Hello', message="已成功讀入檔案："+path)
        return in_file
    # ========================================讀入檔案=================================

    # =====================點擊后讀入檔案下一行并執行和保存結果=========================
    def read(self):
        # ===========讀入首字符===============
        global in_file, h_r
        star = 0
        in_count = 0
        while star == 0:
            # print("in_file[h_r]: ", in_file[h_r])
            in_str = in_file[h_r]
            # print(in_str)
            h_r += 1  # 記錄已讀到哪一行
            if in_str[0] == '#' or in_str == "\n":
                continue
            else:
                in_count = int(in_str)
                star = 1
        # print("in_count:", in_count)
        # in_count 宣告將有幾行數據
        del x_val[0:]
        del y_val[0:]
        cv.delete(tk.ALL)
        data = []
        if in_count == 0:
            tk.messagebox.showinfo(title='Hello', message='讀入點數為零，檔案測試停止')
        else:
            # ===========參照in_count讀入數據===============
            for i in range(0, in_count):
                star2 = 0
                while star2 == 0:
                    in_str = in_file[h_r]
                    h_r += 1
                    if in_str[0] == '#' or in_str == "\n":
                        continue
                    else:
                        data = in_str.split(" ")
                        # print(data)
                        star2 = 1
                # print("data:", data)
                # ==========繪製讀入點==============
                x1, y1 = (int(data[0]) - 0), (int(data[1]) - 0)
                x2, y2 = (int(data[0]) - 5), (int(data[1]) - 5)
                cv.create_oval(x1, y1, x2, y2, fill="red")
                # 加入x_val, y_val
                x_val.append(int(data[0]))
                y_val.append(int(data[1]))
            # ==========清除相等的點============
            de = 0
            while de == 0:
                de2 = 1
                for c1 in range(0, len(x_val)):
                    if de2 == 0:
                        break
                    if c1 == (len(x_val)-1):
                        de = 1
                        break
                    for c2 in range(0, len(x_val)):
                        if c1 != c2:
                            if x_val[c1] == x_val[c2] and y_val[c1] == y_val[c2]:
                                del x_val[c2]
                                del y_val[c2]
                                de2 = 0
                                break
            # =========== 開始繪圖=============
            global d_index, divide_l, divide_r, d_1th, xs_in, ys_in
            d_index = 0
            divide_l = {}
            divide_r = {}
            d_1th = 1
            global x_s, y_s, line, start_x, start_y, end_x, end_y, con_line
            xs_in = []  # x_s對應的index集：x_s[xs_in[i]]即為i點x軸坐標
            ys_in = []  # y_s對應的index集
            line = []  # 已繪製的直線集合
            con_line = []
            start_x = {}  # line對應的起點坐標
            start_y = {}  # line對應的起點坐標
            end_x = {}  # line對應的終點坐標
            end_y = {}  # line對應的終點坐標
            # sort x and y
            x_s, y_s = self.Sort(x_val, y_val)
            # check and store the index /initialize the line
            print("讀入資料為：")
            for i in range(0, len(x_s)):
                print(x_s[i], y_s[i])
                xs_in.append(i)
                ys_in.append(i)
                line += [[]]
                for j in range(0, len(x_s)):
                    line[i].append(-1)
                con_line += [[]]
                for j in range(0, len(x_s)):
                    line[i].append(-1)
                    con_line[i].append(-1)
            # 進行divide操作
            single = self.divide(xs_in)
            if single == -1:
                return 0
            else:
                tk.messagebox.showinfo(title='Hello', message='已存儲點集，請點擊step逐步執行！')
                return 1
    # =====================點擊后讀入檔案下一行并執行和保存結果=========================

    # ========================================泰森多邊形算法===========================
    def Voronoi(self, sl_in, sr_in):
        # 備份一份line
        # line_d = []
        global line,RG, color
        line_d = []
        for i1 in range(0, len(x_s)):
            line_d += [[]]
            for j1 in range(0, len(x_s)):
                line_d[i1].append(-1)
        for l1 in sl_in:
            for l2 in sl_in:
                if l1 == l2:
                    continue
                if line[l1][l2] != -1:
                    line_d[l1][l2] = line[l1][l2]
                    line_d[l2][l1] = line_d[l1][l2]
        for l3 in sr_in:
            for l4 in sr_in:
                if l3 == l4:
                    continue
                if line[l3][l4] != -1:
                    line_d[l3][l4] = line[l3][l4]
                    line_d[l4][l3] = line_d[l3][l4]
        # print("line:", line)
        # print("line_d:", line_d)
        # line_d = copy.deepcopy(line)
        # 處理上次繪出的所有直線
        if RG == 1:
            RG = 0
            color = "red"
        else:
            RG = 1
            color = "green"
        print("點集為:", sl_in, sr_in)
        # =============merge the two 泰森多邊形==========
        # print("===========4====================")
        # 選擇起始點
        l_in = -1  # 左側起始點:l_in
        r_in = -1  # 右側起始點:r_in
        # cut判斷左右兩點是否為切點
        cut = 1
        for k1 in range(0, len(sl_in)):
            for k2 in range(0, len(sr_in)):
                cut = 1
                x_1 = x_s[sl_in[k1]]  # 通過index取出坐標
                y_1 = y_s[sl_in[k1]]
                x_2 = x_s[sr_in[k2]]
                y_2 = y_s[sr_in[k2]]
                # 計算斜率k0
                if x_1 == x_2:
                    k0 = 10000
                elif y_1 == y_2:
                    k0 = 0.0001
                else:
                    k0 = (y_1 - y_2) / (x_1 - x_2)
                b0 = y_1 - k0 * x_1
                # 判斷左側是否有點在連線上方
                for k3 in range(0, len(sl_in)):
                    if k3 == k1:
                        continue
                    xk = x_s[sl_in[k3]]
                    yk = y_s[sl_in[k3]]
                    if yk < (k0 * xk + b0):
                        cut = 0
                        break
                if cut == 0:
                    continue
                # 判斷右側是否有點在連線上方
                for k4 in range(0, len(sr_in)):
                    if k4 == k2:
                        continue
                    xk = x_s[sr_in[k4]]
                    yk = y_s[sr_in[k4]]
                    if yk < (k0 * xk + b0):
                        cut = 0
                        break
                # 兩側都沒有點在連線上方
                if cut == 1:
                    l_in = k1
                    r_in = k2
                    break
            if cut == 1:
                break
        # 未找到切線
        if cut == 0:
            print("=================沒有切點=============")
            return 0

        # =======迭代準備 選定的起始點為：li, ri=================
        li = sl_in[l_in]  # 取出index
        ri = sr_in[r_in]
        end = 0  # end用來表示一次divide-and-conquer是否結束
        next_s = 0   # next_s被用來記錄下一次合併的起點
        next_x = 0
        first = 1
        left_s = 1  # 相交點在左/在右
        last_li = -1  # 上一次相交的直線
        c_x = 0 # 用來搜索相交直線
        c_y = 0
        # ===================開始迭代======================
        while end == 0:
            # line_d = []
            # line_d = copy.deepcopy(line)
            # print("迭代開始")
            # 點的坐標
            x1 = x_s[li]  # 通過index取出坐標
            y1 = y_s[li]
            x2 = x_s[ri]
            y2 = y_s[ri]
            # ========計算中垂線斜率；垂直或平行處理==========
            if x1 == x2:
                k = 0.0001
            elif y1 == y2:
                k = 10000
            else:
                k = -1 / ((y1 - y2) / (x1 - x2))
            # 獲得k和b
            mix = (x1 + x2) / 2  # mix,miy 為中點
            miy = (y1 + y2) / 2
            b = miy - k * mix
            # ========生成直線==============
            if first == 1:  # 初次時設置y為0，自上向下延伸
                sty = next_s
                stx = int((sty - b) / k)
                eny = 600
                enx = int((eny - b) / k)
                c_x = mix
                c_y = miy
                first = 0
            else:
                sty = next_s  # 首先設置y軸起點
                stx = next_x
                c_x = stx
                c_y = sty
                if x1 == x2:
                    if left_s == 1:  # 相交點在左在右
                        eny = sty
                        enx = 1000
                    else:
                        eny = sty
                        enx = 0
                else:
                    eny = 600
                    enx = int((eny - b) / k)
            # print("k and b: ", k, b)
            # lin_p = cv.create_line(stx, sty, enx, eny, fill='blue')  # black為未處理線

            # 判斷是否繼續并找到最近交線（交點到中點距離最短）
            min_d = 100000  # 最短距離
            left_s = 1  # 相交點在左在右
            xj = 0  # 是否相交
            min_px = -1  # 交點x值
            min_py = -1  # 交點y值
            min_line = -1  # 最近交線為哪一條
            min_li = -1  # 左側最近交線為哪一點
            min_ri = -1  # 右側最近交線為哪一點
            loc_re = 1  # 記錄位置關係，位置關係不同剪枝方式不同；1：s修改tart; 2:修改end

            # 檢查左側, 根據起點和終點與直線的位置關係判斷是否相交
            count_l = 0
            for lin3 in line[li]:
                if lin3 == -1 or lin3 == last_li or count_l in sr_in:  # 點與點不存在直線
                    count_l += 1
                    continue
                x3 = x_s[count_l]
                y3 = y_s[count_l]
                # 起點在線上
                if abs(start_y[lin3] - (k * start_x[lin3] + b)) < 0.01:
                    xj = 1
                    px = start_x[lin3]
                    py = start_y[lin3]
                    dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                    if dis < min_d:
                        min_line = lin3
                        min_px = px
                        min_py = py
                        min_d = dis
                        min_li = count_l
                        loc_re = 1
                        # print("=====l1==============")
                    count_l += 1
                    continue
                # 點在線上方
                elif start_y[lin3] > (k * start_x[lin3] + b):
                    # 終點在線上
                    if abs(end_y[lin3] - (k * end_x[lin3] + b)) < 0.01:
                        xj = 1
                        px = end_x[lin3]
                        py = end_y[lin3]
                        dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                        if dis < min_d:
                            min_line = lin3
                            min_px = px
                            min_py = py
                            min_d = dis
                            min_li = count_l
                            loc_re = 1
                            # print("=====l2==============")
                        count_l += 1
                        continue
                    # 不相交
                    elif end_y[lin3] > (k * end_x[lin3] + b):
                        count_l += 1
                        continue
                    # 相交
                    elif end_y[lin3] < (k * end_x[lin3] + b):
                        # print("==============l_1==================")
                        # print(start_y[lin3])
                        # print(end_y[lin3])
                        xj = 1
                        A1 = 2 * (x2 - x1)
                        B1 = 2 * (y2 - y1)
                        C1 = x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
                        A2 = 2 * (x3 - x2)
                        B2 = 2 * (y3 - y2)
                        C2 = x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2
                        xw = ((C1 * B2) - (C2 * B1)) / ((A1 * B2) - (A2 * B1))
                        yw = ((A1 * C2) - (A2 * C1)) / ((A1 * B2) - (A2 * B1))
                        dis = math.sqrt((c_x - xw) ** 2 + (c_y - yw) ** 2)
                        # print("=========l1===========")
                        # print("xw,yw,dis: ", xw, yw, dis)
                        if dis < min_d:
                            min_line = lin3
                            min_px = xw
                            min_py = yw
                            min_d = dis
                            min_li = count_l
                            loc_re = 1
                            # print("=====l3==============")
                        count_l += 1
                        continue
                # 點在線下方 start_y[lin] < (k*start_x[lin] +b)
                elif start_y[lin3] < (k * start_x[lin3] + b):
                    # 終點在線上
                    if abs(end_y[lin3] - (k * end_x[lin3] + b)) < 0.01:
                        xj = 1
                        px = end_x[lin3]
                        py = end_y[lin3]
                        dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                        if dis < min_d:
                            min_line = lin3
                            min_px = px
                            min_py = py
                            min_d = dis
                            min_li = count_l
                            loc_re = 0
                            # print("=====l4==============")
                        count_l += 1
                        continue
                    # 不相交
                    elif end_y[lin3] < (k * end_x[lin3] + b):
                        count_l += 1
                        continue
                    # 相交
                    elif end_y[lin3] > (k * end_x[lin3] + b):
                        # print("==============l_2==================")
                        # print(start_y[lin3])
                        # print(end_y[lin3])\xj =
                        xj = 1
                        A1 = 2 * (x2 - x1)
                        B1 = 2 * (y2 - y1)
                        C1 = x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
                        A2 = 2 * (x3 - x2)
                        B2 = 2 * (y3 - y2)
                        C2 = x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2
                        print("A: ", A1, A2)
                        print("B: ", B1, B2)
                        xw = ((C1 * B2) - (C2 * B1)) / ((A1 * B2) - (A2 * B1))
                        yw = ((A1 * C2) - (A2 * C1)) / ((A1 * B2) - (A2 * B1))
                        dis = math.sqrt((c_x - xw) ** 2 + (c_y - yw) ** 2)
                        # print("=========l2===========")
                        # print("xw,yw,dis: ", xw, yw, dis)
                        if dis < min_d:
                            min_line = lin3
                            min_px = xw
                            min_py = yw
                            min_d = dis
                            min_li = count_l
                            loc_re = 1
                            # print("=====l3==============")
                        count_l += 1
                        continue
            # 檢查右側
            count_r = 0
            for lin4 in line[ri]:
                if lin4 == -1 or lin4 == last_li or count_r in sl_in:  # 點與點不存在直線
                    count_r += 1
                    continue
                x3 = x_s[count_r]
                y3 = y_s[count_r]
                # 起點在線上
                if abs(start_y[lin4] - (k * start_x[lin4] + b)) < 0.01:
                    xj = 1
                    px = start_x[lin4]
                    py = start_y[lin4]
                    dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                    if dis < min_d:
                        min_line = lin4
                        min_px = px
                        min_py = py
                        min_d = dis
                        min_ri = count_r
                        left_s = 0
                        loc_re = 1
                        # print("=====r1==============")
                    count_r += 1
                    continue
                # 點在線上方
                elif start_y[lin4] > (k * start_x[lin4] + b):
                    # 終點在線上
                    if abs(end_y[lin4] - (k * end_x[lin4] + b)) < 0.01:
                        xj = 1
                        px = end_x[lin4]
                        py = end_y[lin4]
                        dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                        # print("=========r1===========")
                        # print("xw,yw,dis: ", xw, yw, dis)
                        if dis < min_d:
                            min_line = lin4
                            min_px = px
                            min_py = py
                            min_d = dis
                            min_ri = count_r
                            left_s = 0
                            # print("=====r2==============")
                        count_r += 1
                        continue
                    # 不相交
                    elif end_y[lin4] > (k * end_x[lin4] + b):
                        count_r += 1
                        continue
                    # 相交
                    elif end_y[lin4] < (k * end_x[lin4] + b):
                        # print("==============r_1==================")
                        # print(start_y[lin4] + 1, end_y[lin4])\
                        xj = 1
                        A1 = 2 * (x2 - x1)
                        B1 = 2 * (y2 - y1)
                        C1 = x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
                        A2 = 2 * (x3 - x2)
                        B2 = 2 * (y3 - y2)
                        C2 = x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2
                        xw = ((C1 * B2) - (C2 * B1)) / ((A1 * B2) - (A2 * B1))
                        yw = ((A1 * C2) - (A2 * C1)) / ((A1 * B2) - (A2 * B1))
                        dis = math.sqrt((c_x - xw) ** 2 + (c_y - yw) ** 2)
                        # print("=========r2===========")
                        # print("xw,yw,dis: ", xw, yw, dis)
                        if dis < min_d:
                            min_line = lin4
                            min_px = xw
                            min_py = yw
                            min_d = dis
                            min_ri = count_r
                            left_s = 0
                            # print("=====r3==============")
                        count_r += 1
                        continue
                # 點在線下方 start_y[lin] < (k*start_x[lin] +b)
                elif start_y[lin4] < (k * start_x[lin4] + b):
                    # 終點在線上
                    if abs(end_y[lin4] - (k * end_x[lin4] + b)) < 0.01:
                        xj = 1
                        px = end_x[lin4]
                        py = end_y[lin4]
                        dis = math.sqrt((c_x - px) ** 2 + (c_y - py) ** 2)
                        if dis < min_d:
                            min_line = lin4
                            min_px = px
                            min_py = py
                            min_d = dis
                            min_ri = count_r
                            left_s = 0
                            # print("=====r4==============")
                        count_r += 1
                        continue
                    # 不相交
                    elif end_y[lin4] < (k * end_x[lin4] + b):
                        count_r += 1
                        continue
                    # 相交
                    elif end_y[lin4] > (k * end_x[lin4] + b):
                        # print("==============r_2==================")
                        # print(start_y[lin4] + 1, end_y[lin4])\
                        xj = 1
                        A1 = 2 * (x2 - x1)
                        B1 = 2 * (y2 - y1)
                        C1 = x2 ** 2 + y2 ** 2 - x1 ** 2 - y1 ** 2
                        A2 = 2 * (x3 - x2)
                        B2 = 2 * (y3 - y2)
                        C2 = x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2
                        xw = ((C1 * B2) - (C2 * B1)) / ((A1 * B2) - (A2 * B1))
                        yw = ((A1 * C2) - (A2 * C1)) / ((A1 * B2) - (A2 * B1))
                        dis = math.sqrt((c_x - xw) ** 2 + (c_y - yw) ** 2)
                        if dis < min_d:
                            min_line = lin4
                            min_px = xw
                            min_py = yw
                            min_d = dis
                            min_ri = count_r
                            left_s = 0
                            # print("=====r3==============")
                        count_r += 1
                        continue
                # print("r_dis: ", dis)
            # print("==============min_d:", min_d)
            # print("left_s: ", left_s)

            # 迭代結束
            if xj == 0:
                end = 1
                lin_n1 = cv.create_line(stx, sty, enx, eny, fill="black")  # blue為未處理線
                # print("lin_n:", lin_n1)
                # print("line in jieshu :", line)
                line[li][ri] = lin_n1
                line[ri][li] = lin_n1
                # print("line in jieshu :", line)
                start_x[lin_n1] = stx
                start_y[lin_n1] = sty
                end_x[lin_n1] = enx
                end_y[lin_n1] = eny
                # print("===========6====================")
                break

            # 判斷是左還是右
            # ==================================================OK
            # print("===========8====================")
            # print("min_line: ", min_line)
            # print("min_px: ", min_px)
            # print("min_py: ", min_py)
            # print("min_d: ", min_d)
            # print("left_s: ", left_s)
            # print("li,min_li: ", li, min_li)
            # print("ri,min_ri: ", ri, min_ri)
            # 與左側相交
            if left_s == 1:
                # print("line in left :", line)
                lin = min_line
                # 找到交點
                # print("====test==========")
                # print("lin: ", lin)
                # print("min_d",min_d)
                enx = min_px
                eny = min_py
                if end_x[lin] == start_x[lin]:
                    ks = 10000
                else:
                    ks = (end_y[lin] - start_y[lin]) / (end_x[lin] - start_x[lin])
                if x_s[li] == x_s[min_li]:
                    ks_t = 10000
                else:
                    ks_t = (y_s[li] - y_s[min_li]) / (x_s[li] - x_s[min_li])
                bs_t = y_s[li] - ks_t * x_s[li]
                # print("ks: ", ks)
                # print("shang xia: ", (y_s[ri] > (k * x_s[ri] + b)))
                # print("start: ",start_x[lin],  start_y[lin])
                # print("end: ",  end_x[lin],  end_y[lin])
                if abs(ks) < 0.001:
                    if y_s[ri] > (k * x_s[ri] + b):
                        start_x[lin] = min_px
                        start_y[lin] = min_py
                    else:
                        end_x[lin] = min_px
                        end_y[lin] = min_py
                else:
                    if y_s[ri] > (ks_t * x_s[ri] + bs_t):
                            end_x[lin] = min_px
                            end_y[lin] = min_py
                            print("==========l2=========")
                    else:
                            start_x[lin] = min_px
                            start_y[lin] = min_py
                            print("==========l3=========")
                            print(start_x[lin], start_y[lin], end_x[lin], end_y[lin])
                min_count_l = min_li
                # 剪枝
                # di為新的減值后線段
                # red為剪枝後的左右側連線
                lin_d1 = cv.create_line(start_x[lin], start_y[lin], end_x[lin], end_y[lin], fill=color)
                # 修改line中線段的長度
                line[li][min_count_l] = lin_d1
                line[min_count_l][li] = lin_d1
                # 刪除暫存線段中的舊線段
                line_d[li][min_count_l] = -1
                line_d[min_count_l][li] = -1
                # 記錄新線段的起點和終點
                start_x[lin_d1] = start_x[lin]
                start_y[lin_d1] = start_y[lin]
                end_x[lin_d1] = end_x[lin]
                end_y[lin_d1] = end_y[lin]
                # 在畫布上刪除舊線段
                cv.delete(lin)
                last_li = lin_d1
                # 畫出新線
                lin_n = cv.create_line(stx, sty, enx, eny, fill="blue")
                # green為超平面連線
                # 記錄新線段起點和終點
                line[li][ri] = lin_n
                line[ri][li] = lin_n
                start_x[lin_n] = stx
                start_y[lin_n] = sty
                end_x[lin_n] = enx
                end_y[lin_n] = eny
                # 設置下一次迭代起點
                next_s = eny
                next_x = enx
                li = min_count_l
                # print("min_l: ", li)
                # print("line[li][min_count_l] :", line[li][min_count_l])
                # print("line in left :", line)
            # 與右側相交
            else:
                # 記錄右側交點數據
                lin = min_line
                enx = min_px
                eny = min_py
                if end_x[lin] == start_x[lin]:
                    ks = 10000
                else:
                    ks = (end_y[lin] - start_y[lin]) / (end_x[lin] - start_x[lin])
                if x_s[ri] == x_s[min_ri]:
                    ks_t = 10000
                else:
                    ks_t = (y_s[ri] - y_s[min_ri]) / (x_s[ri] - x_s[min_ri])
                bs_t = y_s[ri] - ks_t * x_s[ri]
                # print("ks: ", ks)
                # print("shang xia: ", (y_s[ri] > (k * x_s[ri] + b)))
                # print("start: ",start_x[lin],  start_y[lin])
                # print("end: ",  end_x[lin],  end_y[lin])
                if abs(ks) < 0.001:
                    if y_s[li] > (k * x_s[li] + b):
                        start_x[lin] = min_px
                        start_y[lin] = min_py
                    else:
                        end_x[lin] = min_px
                        end_y[lin] = min_py
                else:
                    if y_s[li] > (ks_t * x_s[li] + bs_t):
                        end_x[lin] = min_px
                        end_y[lin] = min_py
                        print("==========r2=========")
                    else:
                        start_x[lin] = min_px
                        start_y[lin] = min_py
                        print("==========r3=========")
                        print(start_x[lin], start_y[lin], end_x[lin], end_y[lin])
                min_count_r = min_ri
                # 剪枝
                # red為剪枝後的左右側連線
                lin_d1 = cv.create_line(start_x[lin], start_y[lin], end_x[lin], end_y[lin], fill=color)
                # 修改line中保存的線段
                line[ri][min_count_r] = lin_d1
                line[min_count_r][ri] = lin_d1
                # 在暫存線段中刪除
                line_d[ri][min_count_r] = -1
                line_d[min_count_r][ri] = -1
                # 設置新線段的起點和終點
                start_x[lin_d1] = start_x[lin]
                start_y[lin_d1] = start_y[lin]
                end_x[lin_d1] = end_x[lin]
                end_y[lin_d1] = end_y[lin]
                # 在畫布中刪除舊線段
                cv.delete(lin)
                last_li = lin_d1
                # 畫出新線
                # print("===========11====================")
                lin_n = cv.create_line(stx, sty, enx, eny, fill="blue")
                # green為超平面連線
                # 記錄超平面線段起點和終點
                line[li][ri] = lin_n
                line[ri][li] = lin_n
                start_x[lin_n] = stx
                start_y[lin_n] = sty
                end_x[lin_n] = enx
                end_y[lin_n] = eny
                # 記錄下一次迭代起點
                next_s = eny
                next_x = enx
                ri = min_count_r
                # print("enx , eny: ", enx, eny)
                # print("min_r: ", min_count_r)
        # print("============================迭代结束====================================")
        # 剔除空直線
        for ld1 in sl_in:
            for ld2 in sl_in:
                if ld1 == ld2:
                    continue
                if line_d[ld1][ld2] != -1:  # 該線段未被修改過
                    kong = 1
                    lc = line[ld1][ld2]
                    for od1 in sl_in:
                        if od1 == ld1 or od1 == ld2:
                            continue
                        if line[ld1][od1] == -1 and line[ld2][od1] == -1:
                            continue
                        if line[ld1][od1] != -1:
                            lt = line[ld1][od1]
                            # 四種情況：起點相等、終點相等、起點等於終點
                            if start_x[lt] == start_x[lc] and start_y[lt] == start_y[lc]:
                                kong = 0
                                break
                            if start_x[lt] == end_x[lc] and start_y[lt] == end_y[lc]:
                                kong = 0
                                break
                            if end_x[lt] == end_x[lc] and end_y[lt] == end_y[lc]:
                                kong = 0
                                break
                            if start_x[lc] == end_x[lt] and start_y[lc] == end_y[lt]:
                                kong = 0
                                break
                        if line[ld2][od1] != -1:
                            lt = line[ld2][od1]
                            # 四種情況：起點相等、終點相等、起點等於終點
                            if start_x[lt] == start_x[lc] and start_y[lt] == start_y[lc]:
                                kong = 0
                                break
                            if start_x[lt] == end_x[lc] and start_y[lt] == end_y[lc]:
                                kong = 0
                                break
                            if end_x[lt] == end_x[lc] and end_y[lt] == end_y[lc]:
                                kong = 0
                                break
                            if start_x[lc] == end_x[lt] and start_y[lc] == end_y[lt]:
                                kong = 0
                                break
                    if kong == 1:  # 說明該直線為空直線，需要刪除
                        line[ld1][ld2] = -1
                        line[ld2][ld1] = -1
                        line_d[ld1][ld2] = -1
                        line_d[ld2][ld1] = -1
                        cv.delete(lc)
        for ld3 in sr_in:
            for ld4 in sr_in:
                if ld3 == ld4:
                    continue
                if line_d[ld3][ld4] != -1:
                    kong2 = 1
                    lc = line[ld3][ld4]
                    for od2 in sr_in:
                        if od2 == ld3 or od2 == ld4:
                            continue
                        if line[ld3][od2] == -1 and line[ld4][od2] == -1:
                            continue
                        if line[ld3][od2] != -1:
                            lt = line[ld3][od2]
                            # 四種情況：起點相等、終點相等、起點等於終點
                            if start_x[lt] == start_x[lc] and start_y[lt] == start_y[lc]:
                                kong2 = 0
                                break
                            if start_x[lt] == end_x[lc] and start_y[lt] == end_y[lc]:
                                kong2 = 0
                                break
                            if end_x[lt] == end_x[lc] and end_y[lt] == end_y[lc]:
                                kong2 = 0
                                break
                            if start_x[lc] == end_x[lt] and start_y[lc] == end_y[lt]:
                                kong2 = 0
                                break
                        if line[ld4][od2] != -1:
                            lt = line[ld4][od2]
                            # 四種情況：起點相等、終點相等、起點等於終點
                            if start_x[lt] == start_x[lc] and start_y[lt] == start_y[lc]:
                                kong2 = 0
                                break
                            if start_x[lt] == end_x[lc] and start_y[lt] == end_y[lc]:
                                kong2 = 0
                                break
                            if end_x[lt] == end_x[lc] and end_y[lt] == end_y[lc]:
                                kong2 = 0
                                break
                            if start_x[lc] == end_x[lt] and start_y[lc] == end_y[lt]:
                                kong2 = 0
                                break
                    if kong2 == 1:  # 說明該直線為空直線，需要刪除
                        line[ld3][ld4] = -1
                        line[ld4][ld3] = -1
                        line_d[ld3][ld4] = -1
                        line_d[ld4][ld3] = -1
                        cv.delete(lc)
        # print("line 的结果是： ", line)
        return 0
    # ========================================泰森多邊形算法===========================

    # ================================繪製convex hull======================================
    def convex(self, s_in):
        global xs_in, ys_in, line, start_x, start_y, end_x, end_y, x_s, y_s, con_line
        if len(s_in) == 0:
            tk.messagebox.showinfo(title='Hello', message='點集過少，無法合併！')
        #  窮盡搜索法直接合併
        for k1 in s_in:
            for k2 in s_in:
                if k1 == k2:
                    continue
                exit_up = 0
                exit_down = 0
                x_1 = x_s[k1]  # 通過index取出坐標
                y_1 = y_s[k1]
                x_2 = x_s[k2]
                y_2 = y_s[k2]
                # 計算斜率k0
                if x_1 == x_2:
                    k0 = 10000
                elif y_1 == y_2:
                    k0 = 0
                else:
                    k0 = (y_1 - y_2) / (x_1 - x_2)
                b0 = y_1 - k0 * x_1
                # 判斷左側是否有點在連線上方
                for k3 in s_in:
                    if k3 == k1 or k3 == k2:
                        continue
                    xk = x_s[k3]
                    yk = y_s[k3]
                    # k3處在兩點連線之下
                    if yk < (k0 * xk + b0):
                        exit_down = 1
                    else:
                        exit_up = 1
                exit_sum = exit_down + exit_up
                # 僅單側有點存在，該連線可行
                if exit_sum <= 1:
                    # convex hull的連線為黑色虛線
                    cv.delete(con_line[k1][k2])
                    lin_con = cv.create_line(x_s[k1], y_s[k1], x_s[k2], y_s[k2], fill='black', dash=(2, 4))
                    con_line[k1][k2] = lin_con
                    con_line[k2][k1] = lin_con
                else:
                    # 新的連線為折回角，刪除線段
                    cv.delete(con_line[k1][k2])
                    con_line[k1][k2] = -1
                    con_line[k2][k1] = -1



window = tk.Tk()
Canv(window)
window.mainloop()
