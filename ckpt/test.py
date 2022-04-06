import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split


x= np.arange(10)
print(x)
print()
a, b = train_test_split(x, test_size=0.1, random_state=42, shuffle=True)
print(a)
print(b)

help(DataLoader)