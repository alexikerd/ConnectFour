import os
from os import path
import random
import cv2
from tqdm import tqdm
import pickle

import numpy as np
import pandas as pd
import matplotlib as plt
from matplotlib import pyplot
from matplotlib.image import imread
from sklearn.neighbors import NearestNeighbors
import torch
import torchvision
import torch.nn as nn
import torchvision.transforms as transforms
import torch.optim as optim
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import ImageFolder
from torch.autograd import Variable

img_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])



class ImageDataset(Dataset):

    def __init__(self,data,transform=img_transform):
        self.data = data
        self.transform = transform
        
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self,index):

        if torch.is_tensor(index):
            index = index.tolist()

        item = self.data.iloc[index]["board"]
        image = item/255
        
        if self.transform:
            image = self.transform(image)
        
        return image




class C4Net(nn.Module):
    def __init__(self):
        super(C4Net, self).__init__()
        
        self.Conv1 = nn.Conv2d(3,3,3)
        self.Conv2 = nn.Conv2d(3,3,3)
        self.Conv3 = nn.Conv2d(3,3,3)
    

        self.BNorm1 = nn.BatchNorm2d(3)
        self.BNorm2 = nn.BatchNorm2d(3)
        self.BNorm3 = nn.BatchNorm2d(3)
        self.BNorm4 = nn.BatchNorm2d(3)

        self.fc1 = nn.Linear(1452, 800)
        self.fc2 = nn.Linear(800, 400)
        self.fc3 = nn.Linear(400, 100)

        self.fc4 = nn.Linear(100,7)
        self.fc5 = nn.Linear(100,1)


        


        
    def predict(self, x):
        
        x = F.relu(self.BNorm1(self.Conv1(x)))                          # batch_size x num_channels x board_x x board_y
        x = F.relu(self.BNorm2(self.Conv2(x)))                          # batch_size x num_channels x board_x x board_y
        x = F.relu(self.BNorm3(self.Conv3(x)))                          # batch_size x num_channels x (board_x-2) x (board_y-2)
        x = x.view(-1,1452)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))

        pi = self.fc4(x)                                                                     
        v = self.fc5(x)   

        return F.softmax(pi,dim=1).numpy()[0], torch.tanh(v).numpy()[0]
    
