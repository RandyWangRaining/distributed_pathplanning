import polygon_prm as PM
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
# 创建节点
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

#定义每个点的范围
interval = [15,15]
start = (0, 0)
goal = (50, 50)
center = [15 *rank , 15 *rank]
xlim = [-15 + rank*interval[0], 15 + rank *interval[1]]
ylim = [-15 + rank*interval[0], 15 + rank *interval[1]]

# 生成每个节点内障碍物
obstacle_list = [
        (5 + interval[0] * rank, 0 + interval[1] * rank, 5),
        (-5 + interval[0] * rank, 5 + interval[1] * rank, 5),
        (-5 +interval[0] * rank,-5 + interval[1] * rank,5)
    ]


workspace = PM.PRM(start, goal, center ,obstacle_list=obstacle_list,xlim = xlim,ylim = ylim) #创建多边形类

prms = comm.gather(workspace,root=0)

if(rank == 0):
    a = PM.PRM_merge(prms)
    # a.draw_edge()
    # a.draw_edge
    a.planning()