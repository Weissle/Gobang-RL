import sys
sys.path.append('../')
import torch
import torch.utils.data as Data
from rule.GobangBase import * 
import RL.RLNet as RL
import RL.DataCreate as DC
import RL.DataLoader as DL
import time

net = RL.RLNet()
lr = 0.01
net.load_state_dict(torch.load('./temp.pt'))
optim = torch.optim.Adam(net.parameters(),lr=lr)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


gobang = GobangForAI(15,15)
while gobang.gameover() == False:
    player = gobang.who_should_place()
    board = None
    if player == "Black":
        board = torch.from_numpy(gobang.board_)
    else:
        board = torch.from_numpy(gobang.board_white_)
    x,y = RL.test(net,board,device)
    print(x,y)
    gobang.place(x,y)
    print(x,y)
    print(gobang.board_)
    a = input()