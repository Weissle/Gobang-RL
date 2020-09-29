import sys
sys.path.append("../")
import torch
import numpy as np

class DataCreator:
    def __init__(self):
        pass
    #return winner_board, winner_place, loser_board, loser_place
    def create(self,record):
        chess_num = len(record.sequence_)
        black_num = chess_num % 2 + int(chess_num/2)
        white_num = chess_num - black_num
        black_record = np.empty((black_num,1,record.x_len,record.y_len),dtype=float)
        white_record = np.empty((white_num,1,record.x_len,record.y_len),dtype=float)
        black_place = np.empty((black_num,2),dtype=float)
        white_place = np.empty((white_num,2),dtype=float)
        black_board = np.zeros((record.x_len,record.y_len),dtype=float)
        white_board = np.zeros((record.x_len,record.y_len),dtype=float)
        sequence = record.sequence_
        black_index,white_index = 0,0
        for index in range(chess_num):
            point = sequence[index]
            x,y = point[0],point[1]
            #黑子下棋
            if index % 2 == 0:
                black_record[black_index,0,:,:] = black_board[:,:]
                black_place[black_index,:] = point
                black_index += 1
                black_board[x,y] = 1
                white_board[x,y] = -1
            else:
                white_record[white_index,0,:,:] = white_board[:,:]
                white_place[white_index,:] = point
                white_index += 1
                black_board[x,y] = -1
                white_board[x,y] = 1
        '''
        black_place = torch.from_numpy(black_place)
        black_record = torch.from_numpy(black_record)
        white_place = torch.from_numpy(white_place)
        white_record = torch.from_numpy(white_record)
        '''
        if record.winner() == "Black":
            return black_record,black_place,white_record,white_place
        else:
            return white_record,white_place,black_record,black_place

        
