import irispy
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

# A simple example with only one obstacle:

obstacles = [np.array([[2., 0], [3,0], [3, 2], [2, 2],[2,0]]).T,
             np.array([[-1., 0], [-1, 2], [0, 2], [0.2, 0]]).T,
             np.array([[0.5, 2]]).T]
bounds = irispy.Polyhedron.fromBounds([-1, -1], [3, 3])
seed_point = np.array([1.0, 2.0])
region = irispy.inflate_region(obstacles, seed_point, bounds)


# def listarray2array(GeneratePoints):
points = region.getPolyhedron().getDrawingVertices()
print(points)
hull = ConvexHull(points)
points = points[hull.vertices]
# region = np.array(region.getPolyhedron().generatorPoints())




# Draw the boundary and obstacles:
plt.figure()
plt.plot(obstacles[0][0],obstacles[0][1])
plt.plot(points[:,0],points[:,1])
plt.show()
