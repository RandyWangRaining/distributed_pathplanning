import matplotlib.pyplot as plt
import random
import math
import copy
import numpy as np
from polygon import *
import sys
sys.path.append('/home/kemove/2023/month_10/rrt_python/mdn4')
import gen_obs28
import pridict
class PolygonNode(myPolygon):
    """
    RRT Node
    """
    def __init__(self, vertices,index=-100):
        super(PolygonNode, self).__init__(vertices)
        self.index = index
        self.parent = None
    def GeneratePN(point,index=-100):
        polygon = myPolygon.Rect(point,[1,1])
        return PolygonNode(polygon.vertices,index)

class PolygonEdge(myPolygon):
    """
    RRT Node
    """
    def __init__(self, vertices , index=-100):
        super(PolygonEdge, self).__init__(vertices)
        self.index = index
        self.nodes = []
    def GeneratePE(point,index):
        polygon = myPolygon.Rect(point,[5,5])
        return PolygonEdge(polygon.vertices,index)



class RRT(object):
    def __init__(self, start, goal, obstacle_list, rand_area):
        """
        Setting Parameter
        start:Start Position [x,y]
        goal:Goal Position [x,y]
        obstacleList:obstacle Positions [[x,y,size],...]
        randArea:random sampling Area [min,max]
        """
        self.start = start
        self.end = goal
        self.nodenum = 0
        self.edgenum = 0
        self.startnode = PolygonNode.GeneratePN(start,self.nodenum)
        self.startedge = PolygonEdge.GeneratePE(start,self.edgenum)
        self.startnode.parent = -1
        self.endedge = PolygonEdge.GeneratePE(goal, -1)
        self.endnode = PolygonNode.GeneratePN(goal, -1)
        self.startedge.nodes.append(self.nodenum)
        self.min_rand = rand_area[0]
        self.max_rand = rand_area[1]
        self.maxIter = 100
        self.obstacleList = obstacle_list
        self.nodeList = [self.startnode]
        self.edgeList = [self.startedge]
        self.nodenum += 1
        self.edgenum += 1

    def data42(self,polygon,goal):
        obstacle7x2 = np.array(self.obstacleList)[:,0:2]
        print(obstacle7x2)
        obstacle28 = np.array( gen_obs28.gen_obs28(0,obstacle7x2)).reshape(-1)
        polygon6x2 = np.array(polygon.vertice6()).reshape(-1)
        #合并
        data40 = np.append(obstacle28,polygon6x2)
        data42 = np.append(data40,np.array(goal))

        return data42



    def random_poly_edge(self):
        point_x = random.uniform(self.min_rand, self.max_rand)
        point_y = random.uniform(self.min_rand, self.max_rand)
        point = [point_x, point_y]
        rpe = PolygonEdge.GeneratePE(point,self.edgenum)
        return rpe
    def Pointdistance(self,nodea,nodeb):
        return math.sqrt((nodea[0]-nodeb[0])**2 +(nodea[1]-nodeb[1])**2)

    def neuro_poly_edge(self):
        random_index = np.argmin([self.Pointdistance(self.end,node.center) for node in self.edgeList])
        print((random_index))
        data42 = self.data42(self.edgeList[random_index], goal=self.end)
        neuro_point = pridict.pridict(data42)
        print(neuro_point)
        rpe = PolygonEdge.GeneratePE(neuro_point, self.edgenum)
        plt.cla()
        rpe.show_polygon()

        for (ox, oy, size) in self.obstacleList:
            plt.plot(ox, oy, "sk", ms=10 * size)

        plt.plot(self.start[0], self.start[1], "^r")
        plt.plot(self.end[0], self.end[1], "^g")
        plt.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand])
        plt.grid(True)
        plt.pause(1)
        return  rpe

    def checkpoly(self,polygon):
        if polygon.polygonarea()>0.1:
            return 1
        return 0
    def get_polynode(self, random_poly_edge):
        if_connected = False
        for polyedge in self.edgeList:
            interpoly =  myPolygon.inter_poly(polyedge,random_poly_edge)
            if interpoly and self.checkpoly(interpoly):
                if_connected = True
                d_list = [(self.nodeList[node_index].center[0] - interpoly.center[0]) ** 2
                          + (self.nodeList[node_index].center[0] - interpoly.center[0]) ** 2
                          for node_index in polyedge.nodes]

                min_index = polyedge.nodes[d_list.index(min(d_list))]
                new_poly_node = PolygonNode(interpoly.vertices,self.nodenum)
                new_poly_node.parent = min_index
                self.nodeList.append(new_poly_node)
                random_poly_edge.nodes.append(self.nodenum)
                polyedge.nodes.append(self.nodenum)
                self.nodenum += 1
        if if_connected:
            self.edgeList.append(random_poly_edge)
            self.edgenum += 1
        return

    def collision_check(self,newPolygonEdge):
        a = 1
        for (ox, oy, size) in self.obstacleList:
            obstacle_polygon = myPolygon.Rect([ox,oy],[size,size])
            if myPolygon.inter_poly(newPolygonEdge,obstacle_polygon):
                a = 0  # collision
        return a  # safe

    def planning(self):
        """
        Path planning
        animation: flag for animation on or off
        """

        while self.maxIter:
            # Random Sampling
            randompoly = self.neuro_poly_edge()


            if not self.collision_check(randompoly):
                continue
            else:
                self.get_polynode(randompoly)

            # check goal
            if myPolygon.inter_poly(self.edgeList[-1],self.endedge):
                self.get_polynode(self.endedge)
                print("Goal")
                break


            if True:
                self.maxIter -= 1
                print(self.maxIter)
                self.draw_graph()

        path = [self.endnode,self.nodeList[-1]]
        last_index = len(self.nodeList) - 1
        while self.nodeList[last_index].parent != -1:
            node = self.nodeList[last_index]
            path.append(node)
            last_index = node.parent

        return path

    def draw_graph(self):
        """
        Draw Graph
        """
        print('draw')
        plt.clf()  # 清除上次画的图
        for edge in self.edgeList:
            edge.show_polygon()

        for (ox, oy, size) in self.obstacleList:
            plt.plot(ox, oy, "sk", ms=10 * size)

        plt.plot(self.start[0], self.start[1], "^r")
        plt.plot(self.end[0], self.end[1], "^g")
        plt.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand])
        plt.grid(True)
        plt.pause(0.01)

    def draw_static(self, path):
        """
        画出静态图像
        :return:
        """
        plt.clf()  # 清除上次画的图

        # for edge in self.edgeList:
        #     edge.show_polygon()

        for (ox, oy, size) in self.obstacleList:
            plt.plot(ox, oy, "sk", ms=10 * size)

        plt.plot(self.start[0], self.start[1], "^r")
        plt.plot(self.end[0], self.end[1], "^b")
        plt.axis([self.min_rand, self.max_rand, self.min_rand, self.max_rand])

        for node in path[1:-1]:
            node.show_polygon()
            line_X = [node.center[0],self.nodeList[node.parent].center[0]]
            line_Y = [node.center[1], self.nodeList[node.parent].center[1]]
            plt.plot(line_X,line_Y)
        for node in self.nodeList[1:-1]:
            node.show_polygon()
            line_X = [node.center[0],self.nodeList[node.parent].center[0]]
            line_Y = [node.center[1], self.nodeList[node.parent].center[1]]
            plt.plot(line_X,line_Y)

        plt.grid(True)
        plt.show()
def main():
    # print("start RRT path planning")

    obstacle_list = [
        (5, -10, 5),
        (-10, 10, 5),
        (-5, -5, 5),
        (12, -10, 5),
        (10, 10, 5),
        (-5, -10, 5),
        (5, -5, 5)
    ]

    # Set Initial parameters
    rrt = RRT(start=[0, 5], goal=[10,5], rand_area=[-15, 15], obstacle_list=obstacle_list)

    path = rrt.planning()

    # Draw final path
    print('draw')



    if 1:
        plt.close()
        rrt.draw_static(path)

if __name__ == '__main__':
    main()