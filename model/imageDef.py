import yaml
from collections import deque


def get_specs(f_yaml):
    """
    Parse specs from yaml file name to dict
    """
    with open(f_yaml, 'r') as f:
        specs = yaml.safe_load(f)
    return specs


class DockerImageDef:
    def __init__(self, name, depend_on=None) -> None:
        self.name = name
        self.depend_on = depend_on
        self.to_build = False
        self.downstream = []
        self.dbuildenv = {}
        self.skip_plans = []

    def __repr__(self) -> str:
        return f'DockerImageDef({self.name})'

    def subtree_order(self):
        """pre-order DFS"""
        stack = deque()
        stack.append(self)
        order = []
        while stack:
            curr = stack.pop()
            order.append(curr)
            for child in curr.downstream:
                stack.append(child)
        return order

    def get_level_order(self):
        '''BFS'''
        queue = [self]
        order = {}
        cnt = 0
        while queue:
            curr = queue.pop(0)
            for child in curr.downstream:
                queue.append(child)
            order[curr] = cnt
            cnt += 1
        return order
