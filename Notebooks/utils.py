from re import sub

def MainConective(exp):
    if exp[:2] == '¬(':
        exp = sub(r'(¬)\(([^ ]+)\)', r'\1 \2', exp).split()
        con = exp[0]
        rank = exp[1]
        
        return con, rank
    elif exp[0] == '¬' and exp[1] != '(':
        exp = sub(r'(¬)([^ ]+)', r'\1 \2', exp).split()
        con = exp[0]
        rank = exp[1]
        
        return con, rank
    elif exp[0] == '(':
        exp = sub(r'\(([^ ]+)\)(v|\^|->|<->)\(([^ ]+)\)', r'\1 \2 \3', exp).split()
        con = exp[1]
        rankL = exp[0]
        rankR = exp[2]
        
        return con, rankL, rankR
    else: 
        exp = sub(r'([^ ]+)(v|\^|->|<->)([^ ]+)', r'\1 \2 \3', exp).split()
        con = exp[1]
        rankL = exp[0]
        rankR = exp[2]
    
        return con, rankL, rankR
        
class Node(object):
    def __init__(self, node=None, nodeOP=None, nodeL=None, nodeR=None):
        self.node = node
        self.nodeOP = nodeOP
        self.nodeL = nodeL
        self.nodeR = nodeR
        
    def __str__(self):
        return "{}\n\t{}\n\t{}\n\t{}".format(self.node, self.nodeOP, self.nodeL, self.nodeR)
        
        
def print_tree(tree, indent = '', rank=''):
    if tree.nodeOP == None:
        print( indent + rank + tree.node )
    elif tree.nodeOP != None and tree.nodeL != None:
        print(indent + rank + tree.node)
        print( indent + '\toperador: ' + tree.nodeOP )
        print_tree(tree.nodeL, indent=indent+'\t', rank = 'rango L: ')
        print_tree(tree.nodeR, indent=indent+'\t', rank = 'rango R: ')
    else:
        print(indent + rank + tree.node)
        print(indent + '\toperador: ' + tree.nodeOP)
        print_tree(tree.nodeR, indent=indent+'\t', rank='rango: ')
        
class Tree():
    def __init__(self):
        import networkx as nx
        self.G = nx.DiGraph()

    def construct_graph(self,tree):
        if tree.nodeOP == None:
            pass
        elif tree.nodeOP != None and tree.nodeR != None and tree.nodeL != None:
            self.G.add_edge(tree.node, tree.nodeL.node)
            self.G.add_edge(tree.node, tree.nodeOP)
            self.G.add_edge(tree.node, tree.nodeR.node)
            self.construct_graph(tree.nodeL)
            self.construct_graph(tree.nodeR)
        elif tree.nodeOP == '¬':
            self.G.add_edge(tree.node, tree.nodeR.node)
            self.G.add_edge(tree.node, tree.nodeOP)
            self.construct_graph(tree.nodeR)

        return self.G

def draw_tree(tree):
    import networkx as nx
    import matplotlib.pyplot as plt
    draw = Tree()
    draw.construct_graph(tree)
    pos = nx.planar_layout(draw.G, scale=1, center=[0,-1])
    pos1 = {}
    for i, (k,v) in enumerate(pos.items()):
        pos1[k] = (i+1)*v
    fig = plt.figure(figsize=(5,5))
    nx.draw_networkx(draw.G, pos=pos1, node_size=100, node_color='#ffffff')
    plt.title('Dibujo del árbol de análisis de la expresión')
    plt.show()
    

