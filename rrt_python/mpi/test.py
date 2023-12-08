from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


class node():
    """
    Node class for dijkstra search
    """

    def __init__(self, x, y, index=-1,cost=-1, parent_index=-1):
        self.x = x
        self.y = y
        self.index = index
        self.cost = cost # 每条边权值
        self.parent_index = parent_index

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," +\
            str(self.cost) + "," + str(self.parent_index)

# class neibornode():#获取相邻区域中的点
#     def __init__(self,node,index_in_neighbor):
#         self.x = node.x
#         self.y = node.y
#         self.index = node.index
#         self.cost = node.cost  # 每条边权值
#         self.parent_index = node.parent_index
#         self.index_in_neighbor = index_in_neighbor
#         self.child_index = None
#         self.child_distance = -1

# class neighbor_in_me():
#     def __init__(self,myrank,neighborrank,prm,range):
#         self.myrank = myrank
#         self.neiborank = neighborrank
#         self.node_in_me = []
#         self.get_nodes(prm,range)
#     def get_nodes(self,prm,range):
#         for node in prm.nodes:
#             if node.x>= range[0] and node.x <= range[1]:
#                 node_in_neighbor = neibornode(node,len(self.node_in_me))
#                 self.node_in_me.append(node_in_neighbor)
#
#     def show(self):
#         plt.figure()
#         for i in range(len(self.node_in_me)):
#             plt.scatter(self.node_in_me[i].x, self.node_in_me[i].y, c='b')
#
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         plt.title('neigborspace')

# class neighbor_to_you():
#     def __init__(self,neighbor_in_me):
#         self.myrank = neighbor_in_me.myrank
#         self.neiborank = neighbor_in_me.neiborank
#         self.node_in_me = []
#         self.nodes(prm,range)
#     def local_to_global(self,neighbor_in_me):
#         for node in neighbor_in_me.node_in_me:
#             global_node = node.
#             self.node_in_me.append(global_node)
# class neighbor_connect():
#     def __init__(self,neighbor_in_me,neighbor_in_you):
#         self.find_child_index(neighbor_in_me,neighbor_in_you)
#     def find_nearest_neighbors(self,nodes, query_node, num_neighbors):
#         query_point = [query_node.x,query_node.y]
#         distances = [np.linalg.norm(np.array(query_point) - np.array([node.x,node.y])) for node in nodes]
#         sorted_indices = np.argsort(distances)
#         return sorted_indices[:num_neighbors]
#     def find_child_index(self,neighbor_in_me,neighbor_in_you):
#         for node in neighbor_in_me.node_in_me:
#             child_ids= self.find_nearest_neighbors(neighbor_in_you.node_in_me,node,num_neighbors=2)
#             node.child_index = child_ids[0]
#             node.child_distance = np.linalg.norm(np.array([node.x,node.y])
#                                                  - np.array([neighbor_in_you.node_in_me[node.child_index].x,
#                                                                                        neighbor_in_you.node_in_me[node.child_index].y]))
#
#     def show(self,neighbor_in_me,neighbor_in_you):
#         plt.figure()
#         for node in neighbor_in_me.node_in_me:
#             plt.scatter(node.x, node.y, c='b')
#             neighbor_node = neighbor_in_you.node_in_me[node.child_index]
#             plt.scatter(neighbor_node.x,neighbor_node.y,c = 'b')
#             plt.plot([node.x, neighbor_node.x], [node.y, neighbor_node.y], c='k', alpha=0.3)
#
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         plt.title('neigborspace')

class prm(object):
    def __init__(self, start,end,numsample=100,num_neighbors = 5, xlim=[-15,15], ylim=[-15,15],obstacles =None):
        """ 随机路线图算法(Probabilistic Roadmap, PRM)
        **param: 关键字参数，用以配置规划参数
                start: 起点坐标 (x,y)
                end: 终点左边 (x,y)
                num_sample: 采样点个数，默认100 int
                distance_neighbor: 邻域距离，默认100 float
        """
        self.start = start
        self.end =end
        self.num_sample = numsample
        self.num_neighbors = num_neighbors
        self.obstacles = obstacles
        self.xlim = xlim
        self.ylim = ylim
        self.nodes = self.generate_prm_points(self.num_sample,self.xlim,self.ylim,obstacles)
        self.distance_matrix = np.zeros([len(self.nodes),len(self.nodes)])
    def in_obstacle(self, point1, obstacles):
        return False

    def generate_prm_points(self, num_points, xlim, ylim, obstacles):
        prm_points = []
        while len(prm_points) < num_points:
            x = np.random.uniform(xlim[0], xlim[1])
            y = np.random.uniform(ylim[0], ylim[1])

            if not self.in_obstacle([x,y],obstacles):
                random_node = node(x,y,len(prm_points))
                prm_points.append(random_node)
        return prm_points

    def find_nearest_neighbors(self,nodes, query_node, num_neighbors):
        query_point = [query_node.x,query_node.y]
        distances = [np.linalg.norm(np.array(query_point) - np.array([node.x,node.y])) for node in nodes]
        sorted_indices = np.argsort(distances)
        return sorted_indices[:num_neighbors]

    def get_distance_matrix(self):
        for i in range(len(self.nodes)):
            indexs = self.find_nearest_neighbors(self.nodes,self.nodes[i],self.num_neighbors)
            for j in range(len(indexs)):
                self.distance_matrix[i][indexs[j]] = np.linalg.norm(np.array([self.nodes[i].x,self.nodes[i].y]) - np.array([self.nodes[indexs[j]].x,self.nodes[indexs[j]].y]))
                self.distance_matrix[indexs[j]][i] = self.distance_matrix[i][indexs[j]]

    def prm_algorithm(self):
        plt.figure()
        for i in range(len(self.nodes)):
            plt.scatter(self.nodes[i].x, self.nodes[i].y, c='b')
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.end[0], self.end[1], c='r', marker='s')

        self.get_distance_matrix()
        # print((self.distance_matrix))
        for i in range(len(self.nodes)-1):
            for j in range(i+1,len(self.nodes)):
                if self.distance_matrix[i][j] > 0:
                    plt.plot([self.nodes[i].x, self.nodes[j].x], [self.nodes[i].y, self.nodes[j].y], c='k', alpha=0.3)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Probabilistic Roadmap')
        # plt.show()


class prm_merge():
    def __init__(self,prms):
        self.nodes = []
        self.start = prms[0].start
        self.end = prms[0].end
        self.each_num_sample = prms[0].num_sample
        self.num_neighbors = prms[0].num_neighbors
        self.obstacles = obstacles
        self.merge_nodes(prms)
        self.distance_matrix = np.zeros([len(self.nodes), len(self.nodes)])
    def merge_nodes(self,prms):
        for i in range(len(prms)):
            self.nodes = self.nodes + prms[i].nodes

    def show_own_nodes(self):
        plt.figure()
        for i in range(self.each_num_sample * rank,self.each_num_sample * (rank + 1)):
            plt.scatter(self.nodes[i].x, self.nodes[i].y, c='b')
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.end[0], self.end[1], c='r', marker='s')

        self.get_distance_matrix()
        # print((self.distance_matrix))
        for i in range(len(self.nodes) - 1):
            for j in range(i + 1, len(self.nodes)):
                if self.distance_matrix[i][j] > 0:
                    plt.plot([self.nodes[i].x, self.nodes[j].x], [self.nodes[i].y, self.nodes[j].y], c='k', alpha=0.3)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Probabilistic Roadmap')
    def find_nearest_neighbors(self,nodes, query_node, num_neighbors):
        query_point = [query_node.x,query_node.y]
        distances = [np.linalg.norm(np.array(query_point) - np.array([node.x,node.y])) for node in nodes]
        sorted_indices = np.argsort(distances)
        return sorted_indices[:num_neighbors]

    def get_distance_matrix(self):
        for i in range(len(self.nodes)):
            indexs = self.find_nearest_neighbors(self.nodes,self.nodes[i],self.num_neighbors)
            for j in range(len(indexs)):
                self.distance_matrix[i][indexs[j]] = np.linalg.norm(np.array([self.nodes[i].x,self.nodes[i].y]) - np.array([self.nodes[indexs[j]].x,self.nodes[indexs[j]].y]))
                self.distance_matrix[indexs[j]][i] = self.distance_matrix[i][indexs[j]]

    def prm_algorithm(self):
        plt.figure()
        for i in range(len(self.nodes)):
            plt.scatter(self.nodes[i].x, self.nodes[i].y, c='b')
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.end[0], self.end[1], c='r', marker='s')

        self.get_distance_matrix()
        # print((self.distance_matrix))
        for i in range(len(self.nodes)-1):
            for j in range(i+1,len(self.nodes)):
                if self.distance_matrix[i][j] > 0:
                    plt.plot([self.nodes[i].x, self.nodes[j].x], [self.nodes[i].y, self.nodes[j].y], c='k', alpha=0.3)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Probabilistic Roadmap')
        # plt.show()
# 设置参数并运行PRM算法
start = (0, 0)
goal = (10, 10)
num_prm_points = 100
num_neighbors = 5
xlim = [-15 + rank*20, 15 + rank *20]
ylim = [-15 + rank*20, 15 + rank*20]

obstacles = None

workspace = prm(start, goal, num_prm_points, num_neighbors, xlim, ylim, obstacles)


prms = comm.gather(workspace,root=0)

if(rank == 0):
    a = prm_merge(prms)
    a.show_own_nodes()
plt.show()