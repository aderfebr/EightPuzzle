import heapq
import tkinter as tk
from tkinter import scrolledtext

initial_state = [0,1,2,6,7,8,3,4,5]

class Node:  
    def __init__(self, state, parent=None, action=None, g=0, h=0):  
        self.state = state  
        self.parent = parent  
        self.action = action  
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __lt__(self, other):  
        return self.f < other.f

class Heuristic:
    def __init__(self,mode):
        self.mode = mode
        self.goal_state = [1,2,3,8,0,4,7,6,5]
    
    def calculate(self,state):
        if self.mode==0:  # 深度优先算法
            return 0
        if self.mode==1:  # 根据错位数估计
            heuristic_value = 0
            for i in range(len(state)):
                if state[i] != 0 and state[i] != self.goal_state[i]:
                    heuristic_value += 1
            return heuristic_value

class Astar:
    def __init__(self,initial_state,mode):
        self.expanded_nodes=0
        self.generated_nodes=0
        self.initial_state=[element for sublist in initial_state for element in sublist]
        self.goal_state = [1,2,3,8,0,4,7,6,5]
        self.mode=mode

    def search(self):
        frontier = []  # 开放列表
        explored = set()  # 已探索的节点集合
        heapq.heappush(frontier, Node(self.initial_state))  
        self.generated_nodes += 1  # 初始节点被生成

        while frontier:  
            node = heapq.heappop(frontier)  
            self.expanded_nodes += 1  # 一个节点被扩展

            if node.state == self.goal_state:  
                return self.reconstruct_path(node)  

            explored.add(tuple(node.state))  

            for successor in self.get_successors(node):  
                self.generated_nodes += 1  # 每个后继节点被生成时增加计数
                if tuple(successor.state) not in explored:  
                    heapq.heappush(frontier, successor)  

        return None  # 无解 

    def get_successors(self,node):  
        successors = []  
        state = node.state  
        zero_index = state.index(0)  # 找到空格的位置
        zero_row, zero_col = divmod(zero_index, 3)  # 计算空格的行和列

        actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        heuristic=Heuristic(self.mode)
        for action in actions:  
            new_row, new_col = zero_row + action[0], zero_col + action[1]  
            if 0 <= new_row < 3 and 0 <= new_col < 3:  # 确保新位置在网格内
                new_index = new_row * 3 + new_col  # 计算新位置的一维索引
                new_state = state[:]  # 复制当前状态
                new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]  # 交换空格和数字
                successors.append(Node(new_state, node, action, node.g + 1, heuristic.calculate(new_state)))  # 创建一个新节点，其中 g 是从起始状态到当前状态的实际代价，h 是启发式值
        return successors  

    def reconstruct_path(self,node):  
        path = []  
        while node is not None:  
            path.append((node.state, node.action))  # 添加当前节点状态和动作到路径
            node = node.parent  # 移动到父节点
        return path[::-1]  # 返回路径的逆序，因为我们是从目标节点回溯到起始节点的
    
    def output(self):
        path=self.search()
        root = tk.Tk()  
        root.title("计算结果")
        if path is None:
            root.geometry(("200x100"))
            tk.Label(root, text="无解!", font=("Microsoft YaHei", 12)).pack(padx=20,pady=10)
        else:
            path=path[1:]
            text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=60)  
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  
            for i in range(len(path)):
                txt=str(i+1)
                if path[i][1]==(1,0):
                    txt+=" 下 "
                if path[i][1]==(-1,0):
                    txt+=" 上 "
                if path[i][1]==(0,1):
                    txt+=" 右 "
                if path[i][1]==(0,-1):
                    txt+=" 左 "
                txt+=str(path[i][0])+"\n"
                text_area.insert(tk.END, txt)
            tk.Label(root, text=f"所用步数为 {len(path)}", font=("Microsoft YaHei", 12)).pack(padx=20,pady=10)
            tk.Label(root, text=f"扩展节点数为 {self.expanded_nodes}", font=("Microsoft YaHei", 12)).pack(padx=20,pady=10)
            tk.Label(root, text=f"生成节点数为 {self.generated_nodes}", font=("Microsoft YaHei", 12)).pack(padx=20,pady=10)
        root.mainloop()
