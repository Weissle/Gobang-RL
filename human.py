from rule.GobangBase import *
import RL.RLNet as RL
import torch
import RL.DataCreate as DC
gobang = GobangForAI(15,15)
net = RL.RLNet()
print(net)

while gobang.gameover() == False:
    player = gobang.who_should_place()
    board = None
    if player == "Black":
        board = torch.from_numpy(gobang.board_)
    else:
        board = torch.from_numpy(gobang.board_white_)
    x,y = RL.test(net,board)
    if x==-1:
        print("error occur")
        break
    gobang.place(x,y)
print(gobang.winner()+" win ")
print(gobang.board_)
print(x,y)
dataCreator = DC.DataCreator()
a,b,c,d = dataCreator.create(gobang)
print(a,b,c,d)
'''
while board.gameover() == False:
    x =int(input("Please "+board.who_should_place()+" place x: "))
    y =int(input("Please "+board.who_should_place()+" place y: "))
    board.place(x,y)
    board.print_board()
print(board.winner()+" win ")
'''
