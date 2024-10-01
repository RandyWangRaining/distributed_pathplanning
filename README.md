# distributed-planning
work for distributed planning
## iris-disro generate a .so file for rrt-python
you should install [iris-distro](https://github.com/rdeits/iris-distro) 
copy iris_wrapper.cpython-... form iris_distro_master/build/iris-build/cxx to rrt_python/python/irispy
## pybind11 and openmpi is bag for work
```
python rrt.py
```

<p align = "center">
<img src="test.gif" width = "640" height = "438" border="5" />
</p>


# distributed-planning
work for distributed planning
iris-disro generate a .so file for rrt-python
pybind11 and openmpi is bag for work

# 安装openmpi

# 安装iris-disro generate
参考 https://github.com/rdeits/iris-distro
下面的三个文件夹中有些可以在该界面找一下
## 首先安装mosek
需要注册学生账号，免费的
Ubuntu 20.04 下 MOSEK 9.3 的安装
## 安装pybind11
## 安装eigen3
可以pip安装
## 最后
将iris-distro build的文件中有一个irisbuild/cxx/iris_wrapper.cpython-38-x86_64-linux-gnu.so文件替换调rrt_python中python文件，可以直接运行rrt_python中rrt.py 
