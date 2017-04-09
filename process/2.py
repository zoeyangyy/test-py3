# # coding = utf-8
# from pylab import *
# import networkx as nx
# # import matplotlib.font_manager as mf
# # myfont = mf.FontProperties(fname='/Users/zoe/msyh.ttf')
#
# g=nx.Graph()
# g.add_edge('春天','b')
# g.add_edge('a','c')
# pos=nx.spring_layout(g)
# nx.draw_networkx_nodes(g, pos)
# nx.draw_networkx_edges(g, pos)
# nx.draw_networkx_labels(g, pos)
# plt.show()
#
# print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

# -*- coding: utf-8 -*-
from pylab import *
import matplotlib.font_manager as mf
# myfont = mf.FontProperties(fname='/Users/zoe/msyh.ttf')
mpl.rcParams['axes.unicode_minus'] = False
# matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']

t = arange(-5*pi, 5*pi, 0.01)
y = sin(t)/t
plt.plot(t, y)
plt.title('这里写的是中文') #指定字体  fontproperties=myfont
plt.xlabel('X坐标')
plt.ylabel('Y坐标')
plt.show()

# import matplotlib.font_manager as mf
#
# print(sorted([f.name for f in mf.fontManager.ttflist]))
