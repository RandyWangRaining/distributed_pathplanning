"""A script that shows how to use the MDN. It's a simple MDN with a single

nonlinearity that's trained to output 1D samples given a 2D input.

"""
import scipy.io as scio
import matplotlib.pyplot as plt
import sys
import numpy as np
import torch.utils.data as Data
import datetime
import os

sys.path.append('../mdn')
import mdn
from models import MMDN
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt

TensorWriter = SummaryWriter('./tensorboard_data')

"""
tensorboard --logdir=./tensorboard_data --port 1234
http://localhost:1234/
"""

wi = 9000       #需要导入的工作空间的个数
nodei=100     #每个工作空间需要导入的node个数
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
device_cpu = torch.device("cpu")

def data_loader(wi,nodei):              #加载数据
    train_Sets=[]
    for w in range(wi):                 #wi为导入工作空间的数量
        print("导入工作空间进度：",100  * w/wi, "%")
        train_sets = []
        xo_name = 'obs/obs%d'%w
        xo = scio.loadmat(xo_name)
        xo = xo['obs']
        xo = xo.flatten()
        if xo.size>28:
            continue
        for i in range(1,nodei):        #nodei为每个工作空间导入node的数量
            file_name='../data/result%d'%w + '/node%d'%i
            data = scio.loadmat(file_name)
            polynode = data['set']      #polynode为多边形的顶点坐标
            polynode=polynode.flatten()
            if polynode.size>12:
                continue
            polynode=np.append(xo,polynode)
            greennode=data['rnodez']    #greennode为50个可行点
            polynode = np.append(polynode, greennode[1])        #加入终点坐标
            for j in range(2,52):
                if polynode.size>42:
                    continue
                train_set = np.append(polynode,greennode[j])    #将50个可行点处理成标签数据
                train_Sets.append(train_set)
        print(len(train_Sets)/44/50/100)
        #train_Sets.append(train_sets)
    train_Sets=np.array(train_Sets)          #将wi个工作空间里的node数据集合在一起作为训练集  总数据条数为wi*nodei*50
    # np.random.shuffle(train_Sets)                             #对数据进行随机化处理
    #train_Sets = torch.tensor(train_Sets)                     #转化为张量

    a = np.vstack(train_Sets).astype(float)
    train_Sets = torch.from_numpy(a)

    train_Sets = train_Sets.to(torch.float32)                 #转化为32位浮点型数据
    split = int(int(8000 * 50 * 100))
    test_Sets = train_Sets[split:, :]
    train_Sets = train_Sets[0:split, :]
    print('test set size: ',test_Sets.size())
    print('train set size: ', train_Sets.size())
    return train_Sets, test_Sets



#train_sets,test_sets=data_loader(wi,nodei)      #加载训练集

#torch.save(test_sets,  '../train_test_data/dataset_test{}.pth'.format(0))
#torch.save(train_sets,  '../train_test_data/dataset_train{}.pth'.format(0))

# directories setup
train_sets = torch.load( '../zzj/train_sets_0-20000.pkl')
#train_sets = torch.load( '../train_test_data/dataset_train0.pth')
#test_sets = torch.load('../train_test_data/dataset_test0.pth')

ws_num_train = 18000
sample_num_train = ws_num_train*20*5*50
test_sets = train_sets[sample_num_train:,:]
train_sets = train_sets[0:sample_num_train,:]


batch_size = 64
dataloader_train = Data.DataLoader(
    dataset=train_sets,
    batch_size=batch_size,
    shuffle=True,
    num_workers=10, pin_memory=True)

total_step = 0
test_num = 0
grad_clip = 0.5
learning_rate = 1e-4


def test(m, data):

    for i in range(1,10):
        index = int(np.random.randint(1, 100 * 800, 1))
        p50 = data[index * 50:index * 50 + 50, :]
        p50 = p50.cuda()
        yy = m.sample(p50[:, 0:42])
        yy = yy.cpu().data.numpy()
        plt.subplot(3,3,i)
        plt.scatter(yy[:, 0], yy[:, 1],color='blue')
        y = p50[:, 42:44].cpu()
        plt.scatter(y[:, 0], y[:, 1],color='red')
    plt.show()



train_N = 500                   #设置训练次数
input_dims = 42                    #神经网络输入的维度
hidden_dims = 256
output_dims = 2                    #神经网络输出的维度
num_gaussians = 24                  #用来拟合的高斯分布个数
# model = nn.Sequential(             #神经网络的模型，可调参数，包括神经网络的层数，各层神经网络的神经元个数
#     nn.Linear(input_dims, 256),nn.Tanh(),
#     nn.Linear(256, 512),nn.Tanh(),
#     nn.Linear(512, 1024),nn.Tanh(),
#     mdn.MDN(1024, output_dims, num_gaussians)
# )

model = MMDN(input_dims, hidden_dims, output_dims, num_gaussians)
weight_path = os.path.join('./model','model_{}.pth'.format('2022-06-07_20-14-43'))
#model.load_state_dict(torch.load(weight_path))

model = model.cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, weight_decay=0)

dataloader_train = Data.DataLoader(
    dataset=train_sets,
    batch_size=batch_size,
    shuffle=True,
    num_workers=10, pin_memory=True)

dataloader_test = Data.DataLoader(
    dataset=test_sets,
    batch_size=batch_size,
    shuffle=True,
    num_workers=10, pin_memory=True)


def test_loss(TensorWriter, model, dataloader_test, epoch, total_step):
    total_test_step = 0
    test_loss = 0
    for step, batch_test in enumerate(dataloader_test):
        # print(batch_s_a, batch_s_s, batch_a)
        batch_test =  batch_test.cuda()
        ls = model.loss(batch_test[:, 0:input_dims], batch_test[:, input_dims: input_dims + 2])
        test_loss += ls.cpu().data.numpy()

        total_test_step += 1

    TensorWriter.add_scalar('loss/test', test_loss/total_test_step, total_step)
    print('epoch:{}  total_step:{} test loss:{:.7f}'.format(epoch, total_step, test_loss/total_test_step))


for epoch in range(10):

    # if epoch == 2:
    #     test(model, train_sets)

    for step, batch_train in enumerate(dataloader_train):
        # print(batch_s_a, batch_s_s, batch_a)

        if step%100000==0:
            test_loss(TensorWriter, model, dataloader_test, epoch, total_step)

        batch_train =  batch_train.cuda()

        model.zero_grad()
        #pi, nd = model(batch_train[:, 0:input_dims])
        #loss = mdn.mdn_loss(pi_x, pi_y, sigma_x, sigma_y, mu_x, mu_y, batch_train[:, input_dims:input_dims + 1],
        #                    batch_train[:, input_dims + 1:])
        ls = model.loss(batch_train[:, 0:input_dims], batch_train[:, input_dims: input_dims + 2])
        ls.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        optimizer.step()
        train_loss = ls.cpu().data.numpy()
        TensorWriter.add_scalar('loss/train', train_loss, total_step)
        total_step += 1
        print('epoch:{}  total_step:{} train loss:{:.7f}'.format(epoch, total_step, train_loss))


    if epoch % 1 == 0:
        torch.save(model.state_dict(),
                   './model'
                   '/model_{}.pth'.format(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))








