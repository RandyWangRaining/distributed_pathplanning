import torch

import numpy as np

import random
from torch.autograd import Variable
import torch.nn as nn

import scipy.io as scio  # 需要用到scipy库

# Environment Encoder

class Encoder(nn.Module):
	def __init__(self):
		super(Encoder, self).__init__()
		self.encoder = nn.Sequential(nn.Linear(2800, 512),nn.PReLU(),nn.Linear(512, 256),nn.PReLU(),nn.Linear(256, 128),nn.PReLU(),nn.Linear(128, 28))
			
	def forward(self, x):
		x = self.encoder(x)
		return x

	
def obs_zhankai(obs):
	n = len(obs)	
	temp=np.zeros((1400,2),dtype=np.float32)
	for i in range(0,n):
		for j in range(0,200):
			if i < 3:
				temp[i*200+j][0] = random.uniform(obs[i][0]-2.5,obs[i][0]+2.5)
				temp[i*200+j][1] = random.uniform(obs[i][1]-2.5,obs[i][1]+2.5)
			else:

				temp[i*200+j][0] = temp[(i-1)*200+j][0]
				temp[i*200+j][1] = temp[(i-1)*200+j][1]
	return temp

# 给一个工作空间编号wi，返回obs_28数据
def gen_obs28(wi,xo):
	Q = Encoder()
	Q.load_state_dict(torch.load('mdn4/models/cae_encoder.pkl',map_location=torch.device('cpu')))
	# if torch.cuda.is_available():
	# 	Q.cuda()

	xo=np.array(xo)
	xo=xo.reshape(-1,2)
	temp = obs_zhankai(xo)

	#temp=temp.reshape(len(temp)//2,2)
	obstacles=np.zeros((1,2800),dtype=np.float32)
	obstacles[0]=temp.flatten()
	inp=torch.from_numpy(obstacles)
	inp=Variable(inp)
	output=Q(inp)
	output=output.data.cpu()
	obs_28=output.numpy()
	obs_28 = obs_28.tolist()
	return obs_28

if __name__ == "__main__":
	data = [1,1]*7
	out = np.array(gen_obs28(1,data)).reshape(-1)
	print(out)
	print('ok')
