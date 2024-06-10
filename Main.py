import tkinter as tk
from tkinter.messagebox import *
import random
import sys
sys.dont_write_bytecode = True
from Astar import Astar

class EightPuzzle:  
    def __init__(self, root):  #初始化棋盘和计数器
        self.root = root
        board = [0,1,2,3,4,5,6,7,8]
        random.shuffle(board)
        self.board=[board[:3],board[3:6],board[6:]]
        self.cnt=0
        self.create_widgets()
    
    def check(self):
        if self.board==[
            [1, 2, 3],  
            [8, 0, 4],
            [7, 6, 5]
        ]:
            showinfo("成功!","所用步数为"+str(self.cnt))

    def create_widgets(self):  #放置按钮
        self.frame = tk.Frame(self.root)  
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  

        for i in range(3):  
            for j in range(3):  
                btn = tk.Button(self.frame, text=str(self.board[i][j]), font=("Helvetica", 24),   
                                command=lambda r=i, c=j: self.move(r, c))  
                btn.grid(row=i, column=j, padx=10, pady=10)
                btn.userdata = (i, j)

        restart_button = tk.Button(self.root, text="重置", command=self.restart_game)  
        restart_button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        button = tk.Button(self.root, text="A*算法(错位数距离)", command=lambda: Astar(self.board,2).output())  
        button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        button = tk.Button(self.root, text="A*算法(错位数个数)", command=lambda: Astar(self.board,1).output())  
        button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        button = tk.Button(self.root, text="深度优先算法", command=lambda: Astar(self.board,0).output())  
        button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        self.step_label = tk.Label(self.root, text="所用步数: 0", font=("Microsoft YaHei", 12))
        self.step_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  

    def restart_game(self):  #重置游戏
        board = [0,1,2,3,4,5,6,7,8]
        random.shuffle(board)
        self.board=[board[:3],board[3:6],board[6:]]
        self.cnt=0
        self.step_label.config(text=f"所用步数: {self.cnt}")
        self.update_buttons()


    def find_zero(self):  #查找空格的当前位置
        for i in range(3):  
            for j in range(3):  
                if self.board[i][j] == 0:  
                    return i, j  

    def move(self, row, col):  #移动空格到其他位置
        zero_row, zero_col = self.find_zero()  
        if (row == zero_row - 1 and col == zero_col) or (row == zero_row + 1 and col == zero_col) or (row == zero_row and col == zero_col - 1) or (row == zero_row and col == zero_col + 1):  
            self.board[zero_row][zero_col], self.board[row][col] = self.board[row][col], self.board[zero_row][zero_col]  
            self.update_buttons()
            self.cnt+=1
            self.step_label.config(text=f"所用步数: {self.cnt}")
        self.check()

    def update_buttons(self):  #更新按钮
        for i in range(3):  
            for j in range(3):  
                btn = self.frame.grid_slaves(row=i, column=j)[0]
                btn.config(text=str(self.board[i][j]))

if __name__ == "__main__":
    root = tk.Tk()  
    root.title("八数码")  
    game = EightPuzzle(root)  
    root.mainloop()