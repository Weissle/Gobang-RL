import torch.utils.data  as Data
#import torch.distributions.transforms as transforms
import torchvision.transforms as transforms
import torch
class myDataset(Data.Dataset):
    def __init__(self,boards,places):
        self.boards = torch.from_numpy(boards)
        self.places = torch.from_numpy(places)

    def __len__(self):
        return len(self.places)
    def __getitem__(self,index):
        return self.boards[index],self.places[index]

def getDataLoader(boards,places):
    dataset = myDataset(boards,places)
    mytransform = transforms.Compose([
        transforms.ToTensor()
    ])
    loader = Data.DataLoader(dataset,batch_size=50,shuffle=True)
    return loader