import polygon_prm as PM
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
# 创建智能节点
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

print("My rank is",rank)


interval = [15,15]    #定义滑动窗口的大小
start = (50, 50)
goal = (50, 50)
center = [15 *rank , 15 *rank]

xlim = [-15 + rank*interval[0], 15 + rank *interval[1]]    #定义滑动窗口的边界
ylim = [-15 + rank*interval[0], 15 + rank *interval[1]]


map_obstacle=[]
for i in range(8):
    for j in range(8):
        obstacle=(15*i-5,15*j-5,5)
        map_obstacle.append(obstacle)


#生成每个节点内障碍物
# obstacle_list = [
#         (5 + interval[0] * rank, 0 + interval[1] * rank, 5),
#         (-5 + interval[0] * rank, 5 + interval[1] * rank, 5),
#         (-5 +interval[0] * rank,-5 + interval[1] * rank,5)
#     ]
def isIn_window(obstacle,xlim,ylim):
    if(obstacle[0]<xlim[0] or obstacle[0]>xlim[1]):
        return 0
    elif(obstacle[1]<ylim[0] or obstacle[1]>ylim[1]):
        return 0    
    else:
        return 1
    
def get_obstacle(map_obstacle,xlim,ylim):
    obstacle_list=[]
    for obstacle in map_obstacle:
            if(isIn_window(obstacle,xlim,ylim)==1 and len(obstacle_list)<5):           
                obstacle_list.append(obstacle)    
    return obstacle_list
    
xlim[0]=xlim[0]+20
xlim[1]=xlim[1]+20
ylim[0]=ylim[0]+20
ylim[1]=ylim[1]+20
obstacle_list=get_obstacle(map_obstacle,xlim,ylim)





workspace = PM.PRM(start, goal, center ,obstacle_list=obstacle_list,xlim = xlim,ylim = ylim) #创建多边形类

# xlim = [-15 + rank*interval[0], 15 + rank *interval[1]]-15
# ylim = [-15 + rank*interval[0], 15 + rank *interval[1]]-15
# workspace = PM.PRM(start, goal, center ,obstacle_list=obstacle_list,xlim = xlim,ylim = ylim) #创建多边形类

prms = comm.gather(workspace,root=0)
# if(rank == 0):         #合并所有的多边形
#     a = PM.PRM_merge(prms)
# if(rank==1 or rank==0):
#     ylim[0]=ylim[0]+20
#     ylim[1]=ylim[1]+20
# #     ylim[0]=ylim[0]+10
# #     ylim[1]=ylim[1]+10
#     obstacle_list=get_obstacle(xlim,ylim)    
#     workspace = PM.PRM(start, goal, center ,obstacle_list=obstacle_list,xlim = xlim,ylim = ylim) #创建多边形类
# prms = comm.gather(workspace,root=0)

if(rank == 0):         #合并所有的多边形
    a = PM.PRM_merge(prms)
    # a.draw_edge()
    # a.draw_edge
    a.planning()       #进行规划



#滑动窗口的定义

#prm的图建立,prm和rrt如何结合

#分布式消息传递一起见图
