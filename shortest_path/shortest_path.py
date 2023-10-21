import sys

import networkx as nx
import matplotlib.pyplot as plt
import random


def draw(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='w')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()


def find_isolated_nodes(G):
    isolated_nodes = []
    for node in G.nodes():
        if not list(G.neighbors(node)):
            isolated_nodes.append(node)
    return isolated_nodes


def find_longest_edge(G):
    max_weight = -1
    max_edge = None
    for edge in G.edges(data=True):
        if edge[2]['weight'] > max_weight:
            max_edge = edge
            max_weight = edge[2]['weight']
    return max_edge


def find_shortest_path(G):
    G_empty = nx.Graph()
    G_empty.add_nodes_from(G)
    find_isolated_nodes(G_empty)

    min_weight = sys.maxsize
    min_edge = None
    for edge in G.edges(data=True):
        if edge[2]['weight'] < min_weight:
            min_edge = edge
            min_weight = edge[2]['weight']
    G_empty.add_weighted_edges_from([(min_edge[0], min_edge[1], min_edge[2]['weight'])])
    draw(G_empty)
    isolated_nodes = find_isolated_nodes(G_empty)

    while len(isolated_nodes) > 0:
        min_weight = sys.maxsize
        min_edge = None
        for isolated_node in isolated_nodes:
            for some_node in G.nodes():
                if some_node not in isolated_nodes:
                    edge_data = G.get_edge_data(isolated_node, some_node)
                    if edge_data is not None and edge_data['weight'] < min_weight:
                        min_weight = edge_data['weight']
                        min_edge = (isolated_node, some_node, min_weight)
        if min_edge is None:
            continue
        G_empty.add_weighted_edges_from([(min_edge[0], min_edge[1], min_edge[2])])
        isolated_nodes.remove(min_edge[0])
        draw(G_empty)

    divide_into_clusters(G_empty)


def divide_into_clusters(G_empty):
    k = 3
    for i in range(k - 1):
        max_edge = find_longest_edge(G_empty)
        G_empty.remove_edges_from([max_edge])
        draw(G_empty)


if __name__ == '__main__':
    G = nx.Graph()
    n = 5
    nodes = range(n)
    G.add_nodes_from(nodes)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.randint(0, 1) == 1:
                edges.append((i, j, random.randint(1, 10)))
    G.add_weighted_edges_from(edges)
    edges_with_values = {}
    for edge in edges:
        edges_with_values[(edge[0], edge[1])] = edge[2]
    draw(G)
    find_shortest_path(G)
