import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4])
G.add_node('first_node', time='5pm')

# G.add_edges_from([(1, 2), (2, 3), (1, 3)])
G.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)])

node_list = G.nodes()
print(G.edges())
print(G.node['first_node'])

nx.draw(G)
plt.show()
