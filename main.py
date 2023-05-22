import tkinter as tk
from tkinter.messagebox import showinfo
import random


class Snake():
    """ 贪吃蛇游戏  """
    def __init__(self):
        """ 游戏参数设置 """
        
        self.window     = None                # 实例化的窗体
        self.canvas     = None                # 实例化的画布
        self.loop       = 0                   # 暂停标记，1为开启，0为暂停
        self.loop_id    = None                # 实例化loop，用来取消循环
        
        self.game_map   = []                  # 整个游戏的地图
        self.snake_body = []                  # 蛇身的坐标集
        self.food_xy    = []                  # 食物的坐标
        self.head_x     = 0                   # 蛇头的X坐标
        self.head_y     = 0                   # 蛇头的Y坐标
        self.dd         = [0]                 # 记录按键方向
        
        self.len        = 3                   # 蛇身初始长度（最小设定值为1，不包括蛇头）
        self.body_len   = self.len            # 蛇身当前长度
        self.FPS        = 120                 # 蛇的移动速度（单位毫秒）
        self.row_cells  = 22                  # 一行多少个单元格(含边框)
        self.col_cells  = 22                  # 一共多少行单元格(含边框)
        self.canvas_bg  = 'white'             # 游戏背景色
        self.cell_size  = 25                  # 方格单元格大小
        self.cell_gap   = 1                   # 方格间距
        self.frame_x    = 15                  # 左右边距
        self.frame_y    = 15                  # 上下边距
        self.win_w_plus = 220                 # 窗口右边额外多出的宽度
        
        self.color_dict = {0:  '#d7d7d7',     # 0表示空白
                           1:   'yellow',     # 1代表蛇头
                           2:  '#009700',     # 2代表蛇身
                           3:      'red',     # 3代表食物
                           4:  '#808080'}     # 4代表墙
        
        self.run_game()

    
    def window_center(self,window,w_size,h_size):
        """ 窗口居中 """
        screenWidth  =  window.winfo_screenwidth()  # 获取显示区域的宽度
        screenHeight = window.winfo_screenheight()  # 获取显示区域的高度
        left =  (screenWidth - w_size) // 2
        top  = (screenHeight - h_size) // 2
        window.geometry("%dx%d+%d+%d" % (w_size, h_size, left, top))
        
        
    def create_map(self):
        """ 创建地图列表 """
        self.game_map = [] 
        for i in range(0,self.col_cells):
            self.game_map.append([])
        for i in range(0,self.col_cells):
           for j in range(0,self.row_cells):
              self.game_map[i].append(j)   
              self.game_map[i][j] = 0  # 生成一个全是0的空数列


    def create_wall(self):
        """ 绘制边框 """
        for i in range(0,self.row_cells-1):
            self.game_map[0][i] = 4
            self.game_map[self.col_cells-1][i] = 4
        
        for i in range(0,self.col_cells-1):
            self.game_map[i][0] = 4
            self.game_map[i][self.row_cells-1] = 4
        self.game_map[-1][-1] = 4
        

    def create_canvas(self):
        """ 创建画布 """
        canvas_h = self.cell_size * self.col_cells + self.frame_y*2
        canvas_w = self.cell_size * self.row_cells + self.frame_x*2
        
        self.canvas = tk.Canvas(self.window,  bg = self.canvas_bg, 
                                height = canvas_h,
                                 width = canvas_w,
                           highlightthickness = 0)
        self.canvas.place(x=0,y=0)
        
        
    def create_cells(self):
        """ 创建单元格 """
        for y in range(0,self.col_cells):
            for x in range(0,self.row_cells):
                a = self.frame_x + self.cell_size*x
                b = self.frame_y + self.cell_size*y
                c = self.frame_x + self.cell_size*(x+1)
                d = self.frame_y + self.cell_size*(y+1)
                e = self.canvas_bg
                f = self.cell_gap
                g = self.color_dict[self.game_map[y][x]]
                self.canvas.itemconfig(self.canvas.create_rectangle(a,b,c,d, outline=e, width=f, fill=g),fill=g)
        

    def create_snake(self):
        """ 创建蛇头和蛇身 """
        self.snake_body = [[self.col_cells // 2 , self.row_cells // 2]] # 蛇头出生地在地图的中央
        self.game_map[self.snake_body[0][0]][self.snake_body[0][1]] = 1  # 蛇头上色，颜色为定义的1


    def create_food(self):
        """ 创建食物 """
        
        self.food_xy = [0,0]
        self.food_xy[1] = random.randint(1, self.row_cells-2)
        self.food_xy[0] = random.randint(1, self.col_cells-2)
        
        while self.game_map[self.food_xy[0]][self.food_xy[1]] != 0:
            self.food_xy[0] = random.randint(1,self.row_cells-2)
            self.food_xy[1] = random.randint(1,self.col_cells-2)

        self.game_map[self.food_xy[0]][self.food_xy[1]] = 3


    def snake_xy(self):
        """ 获取蛇头坐标 """
        xy = []
        for i in range(0,self.col_cells):
                try: # 查找数值为1的坐标，没有就返回0。为防止在0列，先加上1，最后再减去。
                    x = self.game_map[i].index(1) + 1 
                except:
                    x = 0
                xy.append(x)
        self.head_x = max(xy)
        self.head_y = xy.index(self.head_x)
        self.head_x = self.head_x - 1 # 之前加1，现在减回
        
        
    def move_snake(self,event):
        """ 蛇体移动 """
        def move_key(a,b,c,d):  # 记录按键的方向，1上2下3左4右
            direction = event.keysym
                    
            if   self.head_x != self.snake_body[-1][1]:
                if(direction == a):
                    self.dd[0] = 1
                if(direction == b):
                    self.dd[0] = 2
            else:
                if(direction == c):
                    self.dd[0] = 3
                if(direction == d):
                    self.dd[0] = 4
                  
            if   self.head_y != self.snake_body[-1][0]:
                if(direction == c):
                    self.dd[0] = 3
                if(direction == d):
                    self.dd[0] = 4
            else:
                if(direction == a):
                    self.dd[0] = 1
                if(direction == b):
                    self.dd[0] = 2

        def pause_key(key):
            """ 暂停键 """
            direction = event.keysym
            if(direction == key):
                self.loop = 0
                showinfo('暂停','按确定键继续')
                self.loop = 1
                self.window.after(self.FPS, self.game_loop)
                    
        move_key('w','s','a','d')
        move_key('W','S','A','D')
        move_key('Up','Down','Left','Right')
        pause_key('space')
        
        
    def game_over(self):
        
        def over():
            showinfo('Game Over','再来一局')
            self.body_len = self.len
            self.game_start()
        
        if [self.head_y,self.head_x] in self.snake_body[0:-2]:
            over()
        if self.head_x == self.row_cells - 1 or self.head_x == 0:
            over()
        if self.head_y == self.col_cells - 1 or self.head_y == 0:
            over()
        
        
    def snake_record(self):
        """ 蛇身 """ # 记录蛇头运行轨迹，生成蛇身
        
        temp = []
        temp.append(self.head_y)
        temp.append(self.head_x)
        self.snake_body.append(temp) 
        
        if self.snake_body[-1] == self.snake_body[-2]: 
            del self.snake_body[-1]
        
        if [self.head_y,self.head_x] == self.food_xy: # 碰到食物身体加长，并再随机生成一个食物
            self.body_len += 1
            self.create_food()
        elif len(self.snake_body) > self.body_len:  # 限制蛇身长度，不超过设定值
            self.game_map[self.snake_body[0][0]][self.snake_body[0][1]] = 0
            del self.snake_body[0]
            

    def auto_move(self):
        """ 自动前进 """
        def move(d,x,y):
            if self.dd[0] == d:  # 根据方向值来决定走向
                self.game_map[self.head_y + x][self.head_x + y] = 1
                self.game_map[self.head_y + 0][self.head_x + 0] = 2
            
        move( 1, -1,  0 )
        move( 2,  1,  0 )
        move( 3,  0, -1 )
        move( 4,  0,  1 )


    def game_loop(self):
        """ 游戏循环刷新 """
        self.snake_record()
        self.auto_move()
        self.snake_xy()
        self.canvas.delete('all') # 清除canvas
        self.create_cells()
        self.game_over()
        if self.loop == 1:
            self.loop_id  = self.window.after(self.FPS, self.game_loop)
        
        
    def game_start(self):
        """  """
        self.loop = 1 # 暂停标记，1为开启，0为暂停
        self.dd = [0] # 记录按键方向
        self.create_map()
        self.create_wall()
        self.create_snake()
        self.create_food()
        self.window.bind('<Key>', self.move_snake)
        self.snake_xy()
        self.game_loop()
        
        def close_w():
            self.loop = 0
            self.window.after_cancel(self.loop_id)
            self.window.destroy()
            
        self.window.protocol('WM_DELETE_WINDOW', close_w)
        self.window.mainloop()
        
        
    def run_game(self):
        """ 开启游戏 """
        
        self.window = tk.Tk()
        self.window.focus_force() # 主窗口焦点
        self.window.title('Snake')
        
        win_w_size = self.row_cells * self.cell_size + self.frame_x*2 + self.win_w_plus 
        win_h_size = self.col_cells * self.cell_size + self.frame_y*2
        self.window_center(self.window,win_w_size,win_h_size)
        
        txt_lable = tk.Label(self.window, text=
                              "方向键移动，或者"
                             +"\n字母键WSAD移动"
                             +"\n（大小写均可）"
                             +"\n"
                             +"\n空格键暂停"
                             +"\n作者:周玄玄",
                             font=('Yahei', 15),anchor="ne", justify="left")
        
        txt_lable.place(x = self.cell_size * self.col_cells + self.cell_size*2, 
                        y = self.cell_size*6)
        
        self.create_canvas()
        self.game_start()
        
        
if __name__ == '__main__':
    
    Snake()

