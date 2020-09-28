import torch
from torch import nn, optim
import numpy as np

class RLNet(nn.Module):
    def __init__(self):
        super(RLNet, self).__init__()
        self.conv = nn.Sequential(
            # 1 * 15 * 15
            nn.Conv2d(1, 32, 9),  # 32 * 7 * 7
            nn.ReLU(),
            nn.Conv2d(32, 256, 5, padding=1),  # 256 * 5 * 5
            nn.ReLU(),
    #        nn.MaxPool2d(3,1),  # 256 * 3 * 3
            nn.Conv2d(256, 1024, 3),  # 1024 * 3 * 3
            nn.ReLU(),
            nn.Conv2d(1024, 2048, 3),  # 2048 * 1 * 1
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 15**2)
        )

    def forward(self, board):
        first_ = self.conv(board.float())
        first_ = first_.view(board.shape[0],-1)
        output = self.fc(first_)
        return output

@torch.no_grad()
def test(net,board):
    board = board.view(1,1,15,15)
    probs = net(board)
    probs_softmax = nn.Softmax(dim=1)(probs)
    probs_rank_index = np.argsort(probs_softmax.numpy())
    for index in probs_rank_index[0][::-1]:
        x = int(index / 15)
        y = int(index % 15)
        if(board[0,0,x,y]==0):
            return x,y
    return -1,-1