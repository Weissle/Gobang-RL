import torch
import torch.utils.data as Data
from rule.GobangBase import * 
import RL.RLNet as RL
import RL.DataCreate as DC
import RL.DataLoader as DL
import time
from torchsummary import summary
net = RL.RLNet()
#print(net)
train_times = 500
borad_per_train = 10
lr = 0.01
epochs_num = 5
dataCreator = DC.DataCreator()
optim = torch.optim.Adam(net.parameters(),lr=lr)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

start = time.time()
for i in range(train_times):
    winner_board,winner_place = np.zeros((0)),np.zeros((0))
    for j in range(borad_per_train):
        gobang = GobangForAI(15,15)
        while gobang.gameover() == False:
            player = gobang.who_should_place()
            board = None
            if player == "Black":
                board = torch.from_numpy(gobang.board_)
            else:
                board = torch.from_numpy(gobang.board_white_)
            x,y = RL.test(net,board,device)
            gobang.place(x,y)
        if gobang.winner == "None":
            continue
        temp_winner_board,temp_winner_place,_, _ = dataCreator.create(gobang)
        if len(winner_board) == 0:
            winner_board = temp_winner_board
            winner_place = temp_winner_place
        else:
            winner_board = np.concatenate((winner_board,temp_winner_board))
            winner_place = np.concatenate((winner_place,temp_winner_place))
    winner_loader = DL.getDataLoader(winner_board,winner_place)
    RL.train(net,winner_loader,True,optim,device,epochs_num)
    if i and i % 50 == 0:
        torch.save(net.state_dict(),"./model/temp.pt")
print(time.time()-start)


gobang = GobangForAI(15,15)
while gobang.gameover() == False:
    player = gobang.who_should_place()
    board = None
    if player == "Black":
        board = torch.from_numpy(gobang.board_)
    else:
        board = torch.from_numpy(gobang.board_white_)
    x,y = RL.test(net,board,device)
    gobang.place(x,y)
    print(x,y)
    print(gobang.board_)
    a = input()
print(gobang.winner()+" win ")
print(gobang.board_)
print(x,y)