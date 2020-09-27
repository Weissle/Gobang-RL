import numpy as np


class Gobang:
    def __init__(self, x_len, y_len):
        self.sequence_ = []
        self.x_len = x_len
        self.y_len = y_len
        self.board_ = np.zeros((x_len, y_len), dtype=int)
        self.over_ = False
        self.winner_ = None
    def gameover(self):
        return self.over_

    def winner(self):
        return self.winner_

    def towin(self):
        self.over_ = True
        if len(self.sequence_) %2 == 0:
            self.winner_ = "White"
        else:
            self.winner_ = "Black"
    def check(self,x, y, chess):
        up_x,down_x = x,x
        left_y,right_y =y,y
        lu_lx,lu_ly = x,y
        lu_rx,lu_ry = x,y
        ru_lx,ru_ly = x,y
        ru_rx,ru_ry = x,y

        for i in range(5):
            if up_x >= 0 and self.board_[up_x,y]==chess:
                up_x -= 1
            if down_x < self.x_len and self.board_[down_x,y]==chess:
                down_x +=1
            if left_y >= 0 and self.board_[x,left_y]==chess:
                left_y -= 1
            if right_y < self.y_len and self.board_[x,right_y]==chess:
                right_y +=1
            if lu_lx >= 0 and lu_ly >=0 and self.board_[lu_lx,lu_ly]==chess:
                lu_lx -= 1
                lu_ly -= 1
            if lu_rx < self.x_len and lu_ry < self.y_len and self.board_[lu_rx,lu_ry]==chess:
                lu_rx += 1
                lu_ry += 1
            if ru_lx < self.x_len and ru_ly >=0 and self.board_[ru_lx,ru_ly]==chess:
                ru_lx += 1
                ru_ly -= 1
            if ru_rx >=0 and ru_ry < self.y_len and self.board_[ru_rx,ru_ry]==chess:
                ru_rx -= 1
                ru_ry += 1
        if down_x - up_x >= 6 or right_y - left_y >= 6 or lu_rx - lu_lx >=6 or ru_lx - ru_rx >=6:
            self.towin()
        '''        
        while up_x >= 0 and self.board_[up_x,y] == chess:
            up_x -= 1
        while down_x < self.x_len and self.board_[down_x,y] == chess:
            down_x += 1
        if down_x - up_x >= 4:
            towin()
            return
        
        while left_y>=0 and self.board_[x,left_y] == chess:
            left_y -= 1
        while right_y<self.y_len and self.board_[x,right_y] == chess:
            right_y += 1
        if down_x - up_x >= 4:
            towin()
            return
        '''

    def place(self, x, y):
        if self.over_ or  x < 0 or y < 0 or x >= self.x_len or y >= self.y_len or self.board_[x, y] != 0 :
            return
        chess = None
        if len(self.sequence_) % 2 == 0:
            chess = 1
        else:
            chess = -1
        self.sequence_.append((x,y))
        self.board_[x, y] = chess
        self.check(x,y,chess)

    def place_indexfrom1(self, x, y):
        self.place(x-1,y-1)
    
    def who_should_place(self):
        if len(self.sequence_) % 2 ==0:
            return "Black"
        else:
            return "White"
    
    def print_board(self):
        print(self.board_)