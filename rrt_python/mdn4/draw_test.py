import scipy.io as scio
import matplotlib.pyplot as plt
import sys
import numpy as np
import torch.utils.data as Data
import datetime
import os
import math
sys.path.append('~/hzz/MDN/mdn')
import mdn
from models import MMDN
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt


# 4950 * w 条数据
def test(m, data, w):
	#print(len(data))
    a = 5
    b = 8
    loss = 0
    num = 0
    fig = plt.figure()
    for i in range(1, a*b+1):
        index = int(np.random.randint(1, 100 * w, 1)) # 生成1-80000之间的一个数字
        p50 = data[index * 50:index * 50 + 50, :]
        p50 = p50.cuda()
        ls = model.loss(p50[:, 0:42], p50[:, 42: 44])
        test_loss = ls.cpu().data.numpy()
        loss += test_loss
        num += 1
        yy = m.sample(p50[:, 0:42])
        yy = yy.cpu().data.numpy()
        plt.subplot(a,b,i)
        plt.scatter(yy[:, 0], yy[:, 1],color='blue')
        y = p50[:, 42:44].cpu()
        plt.scatter(y[:, 0], y[:, 1],color='red')
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)
    return loss/num
    

def draw(m, data, wi ,w, pkl_num,t,model):
    a = 5
    b = 8
    loss = 0
    discrete_loss = 0
    num = 0


    #weight_path = os.path.join('/home/haichao/hzz/MDN/mdn4.0/model/model1000/model_w'+str(wi)+'_epoch_'+str(pkl_num)+'.pth')
    weight_path = os.path.join('/home/haichao/hzz/MDN/mdn4.0/model_2022-06-19_17-42-07.pth')
    model.load_state_dict(torch.load(weight_path))
    model = model.cuda()
    fig = plt.figure()
    for i in range(1, a*b+1):
        index = int(np.random.randint(1, 100 * w, 1)) # 生成1-80000之间的一个数字
        p50 = data[index * 50:index * 50 + 50, :]
        p50 = p50.cuda()
        ls = model.loss(p50[:, 0:42], p50[:, 42: 44])
        test_loss = ls.cpu().data.numpy()
        loss += test_loss
        num += 1
        yy = m.sample(p50[:, 0:42])
        y = p50[:, 42:44].cpu()
        d_loss, m_x1, m_x2, m_y1, m_y2 = discrete_loss_cal(yy,y)
        discrete_loss += d_loss
        yy = yy.cpu().data.numpy()
        plt.subplot(a,b,i)
        plt.scatter(yy[:, 0], yy[:, 1],color='blue')
        plt.scatter(y[:, 0], y[:, 1],color='red')
        plt.scatter(m_x1, m_y1,color='green')
        plt.scatter(m_x2, m_y2,color='green')
        plt.xlim(-15, 15)
        plt.ylim(-15, 15)
    mean_loss = loss/num
    discrete_loss = discrete_loss/num
    plt.title(t+"  workspace: " + str(w) + ", mean_loss: "+str(mean_loss)+"  discrete_loss: "+str(discrete_loss), x = -4, y = 6,fontdict={'weight':'normal','size': 20}) 
    fig.set_size_inches(15,10)
    print(t+"  workspace: " + str(w) + ", mean_loss: "+str(mean_loss)+"  discrete_loss: "+str(discrete_loss))   


def mean(x):
    avg = 0
    for i in range(0,50):
        avg += x[i].item()
    avg /= 50
    return avg
def discrete_loss_cal(yy,y):
	x1 = yy[:, 0]
	y1 = yy[:, 1]
	x2 = y[:, 0]
	y2 = y[:, 1]
	m_x1 = mean(x1)
	m_x2 = mean(x2)
	m_y1 = mean(y1)
	m_y2 = mean(y2)
	discrete_loss = math.sqrt( (mean(x1)-mean(x2))**2 + (mean(y1)-mean(y2))**2 )
	return discrete_loss, m_x1, m_x2, m_y1, m_y2











def not_draw(m, data, wi ,w, pkl_num,t,model):
    a = 5
    b = 8
    loss = 0
    discrete_loss = 0
    num = 0
    weight_path = os.path.join('/home/haichao/hzz/MDN/mdn/model/model1000/model_w'+str(wi)+'_epoch_'+str(pkl_num)+'.pth')
    model.load_state_dict(torch.load(weight_path))
    model = model.cuda()
    for i in range(1, a*b+1):
        index = int(np.random.randint(1, 100 * w, 1)) # 生成1-80000之间的一个数字
        p50 = data[index * 50:index * 50 + 50, :]
        p50 = p50.cuda()
        ls = model.loss(p50[:, 0:42], p50[:, 42: 44])
        test_loss = ls.cpu().data.numpy()
        loss += test_loss
        num += 1
        yy = m.sample(p50[:, 0:42])
        y = p50[:, 42:44].cpu()
        d_loss, m_x1, m_x2, m_y1, m_y2 = discrete_loss_cal(yy,y)
        discrete_loss += d_loss
        yy = yy.cpu().data.numpy()
    mean_loss = loss/num
    discrete_loss = discrete_loss/num
    print(t+"  epoch: " + str(pkl_num) + ", mean_loss: "+str(mean_loss)+"  discrete_loss: "+str(discrete_loss))   
    return mean_loss, discrete_loss


def draw_test():
	wi = 1000       #需要导入的工作空间的个数
	nodei=100     #每个工作空间需要导入的node个数
	device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
	device_cpu = torch.device("cpu")

	#加载数据，wi为工作空间数量，nodei为每个工作空间导入的node数量

	train_sets = torch.load( '/home/haichao/hzz/MDN/mdn/train_test_data/dataset_train'+str(wi)+'.pth')
	test_sets = torch.load('/home/haichao/hzz/MDN/mdn/train_test_data/dataset_test'+str(wi)+'.pth')
	unknown = torch.load('/home/haichao/hzz/MDN/mdn/train_test_data/train_sets_18001-20000.pkl')
	print("加载成功")




	total_step = 0
	test_num = 0
	grad_clip = 0.5
	learning_rate = 1e-4


	print("注意：红点为原始50个点，蓝点为MDN计算的点")
	train_N = 500                   #设置训练次数
	input_dims = 42                    #神经网络输入的维度
	hidden_dims = 256
	output_dims = 2                    #神经网络输出的维度
	num_gaussians = 24                  #用来拟合的高斯分布个数

	model = MMDN(input_dims, hidden_dims, output_dims, num_gaussians)

	pkl_num = 158
	#pkl_num = int(sys.argv[1])

	#weight_path = os.path.join('../mdn/model/model1000/model_w'+str(wi)+'_epoch_'+str(pkl_num)+'.pth')
	#model.load_state_dict(torch.load(weight_path))
	#model = model.cuda()

	#draw(model, test_sets, wi, wi*0.2*0.95,pkl_num,"test_sets",model)

	#draw(model, train_sets, wi,wi*0.8*0.95,pkl_num,"train_sets",model)

	#plt.show()

	# draw(model, test_sets, wi, wi*0.2*0.95,  2 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  2 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  2 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  2 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  2 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	# draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	#draw(model, test_sets, wi, wi*0.2*0.95,  168 ,"test_sets",model)
	#draw(model, train_sets, wi,wi*0.8*0.95,13,"train_sets",model)

	draw(model, unknown, wi,wi*0.8*0.95,13,"unknown",model)
	plt.show()

	p1 = 13
	mean_loss = 0
	discrete_loss = 0
	N = 5
	for i in range(N):
		m_l,d_l = not_draw(model, train_sets, wi,wi*0.8*0.95,p1,"train_sets",model)
		mean_loss += m_l
		discrete_loss += d_l
	mean_loss = mean_loss/N
	discrete_loss = discrete_loss/N
	print("mean_loss = ", mean_loss, "   discrete_loss: ",discrete_loss)
	#plt.show()
#draw_test()





