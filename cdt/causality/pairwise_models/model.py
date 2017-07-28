"""
Pairwise causal models base class
Author: Diviyan Kalainathan
Date : 7/06/2017
"""
from sklearn.preprocessing import scale
from ...utils.Graph import DirectedGraph


class Pairwise_Model(object):
    """ Base class for all pairwise causal inference models

    Usage for undirected/directed graphs and CEPC df format.
    """

    def __init__(self):
        """ Init. """
        super(Pairwise_Model, self).__init__()

    def predict_proba(self, a, b):
        """ Prediction method for pairwise causal inference.
        predict is meant to be overridden in all subclasses

        :param a: Variable 1
        :param b: Variable 2
        :return: probability (Value : 1 if a->b and -1 if b->a)
        :rtype: float
        """
        raise NotImplementedError

    def predict_dataset(self, x):
        """ Causal prediction of a pairwise dataset (x,y)

        :param x: Pairwise dataset
        :type x: cepc_df format
        :return: predictions probabilities
        :rtype: list
        """

        pred = []
        for idx, row in x.iterrows():
            a = scale(row['A'].reshape((len(row['A']), 1)))
            b = scale(row['B'].reshape((len(row['B']), 1)))

            pred.append(self.predict_proba(a, b))

        return pred

    def orient_graph(self, df_data, umg):
        """ Orient an undirected graph using the pairwise method defined by the subclass
        Requirement : Name of the nodes in the graph correspond to name of the variables in df_data

        :param df_data: dataset
        :param umg: UndirectedGraph
        :return: Directed graph w/ weights
        :rtype: DirectedGraph
        """

        edges = umg.get_list_edges()
        graph = DirectedGraph()

        for edge in edges:
            a, b, c = edge
            weight = self.predict_proba(
                scale(df_data[a].as_matrix()), scale(df_data[b].as_matrix()))
            if weight > 0:  # a causes b
                graph.add(a, b, weight)
            else:
                graph.add(b, a, abs(weight))
        graph.remove_cycles()
        return graph
