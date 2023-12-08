import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon,Point

class myPolygon(object):
    # 根据外点生成多边形
    def __init__(self,vertices):
        self.vertices = vertices
        vertices2array = np.array(self.vertices).reshape([-1,2])
        self.center = [np.mean(vertices2array[:, 0]), np.mean(vertices2array[:, 1])]

    def Rect(center ,size ):
        return myPolygon(myRect(center,size).vertices)

    #生成相交凸多边形
    def inter_poly(polygona,polygonb):
        if not myPolygon.is_intersect(polygona,polygonb):
            return
        else :
            polya = Polygon(polygona.vertices)
            polyb = Polygon(polygonb.vertices)
            isIntersection = polya.intersection(polyb)
            inter_poly = myPolygon([[vertice[0],vertice[1]] for vertice in list(isIntersection.exterior.coords)][0:-1])
            # print(isIntersection)
            return inter_poly

    #判断多边形是否包含在另一个中
    def is_intersect(polygona,polygonb):
        polya = Polygon(polygona.vertices)
        polyb = Polygon(polygonb.vertices)
        isIntersects = polya.intersection(polyb)
        if isIntersects:
            return True
        else:
            return False
    #计算面积
    def polygonarea(self):
        polygon = Polygon(self.vertices)
        return polygon.area

    # 画图
    def show_polygon(self):
        vertices = self.vertices.copy()
        vertices2array = np.array(vertices)
        vertices2array = np.insert(vertices2array,len(vertices2array),vertices2array[0],axis=0)
        plt.plot(vertices2array[:,0],vertices2array[:,1],"b")
    def txt_polygon(self):
        print(self.vertices)

    # 找多边形的六个顶点
    def vertice6(self):
        if len(self.vertices)>=6:
            return self.vertices[0:6]
        elif len(self.vertices) < 6:
            # i = 0
            vertice6 = self.vertices.copy()
            while len(vertice6) < 6:
                #vertice6.append(vertice6[len(self.vertices)-1])
                vertice6 = np.concatenate((vertice6, [vertice6[len(self.vertices)-1]]))
            return vertice6
    #判断点是否在多边形内
    def point_inside_polygon(point,polygon_vertices):
        point = Point(point[0], point[1])
        polygon = Polygon(polygon_vertices)
        return polygon.contains(point)
class myRect(object):
    """
    RRT sample polygon
    """
    def __init__(self, center ,size = [1,1]):
        self.center = center
        self.size = size
        self.vertices = []
        self.vertices.append([center[0] - size[0] / 2, center[1] - size[1] / 2])
        self.vertices.append([center[0] + size[0] / 2, center[1] - size[1] / 2])
        self.vertices.append([center[0] + size[0] / 2, center[1] + size[1] / 2])
        self.vertices.append([center[0] - size[0] / 2, center[1] + size[1] / 2])

def main():
    obstacle = [[0, 0], [4, 0], [4, 4], [0, 4]]
    # 要判断的点
    point_to_check = (2, 2)

    # 判断点是否在多边形内部
    is_inside = myPolygon.point_inside_polygon(point_to_check,obstacle)

    if is_inside:
        print("点在多边形内部")
    else:
        print("点不在多边形内部")
if __name__ == '__main__':
    main()