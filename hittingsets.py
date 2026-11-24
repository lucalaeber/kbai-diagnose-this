"""
Knowledge Based AI - Programming assignment 3: Diagnose THIS
Group: 21
Authors: Luca Laber (s1089333), Nadezhda Kancheva (s1141095)
"""

from collections import deque
class TreeNode:
    """
    A node of the hitting set tree (HS-tree).

    An open node is labelled with a conflict set. A node is closed when no
    conflict set is left to resolve, and pruned when it can be discarded.
    Every edge from a node to a child is labelled with one component of the
    node's conflict set.
    """

    def __init__(self, parent=None, edge_label=None):
        """
        :param parent: the node above this one (None for the root)
        :param edge_label: the component on the edge from the parent to this node
        """
        self.parent = parent # the node above (None for the root)
        self.edge_label = edge_label # component on the edge from the parent
        self.children = [] # child nodes
        self.label = None # a conflict set
        self.status = "open" # open / closed / pruned

        # Components on the edges from the root to this node (the candidate hitting set).
        # Stored as a frozenset so subset and intersection checks are cheap.
        if parent is None:
            self.path = frozenset()
        else:
            self.path = parent.path | {edge_label}

def find_unhit_conflict_set(path, conflict_sets):
    """
    Returns the first conflict set that has no component in common with the path,
    or None if the path hits every conflict set.

    :param path: frozenset of components on the path from the root to a node
    :param conflict_sets: list of conflict sets (frozensets)
    :return: a conflict set, or None
    """
    for conflict_set in conflict_sets:
        if not path & conflict_set: # empty intersection: this set is not hit
            return conflict_set
    return None


def build_hitting_set_tree(conflict_sets, breadth_first=True):
    """
    Builds the HS-tree.

    :param conflict_sets: list of conflict sets (frozensets)
    :param breadth_first: True for BFS, False for DFS
    :return: the root node and the list of closed nodes
    """
    root = TreeNode()
    open_nodes = deque([root])
    closed_nodes = []

    while open_nodes:
        # BFS takes from the front of the queue, DFS from the back
        node = open_nodes.popleft() if breadth_first else open_nodes.pop()

        unhit_conflict_set = find_unhit_conflict_set(node.path, conflict_sets)

        if unhit_conflict_set is None:
            # every conflict set is hit, so node.path is a hitting set
            node.status = "closed"
            closed_nodes.append(node)
        else:
            # still a conflict set left: label the node and expand it
            node.label = unhit_conflict_set
            for component in sorted(unhit_conflict_set):
                child = TreeNode(parent=node, edge_label=component)
                node.children.append(child)
                open_nodes.append(child)

    return root, closed_nodes


def filter_minimal_sets(sets):
    """
    Keeps only the minimal sets: those with no proper subset in the collection.

    :param sets: list of frozensets
    :return: list of the minimal frozensets
    """
    minimal_sets = []
    for candidate in sets:
        is_minimal = True
        for other in sets:
            if other < candidate:       # other is a proper subset of candidate
                is_minimal = False
                break
        if is_minimal:
            minimal_sets.append(candidate)
    return minimal_sets


def run_hitting_set_algorithm(conflict_sets):
    """
    Algorithm that handles the entire process from conflict sets to hitting sets

    :param conflict_sets: list of conflict sets as list
    :return: the hitting sets and minimal hitting sets as list of lists
    """
    # the tree code works with frozensets (fast intersection and subset checks)
    conflict_sets = [frozenset(conflict_set) for conflict_set in conflict_sets]

    _, closed_nodes = build_hitting_set_tree(conflict_sets)

    # the path of every closed node is a hitting set; drop duplicates but keep the order
    hitting_sets = []
    for node in closed_nodes:
        if node.path not in hitting_sets:
            hitting_sets.append(node.path)

    minimal_hitting_sets = filter_minimal_sets(hitting_sets)

    # convert back to sorted lists of lists
    return ([sorted(hitting_set) for hitting_set in hitting_sets],
            [sorted(minimal_set) for minimal_set in minimal_hitting_sets])