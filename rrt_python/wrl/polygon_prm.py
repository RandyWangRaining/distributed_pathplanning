import matplotlib.pyplot as plt
import random
random.seed(1036)
import math
import copy
import numpy as np
from scipy.spatial import ConvexHull
from polygon import *
from python import irispy
import sys
sys.path.append('/home/hfy/distributed_planning/rrt_python/mdn4')
import gen_obs28
import pridict
class PolygonNode(myPolygon): #G（V，E）的V
    """
    PRM Node
    """
    def __init__(self, vertices,index=-100):
        super(PolygonNode, self).__init__(vertices)
        self.index = index
        self.edgeindex = [] #记录两条边
        self.parent = -1
    # def GeneratePN(point,index=-100):
    #     polygon = myPolygon.Rect(point,[1,1])
    #     return PolygonNode(polygon.vertices,index)

class PolygonEdge(myPolygon):#G（V，E）的E
    """
    RRT Node
    """
    def __init__(self, vertices , index=-100):
        super(PolygonEdge, self).__init__(vertices)
        self.index = index
        self.nodes = []

class PRM(object):
    def __init__(self, start, goal, center,obstacle_list, xlim, ylim):

        self.start = start
        self.goal = goal
        self.center = center
        self.maxKNN =5 #同一个edge中太多vertex,仅连接最近的几个顶点
        self.maxIter = 10 #每次生成点最多预测次数
        self.xlim = xlim
        self.ylim = ylim
        self.obstacleList = obstacle_list #输入的obstacle形式
        self.obstacles = self.List2obstacles(self.obstacleList) #用于匹配irispy

        self.T_obstacles = [obstacle.T for obstacle in self.obstacles] #obstacle不同形式，用于检测障碍物

        self.nodeList = []
        self.edgeList = []
        self.distMatrix = None

        #判断起点终点是否在多边形内
        if start[0] >= xlim[0] and start[0]<= xlim[1] and start[1]>= ylim[0] and start[1] <= ylim[1]:
            start_edge = PolygonEdge(self.max_polygon(self.start,self.obstacles,self.xlim,self.ylim))
            self.edgeList.append(start_edge)
            self.edgeList.append(start_edge)
            print("start in region")
        if goal[0] >= xlim[0] and goal[0] <= xlim[1] and goal[1] >= ylim[0] and start[1] <= ylim[1]:
            goal_edge = PolygonEdge(self.max_polygon(self.goal, self.obstacles, self.xlim, self.ylim))
            self.edgeList.append(goal_edge)
            self.edgeList.append(goal_edge)
            print("goal in region")

        #通过圣经网络预测多边形
        self.all_edges_neuro()


    #判断点是否在多边形内或者障碍物内
    def if_point_feasible(self,point):
        for polygon in self.edgeList:
            if myPolygon.point_inside_polygon(point,polygon.vertices):
                return False
        for obstacle in self.T_obstacles:
            if myPolygon.point_inside_polygon(point,obstacle):
                return False
        return True

    #随机产生预测点
    def random_poly_edge(self):
        while True:
            point_x = random.uniform(self.xlim[0], self.xlim[1])
            point_y = random.uniform(self.ylim[0], self.ylim[1])
            point = [point_x,point_y]
            if self.if_point_feasible(point = point):
                regionvertices = self.max_polygon(point, self.obstacles, self.xlim, self.ylim)
                rpe = PolygonEdge(regionvertices)
                return rpe
                break
        return None

    #节点之间的距离
    def Pointdistance(self,nodea,nodeb):
        return math.sqrt((nodea[0]-nodeb[0])**2 +(nodea[1]-nodeb[1])**2)

    #产生四十二位的数据用于神经网络输入
    def data42(self,polygon,goal):
        obstacle7x2 = np.array(self.obstacleList)[:,0:2]
        obstacle7x2 = obstacle7x2 - self.center
        # print(obstacle7x2)
        obstacle28 = np.array( gen_obs28.gen_obs28(0,obstacle7x2)).reshape(-1)
        relative_vertice = np.array(polygon.vertice6()) - self.center
        polygon6x2 = np.array(relative_vertice).reshape(-1)
        #合并
        data40 = np.append(obstacle28,polygon6x2)
        data42 = np.append(data40,np.array(goal) - self.center)

        return data42

    #神经网络生成预测点
    def neuro_poly_edge(self):
        #如果没有初始边，以初始中心生成多边形
        if len(self.edgeList) == 0 :
            regionvertices = self.max_polygon(self.center, self.obstacles, self.xlim, self.ylim)
            rpe = PolygonEdge(regionvertices)
            return rpe
        else:
            # 不断分别向起点终点生成多边形预测点
            k = 0
            if k%2 == 0:
                random_index = np.argmin([self.Pointdistance(self.goal, node.center) for node in self.edgeList])
                data42 = self.data42(self.edgeList[random_index], goal=self.goal)
            else:
                random_index = np.argmin([self.Pointdistance(self.start, node.center) for node in self.edgeList])
                data42 = self.data42(self.edgeList[random_index], goal=self.start)
            #预测二十次可用点
            while k < 20:
                point = pridict.pridict(data42)
                point = np.array(point)
                point = point + self.center
                k = k + 1
                if self.if_point_feasible(point = point):
                    regionvertices = self.max_polygon(point, self.obstacles, self.xlim, self.ylim)
                    rpe = PolygonEdge(regionvertices)
                    return rpe
                if k % 2 == 0:
                    random_index = np.argmin([self.Pointdistance(self.goal, node.center) for node in self.edgeList])
                    data42 = self.data42(self.edgeList[random_index], goal=self.goal)
                else:
                    random_index = np.argmin([self.Pointdistance(self.goal, node.center) for node in self.edgeList])
                    data42 = self.data42(self.edgeList[random_index], goal=self.start)
        return None

    def List2obstacles(self,List):
        obstacles = []
        for i in range(len(List)):
            vertice1 = [List[i][0] - List[i][2] / 2, List[i][1] - List[i][2] / 2]
            vertice2 = [List[i][0] + List[i][2] / 2, List[i][1] - List[i][2] / 2]
            vertice3 = [List[i][0] + List[i][2] / 2, List[i][1] + List[i][2] / 2]
            vertice4 = [List[i][0] - List[i][2] / 2, List[i][1] + List[i][2] / 2]
            obstacle =[vertice1,vertice2,vertice3,vertice4]
            #为了符合irispy的格式，获得多边形凸优化
            obstacles.append(np.array(obstacle).T)
        return obstacles

    # irispy使用方法
    def max_polygon(self,point,obstacles,xlim,ylim):
        bounds = irispy.Polyhedron.fromBounds([xlim[0], ylim[0]], [xlim[1], ylim[1]])
        seed_point = np.array(point)
        region = irispy.inflate_region(obstacles, seed_point, bounds)

        regionvertices = region.getPolyhedron().getDrawingVertices()
        hull = ConvexHull(regionvertices)
        regionvertices = regionvertices[hull.vertices]
        return regionvertices

    def test_rpe(self):
        print('draw')
        plt.figure()
        for obstacle in self.obstacles:
            points = np.insert(obstacle, len(obstacle[0]), obstacle[:,0], axis=1)
            plt.plot(points[0],points[1])

        rpe = self.random_poly_edge()
        points = np.insert(rpe.vertices, len(rpe.vertices), rpe.vertices[0], axis=0)
        plt.plot(points[:,0], points[:,1])
        plt.axis([self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]])
        plt.grid(True)
        plt.show()


    #生成所有edge
    def all_edges_neuro(self):
        i = 0

        while(i < self.maxIter):
            rand_poly_edge = self.neuro_poly_edge()
            i = i+1
            if rand_poly_edge:
                self.edgeList.append(rand_poly_edge)

    def all_edges_offlines(self):
        i = 0
        while(i < self.maxIter):
            rand_poly_edge = self.random_poly_edge()
            i = i+1
            if rand_poly_edge:
                self.edgeList.append(rand_poly_edge)

#通过edge的交集产生节点
    def all_nodes_offlines(self):
        for a in range(len(self.edgeList) - 1):
            for b in range(a + 1, len(self.edgeList)):
                interpoly = myPolygon.inter_poly(self.edgeList[a], self.edgeList[b])
                if interpoly and self.checkpoly(interpoly):
                    new_poly_node = PolygonNode(interpoly.vertices, len(self.nodeList))
                    new_poly_node.edgeindex = [a,b]
                    self.nodeList.append(new_poly_node)
        self.distMatrix = np.zeros((len(self.nodeList),len(self.nodeList)))

#节点的面积需要大于一定值用于通过
    def checkpoly(self, polygon):
        if polygon.polygonarea() > 1:
            return 1
        return 0

    def collision_check(self,newPolygonEdge):
        a = 1
        for (ox, oy, size) in self.obstacleList:
            obstacle_polygon = myPolygon.Rect([ox,oy],[size,size])
            if myPolygon.inter_poly(newPolygonEdge,obstacle_polygon):
                a = 0  # collision
        return a  # safe

# 检查节点是否在同一edge中
    def commedge(self,nodea,nodeb):
        if nodea.edgeindex[0] == nodeb.edgeindex[0] or nodea.edgeindex[0] == nodeb.edgeindex[1] or nodea.edgeindex[1] == nodeb.edgeindex[0] or nodea.edgeindex[1] == nodeb.edgeindex[1]:
            return  1
        return 0
    def distance(self,nodea,nodeb):
        return math.sqrt((nodea.center[0]-nodeb.center[0])**2 +(nodea.center[1]-nodeb.center[1])**2)

    #生成临接矩阵
    def generate_map(self):
        for a in range(len(self.nodeList)-1):
            i = 0
            for b in range(a+1,len(self.nodeList)):
                if self.commedge(self.nodeList[a],self.nodeList[b]):
                    distanceab = self.distance(self.nodeList[a],self.nodeList[b])
                    if True:
                        self.distMatrix[a][b] = distanceab
                        self.distMatrix[b][a] = distanceab

    #生成树
    def dijkstra(self,start):
        n = len(self.distMatrix)
        distance = np.full(n, float('inf'))
        visited = np.zeros(n, dtype=bool)
        distance[start] = 0.1
        for _ in range(n):
            # Find the node with the minimum distance that is not visited
            index = -1
            dis = float('inf')
            for i in range(n):
                if not visited[i] and distance[i]<dis:
                    dis = distance[i]
                    index = i
            current = index

            # Mark the current node as visited
            visited[current] = True

            # Relax edges and update distances
            for neighbor in range(n):
                if not visited[neighbor] and self.distMatrix[current][neighbor] > 0:
                    new_distance = distance[current] + self.distMatrix[current][neighbor]
                    if new_distance<distance[neighbor]:
                        self.nodeList[neighbor].parent = current
                        distance[neighbor] = new_distance
        print([self.nodeList[nei].parent for nei in range(n) ] )
        return distance


    # 找到起点终点的序号
    def start_node_index(self):
        for i in range(len(self.nodeList)):
            if myPolygon.point_inside_polygon(self.start,self.nodeList[i].vertices):
                return i
    def goal_node_index(self):
        for i in range(len(self.nodeList)):
            if myPolygon.point_inside_polygon(self.goal,self.nodeList[i].vertices):
                return i

    #单独的规划
    def planning(self):
        """
        Path planning
        animation: flag for animation on or off
        """
        self.all_nodes_offlines()
        self.generate_map()
        start_index = self.start_node_index()
        self.dijkstra(start=start_index)
        self.draw_edge()
        self.draw_node()
        self.draw_path()

    #画图
    def draw_edge(self):
        plt.figure()
        for edge in self.edgeList:
            edge.show_polygon()

        for obstacle in self.obstacles:
            points = np.insert(obstacle, len(obstacle[0]), obstacle[:, 0], axis=1)
            plt.plot(points[0], points[1])
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.goal[0], self.goal[1], c='r', marker='s')
        plt.axis("auto")
        plt.grid(True)
        plt.pause(0.01)
        plt.show()

    def draw_node(self):
        plt.figure()
        for node in self.nodeList:
            node.show_polygon()
            if node.parent != -1:
                line_X = [node.center[0], self.nodeList[node.parent].center[0]]
                line_Y = [node.center[1], self.nodeList[node.parent].center[1]]
                plt.plot(line_X, line_Y)

        for obstacle in self.obstacles:
            points = np.insert(obstacle, len(obstacle[0]), obstacle[:, 0], axis=1)
            plt.plot(points[0], points[1])
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.goal[0], self.goal[1], c='r', marker='s')
        plt.axis("auto")
        plt.grid(True)
        plt.pause(0.01)
        plt.show()

    def draw_path(self):
        plt.figure()
        for obstacle in self.obstacles:
            points = np.insert(obstacle, len(obstacle[0]), obstacle[:, 0], axis=1)
            plt.plot(points[0], points[1])
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.goal[0], self.goal[1], c='r', marker='s')

        now_index = self.goal_node_index()
        print(now_index)
        parent_index = self.nodeList[now_index].parent
        while parent_index != -1:
            self.nodeList[now_index].show_polygon()
            line_X = [self.nodeList[now_index].center[0], self.nodeList[parent_index].center[0]]
            line_Y = [self.nodeList[now_index].center[1], self.nodeList[parent_index].center[1]]
            plt.plot(line_X, line_Y)
            now_index = parent_index
            parent_index = self.nodeList[now_index].parent

        self.nodeList[now_index].show_polygon()

        plt.axis("auto")
        plt.grid(True)
        plt.pause(0.01)
        plt.show()

    def draw_graph(self):

        print('draw')
        plt.clf()  # 清除上次画的图
        plt.scatter(self.start[0], self.start[1], c='g', marker='s')
        plt.scatter(self.goal[0], self.goal[1], c='r', marker='s')
        for node in self.nodeList[1:-1]:
            node.show_polygon()
            if (node.parent != -1):
                line_X = [node.center[0], self.nodeList[node.parent].center[0]]
                line_Y = [node.center[1], self.nodeList[node.parent].center[1]]
                plt.plot(line_X, line_Y)

        for obstacle in self.obstacles:
            points = np.insert(obstacle, len(obstacle[0]), obstacle[:, 0], axis=1)
            plt.plot(points[0], points[1])

        plt.axis("auto")
        plt.grid(True)
        plt.pause(0.01)
        plt.show()


# 合并多个prm
class PRM_merge(PRM):
    def __init__(self,prms):
        self.start = prms[0].start
        self.goal = prms[0].goal
        self.maxKNN = prms[0].maxKNN
        self.maxIter = prms[0].maxIter
        self.obstacleList = []
        self.nodeList = []
        self.edgeList = []
        # 合并障碍物和edge
        for i in range(len(prms)):
            self.obstacleList += prms[i].obstacleList
            self.edgeList += prms[i].edgeList
        self.obstacles = self.List2obstacles(self.obstacleList)
        self.distMatrix = None
    # def algorithm(self):
    #     self.all_nodes_offlines()
    #     self.generate_map()
    #     self.dijkstra(start=0)
    #     self.draw_graph()
def main():
    print("start PRM path planning")
    rank = 0
    center = [20 *rank,20*rank]
    obstacle_list = [
        (5 + 20 * rank, 0 + 20 * rank, 5),
        (-5 + 20 * rank, 5 + 20 * rank, 5),
        (-5 + 20 * rank,-5 + 20 * rank,5)
    ]
    xlim = [-15 + 20 * rank,15 + 20 * rank]
    ylim = [-15 + 20 * rank, 15 + 20 * rank]

    # Set Initial parameters
    prm = PRM(start=[0, 0], goal=[8, 9], center=center, obstacle_list=obstacle_list,xlim = xlim,ylim = ylim)
    path = prm.planning()

    # # Draw final path
    # if 1:
    #     plt.close()
    #     rrt.draw_static(path)


if __name__ == '__main__':
    main()