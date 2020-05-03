import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    best_tree = minimum_spanning_tree(G)
    best_avg = average_pairwise_distance(best_tree)
    for i in range(1000):
        tree = minimum_spanning_tree(G)
        new_g = remove_bad_leaves(tree)
        if average_pairwise_distance(new_g) < best_avg:
            best_tree = tree
            best_avg = average_pairwise_distance(new_g)
    return best_tree

def minimum_spanning_edges(G, weight='weight', data=True):
    """

    Examples
    --------
    >>> G=nx.cycle_graph(4)
    >>> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >>> mst=nx.minimum_spanning_edges(G,data=False) # a generator of MST edges
    >>> edgelist=list(mst) # make a list of the edges
    >>> print(sorted(edgelist))
    [(0, 1), (1, 2), (2, 3)]

    Notes
    -----
    Uses Kruskal's algorithm.

    If the graph edges do not have a weight attribute a default weight of 1
    will be used.

    Modified code from David Eppstein, April 2006
    http://www.ics.uci.edu/~eppstein/PADS/
    """
    from networkx.utils import UnionFind
    if G.is_directed():
        raise nx.NetworkXError(
            "Mimimum spanning tree not defined for directed graphs.")

    subtrees = UnionFind()
    edges = sorted(G.edges(data=True), key=lambda t: t[2].get(weight, 1))
    probability = 99
    for u, v, d in edges:
        r = rand.randint(1,101)
        if subtrees[u] != subtrees[v]:
            if data and (r in range(probability)):
                yield (u, v, d)
            else:
                yield (u, v)
            subtrees.union(u, v)
        probability -= 1

def minimum_spanning_tree(G, weight='weight'):
    """Return a minimum spanning tree or forest of an undirected
    weighted graph.

    A minimum spanning tree is a subgraph of the graph (a tree) with
    the minimum sum of edge weights.

    If the graph is not connected a spanning forest is constructed.  A
    spanning forest is a union of the spanning trees for each
    connected component of the graph.

    Parameters
    ----------
    G : NetworkX Graph

    weight : string
       Edge data key to use for weight (default 'weight').

    Returns
    -------
    G : NetworkX Graph
       A minimum spanning tree or forest.

    Examples
    --------
    >>> G=nx.cycle_graph(4)
    >>> G.add_edge(0,3,weight=2) # assign weight 2 to edge 0-3
    >>> T=nx.minimum_spanning_tree(G)
    >>> print(sorted(T.edges(data=True)))
    [(0, 1, {}), (1, 2, {}), (2, 3, {})]
    """
    T = nx.Graph(minimum_spanning_edges(G, weight=weight, data=True))
    # Add isolated nodes
    if len(T) != len(G):
        T.add_nodes_from([n for n, d in G.degree().items() if d == 0])
    # Add node and graph attributes as shallow copy
    for n in T:
        T.node[n] = G.node[n].copy()
    T.graph = G.graph.copy()
    return T

def remove_bad_leaves(G):
    for v in G.nodes:
        T = G.copy()
        T.remove_node(v)
        if G.in_degree(v) == 1 and G.out_degree(v) == 1:
            curr = average_pairwise_distance(G)
            if average_pairwise_distance(T) < curr:
                G.remove_node(v)
    return G



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     T = solve(G)
#     assert is_valid_network(G, T)
#     print("Average  pairwise distance: {}".format(average_pairwise_distance(T)))
#     write_output_file(T, 'out/test.out')
