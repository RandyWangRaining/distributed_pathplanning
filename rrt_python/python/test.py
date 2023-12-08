import irispy
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

# A simple example with only one obstacle:

obstacles = [np.array([[2., 0], [2, 2], [3, 2], [3, 0],[2., 0]]).T,
             np.array([[-1., 0], [-1, 2], [0, 2], [0.2, 0],[-1., 0]]).T]
bounds = irispy.Polyhedron.fromBounds([-1, -1], [3, 3])
seed_point = np.array([-0.5,1.5])
region = irispy.inflate_region(obstacles, seed_point, bounds)


# def listarray2array(GeneratePoints):
points = region.getPolyhedron().getDrawingVertices()
hull = ConvexHull(points)
points = points[hull.vertices]
print(points)
points = np.insert(points,len(points),points[0],axis=0)
print(points)
# points.append(points[0])
# region = np.array(region.getPolyhedron().generatorPoints())




# Draw the boundary and obstacles:
plt.figure()
for obstacle in obstacles:
    plt.plot(obstacle[0],obstacle[1])
plt.plot(points[:,0],points[:,1])
plt.show()
