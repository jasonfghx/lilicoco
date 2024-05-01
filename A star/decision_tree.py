from decision import *
from lidar import lidar


class Tree_node():
    def __init__(self, determine_fun=None, left_node=None, right_node=None) -> None:
        self._fun = determine_fun
        self._left = left_node
        self._right = right_node

    @property
    def fun(self):
        return self._fun

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @left.setter
    def left(self, data: object):
        if(not (isinstance(data, Tree_node))):
            if(data != None):
                raise TypeError

        self._left = data

    @right.setter
    def right(self, data: object):
        if(not (isinstance(data, Tree_node))):
            if(data != None):
                raise TypeError

        self._right = data


class Control_unit():
    _node_num = 1

    def __init__(self, node: Tree_node) -> None:
        '''
        Add root
        '''
        self._root = node

    def add_node(self, parent: Tree_node, left, right):
        if(not (isinstance(left, Tree_node) and isinstance(right, Tree_node))):
            if(left != None and right != None):
                raise TypeError

        parent.left = left
        parent.right = right

        self._node_num += 1

    def traverse(self, node, data):
        if node is not None:
            # print(node.fun.__name__)
            result = node.fun(data)
            if result == 0:
                self.traverse(node.left, data)
            else:
                self.traverse(node.right, data)

    def run(self, data):
        self.traverse(self._root, data)

    def _run_print_tree(self, node, level=0):
        if node is None:
            return

        print('\t   ' * level + '|->', node.fun.__name__)
        self._run_print_tree(node.right, level=level+1)
        self._run_print_tree(node.left, level=level+1)

    def print(self):
        self._run_print_tree(self._root)

    @property
    def root(self):
        return self._root


class lidar_Controller():
    def __init__(self, print_out=False):
        root = Tree_node(is_reachable)
        this = Control_unit(root)

        # ----
        node_go_to_dest = Tree_node(go_to_dest)
        node_scan_and_is_wander = Tree_node(scan_and_is_wander)
        node_lager_radius = Tree_node(lager_radius)
        node_is_all_white = Tree_node(is_all_white)

        node_is_all_black = Tree_node(is_all_black)

        node_smaller_radius = Tree_node(smaller_radius)
        node_go_the_shortest = Tree_node(go_the_shortest)

        node_is_nextstep_one = Tree_node(is_nextstep_one)
        node_rating_and_the_smallest_is_one = Tree_node(
            rating_and_the_smallest_is_one)

        node_go_to_the_only_nextstep = Tree_node(go_to_the_only_nextstep)
        node_look_backward_and_is_newlist_one = Tree_node(
            look_backward_and_is_newlist_one)

        node_choose_best_look_backward = Tree_node(choose_best_look_backward)
        node_choose_best_abc_order = Tree_node(choose_best_abc_order)

        # ----

        this.add_node(this.root, node_scan_and_is_wander, node_go_to_dest)

        this.add_node(node_scan_and_is_wander,
                      node_is_all_white, node_lager_radius)

        this.add_node(node_is_all_white, node_is_all_black,
                      node_go_the_shortest)

        this.add_node(node_is_all_black, node_is_nextstep_one,
                      node_smaller_radius)

        this.add_node(node_is_nextstep_one,
                      node_rating_and_the_smallest_is_one, node_go_to_the_only_nextstep)

        this.add_node(node_rating_and_the_smallest_is_one,
                      node_look_backward_and_is_newlist_one, node_choose_best_abc_order)

        this.add_node(node_look_backward_and_is_newlist_one,
                      node_choose_best_abc_order, node_choose_best_look_backward)

        self._this = this
        self.if_print = print_out

    def run(self, lidar_obj: lidar) -> None:
        self._this.run(lidar_obj)

    def print(self):
        self._this.print()


if __name__ == "__main__":
    k = lidar_Controller()
    k.print()
    i = 1
    '''
    while(not robot.if_in_dest()):
        print("k.run(robot)\n")
        k.run(robot)

    print(robot.getter_single('cp'))
    '''
