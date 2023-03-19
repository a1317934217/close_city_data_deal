# coding:utf-8
"""
@file: test_file.py
@author: wu hao
@time: 2023/3/11 20:02
@env: 封城数据处理
@desc:
@ref:
"""
from math import e
from math import log
from networkx.algorithms.connectivity import minimum_st_node_cut, minimum_node_cut
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.flow import shortest_augmenting_path
from networkx.algorithms.connectivity import minimum_st_node_cut

from networkx.algorithms.connectivity import local_edge_connectivity
from networkx.algorithms.connectivity import local_node_connectivity
import networkx as nx
import matplotlib.pyplot as plt
from networkx import laplacian_matrix
from numpy import array
import numpy as np
from networkx.algorithms import approximation as approx
from networkx.algorithms.connectivity import minimum_st_node_cut
import  pandas as pd
G = nx.Graph()
G1 = nx.Graph()
G.add_node("A",desc="A")
G.add_node("B",desc="B")
G.add_node("C",desc="C")
G.add_node("D",desc="D")
G.add_node("E",desc="E")
G.add_node("F",desc="F")
# G.add_node("G",desc="G")
G.add_edges_from([("A","B") ,("A" ,"C") ,("A" ,"D") ,("A" ,"E"),("B" ,"C"),("B","D")
                  ,("B" ,"E"),("D" ,"C"),("E" ,"C"),("D" ,"E"),("F" ,"A"),("F" ,"B")
                     ,("F" ,"C")])


# G1.add_node("A",desc="A")
# G1.add_node("B",desc="B")
# G1.add_node("C",desc="C")
# G1.add_node("D",desc="D")
# G1.add_node("E",desc="E")
# # G.add_node("F",desc="F")
# # G.add_node("G",desc="G") ,("B" ,"D")
# G1.add_edges_from([("A","B") ,("A" ,"D") ,("C" ,"B") ,("C" ,"D")])

pos = nx.circular_layout(G)
nx.draw(G,pos)
mode_labels = nx.get_node_attributes(G,'desc')
nx.draw_networkx_nodes(G,pos,label=mode_labels)
plt.show()







