import torch
from torch import nn, optim
import numpy as np
import torch.utils.data as Data
import time

class RLNet(nn.Module):
    def __init__(self):
        super(RLNet, self).__init__()
        self.conv = nn.Sequential(
            # 1 * 15 * 15
            nn.Conv2d(1, 4, 3),  # 4 * 13 * 13
            nn.ReLU(),
            nn.Conv2d(4, 16, 3), # 16 * 11 * 11
            nn.ReLU(),
            nn.Conv2d(16, 64, 3),  # 64 * 9 * 9
            nn.ReLU(),
            nn.Conv2d(64, 256, 3, padding=1),  # 256 * 9 * 9
            nn.ReLU(),
            nn.Conv2d(256, 1024, 3),  # 1024 * 7 * 7
            nn.ReLU(), 
            nn.Conv2d(1024, 1024, 3),  # 1024 * 5 * 5
            nn.ReLU(),
            nn.Conv2d(1024, 1024, 3),  # 1024 * 3 * 3
            nn.ReLU(),
            nn.Conv2d(1024, 1024, 3),  # 1024 * 1 * 1
            nn.ReLU(),
        )
        self.fc = nn.Sequential(
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Dropout(p=0.5),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 15**2)
        )

    def forward(self, board):
        # print(board.shape)
        first_ = self.conv(board.float())
        first_ = first_.view(board.shape[0],-1)
        output = self.fc(first_)
        return output
@torch.no_grad()
def test(net,board,device):
    net = net.to(device)
    board = board.view(1,1,15,15)
    board = board.to(device)
    probs = net(board)
    probs_softmax = nn.Softmax(dim=1)(probs)
    probs_softmax = probs_softmax.cpu()
    probs_rank_index = np.argsort(probs_softmax.numpy())
    for index in probs_rank_index[0][::-1]:
        x = int(index / 15)
        y = int(index % 15)
        if(board[0,0,x,y]==0):
            return x,y
    return -1,-1

def train(net,data_iterator,iswin,optim,device,num_epochs):
    net = net.to(device)
    print("train on ",device)
    loss = torch.nn.CrossEntropyLoss()

    for epoch in range(num_epochs):
        
        for X,y in data_iterator:
            X = X.to(device)
            y = y.to(device)
            label = torch.zeros((len(y)),device=device,dtype=torch.long)
            for i in range(len(y)):
                label[i] = int(y[i][0]*15 + y[i][1])
            y_hat = net(X)
            l = loss(y_hat,label)
            optim.zero_grad()
            l.backward()
            optim.step()