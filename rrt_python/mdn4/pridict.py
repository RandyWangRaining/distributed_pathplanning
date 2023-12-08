import scipy.io as scio
import matplotlib.pyplot as plt
import sys
import numpy as np
import torch.utils.data as Data
import datetime
import os
import math
# sys.path.append('~/hzz/MDN/mdn')
import mdn
from models import MMDN
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt




def pridict(data42):
	#print(type(data42))
	#print(data42[1])
	data = np.zeros([42])
	for i in range(0,42):
		data[i] = data42[i]
	#print(data)
	data = torch.tensor(data)
	data = data.to(torch.float32) 
	data = data.reshape(1,42) 
	
	#print(data.shape)
	wi = 1000       #需要导入的工作空间的个数
	nodei=100     #每个工作空间需要导入的node个数
	device_cpu = torch.device("cpu")
	total_step = 0
	test_num = 0
	grad_clip = 0.5
	learning_rate = 1e-4
	train_N = 500                   #设置训练次数
	input_dims = 42                    #神经网络输入的维度
	hidden_dims = 256
	output_dims = 2                    #神经网络输出的维度
	num_gaussians = 24                  #用来拟合的高斯分布个数

	model = MMDN(input_dims, hidden_dims, output_dims, num_gaussians)
	weight_path = os.path.join('mdn4/model_2022-06-19_17-42-07.pth')
	model.load_state_dict(torch.load(weight_path,map_location=torch.device('cpu')))
	yy = model.sample(data)
	yy = yy.cpu().data.numpy()
	#m_x1,m_y1 = discrete_loss_cal(yy)
	a = yy[0][0]
	b = yy[0][1]
	#print(type(a))
	return [a,b]

def mean(x):
    avg = 0
    for i in range(0,50):
        avg += x[i].item()
    avg /= 50
    return avg
def discrete_loss_cal(yy):
	x1 = yy[:, 0]
	y1 = yy[:, 1]
	m_x1 = mean(x1)
	m_y1 = mean(y1)
	return m_x1, m_y1

def add(x,y):
	return x+y





