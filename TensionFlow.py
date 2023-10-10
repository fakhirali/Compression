import numpy as np
import copy 
import warnings
from typing import Tuple
import graphviz

#TODO:


#Neuron Class
class Neuron:
    def __init__(self, value):
        #value
        #local derivative
        self.value = value
        self.grad = None
        self._local_backwards = []
        self.children = []
        self.op = ''
        
    def __getitem__(self,idx):
        return_val = self.value[idx]
        if not isinstance(return_val,np.ndarray):
            return return_val
        else:
            new_neuron = Neuron(self.value[idx])
            new_neuron.children = [self]
            mask = np.zeros_like(self.value)
            mask[idx] = 1
            new_neuron._local_backwards.append(lambda x: x * mask)
            new_neuron.op = 'getitem'
            return new_neuron

    def __len__(self):
        return len(self.value)

    # def __repr__(self):
    #     # return str(f'{self.value} grad: {self.grad}')
    #     return str(f'Tension: {self.value}')
    
    def __mul__(self, other_neuron):
        #if not a neuron then create a neuron
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        if isinstance(self.value, np.ndarray) and isinstance(other_neuron.value, np.ndarray):
            assert self.value.shape == other_neuron.value.shape, "Shapes must be same to perform element-wise multiplication"

        # self,other_neuron = self._handle_back_add(other_neuron)
        new_val = self.value * other_neuron.value
        new_neuron = Neuron(self.value * other_neuron.value)
        new_neuron.children = [self,other_neuron]

        t1= other_neuron.value
        t2= self.value
        new_neuron._local_backwards.append(lambda x: x*t1)
        new_neuron._local_backwards.append(lambda x: x*t2)
        new_neuron.op = 'mul'
        return new_neuron

    def __matmul__(self,other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        new_neuron = Neuron(self.value @ other_neuron.value)
        new_neuron.children = [self, other_neuron]
        t1 = other_neuron.value.T
        t2 = self.value.T
        new_neuron._local_backwards.append(lambda x: x @ t1)
        new_neuron._local_backwards.append(lambda x: t2 @ x)
        new_neuron.op = 'matmul'
        return new_neuron
    
    def shape(self):
        return self.value.shape

    def __add__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        if isinstance(self.value, np.ndarray) and isinstance(other_neuron.value, np.ndarray):
            assert self.value.shape == other_neuron.value.shape, "Shapes must be same to perform element-wise addition"
        # self,other_neuron = self._handle_back_add(other_neuron)
        new_neuron = Neuron(self.value + other_neuron.value)
        new_neuron.children = [self,other_neuron]
        new_neuron._local_backwards.append(lambda x: x)
        new_neuron._local_backwards.append(lambda x: x)
        new_neuron.op = 'add'
        return new_neuron
    

    def sum(self, dim=-1):
        assert isinstance(self.value, np.ndarray), "Has to be a numpy array to sum"
        new_neuron = Neuron(self.value.sum(dim, keepdims=True))
        new_neuron.children = [self]
        t1 = self.value.shape
        new_neuron._local_backwards.append(lambda x: x * np.ones(t1))
        new_neuron.op = 'sum'
        return new_neuron

    #setting right add and mul to mul and add
    __radd__ = __add__
    __rmul__ = __mul__
    
    def __neg__(self):
        # self,other_neuron = self._handle_back_add()
        minus_one = Neuron(-1)
        return self * minus_one
    
    def __sub__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self + (-other_neuron)
    
    def __rsub__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return other_neuron + -(self)
    
    def __truediv__(self,other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        
        return self * other_neuron.mul_inverse()
    
    def __rtruediv__(self,other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.mul_inverse() * other_neuron
    
    def __lt__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.value < other_neuron.value
    
    def __gt__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.value > other_neuron.value
    
    def __eq__(self, other_neuron):
        #this is equal to the "is" operator to make toposort in list work
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.__repr__() == other_neuron.__repr__()
        # return self.value == other_neuron.value

    def __ge__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.value >= other_neuron.value

    def __le__(self, other_neuron):
        if not isinstance(other_neuron, Neuron):
            other_neuron = Neuron(other_neuron)
        return self.value <= other_neuron.value

    def __float__(self):
        return self.value
    def __hash__(self):
        return hash(self.__repr__())

    def mul_inverse(self):
        # self,other_neuron = self._handle_back_add()
        new_neuron = Neuron(1/self.value)
        temp = -1/(self.value**2)
        # print(temp)
        new_neuron._local_backwards.append(lambda x: x * temp)
        new_neuron.children = [self]
        new_neuron.op = 'mul_inverse'
        return new_neuron

    def reshape(self, new_shape):
        new_neuron = Neuron(self.value.reshape(new_shape))
        new_neuron.children = [self]
        new_neuron._local_backwards.append(lambda x: x.reshape(self.value.shape))
        new_neuron.op = 'reshape'
        return new_neuron
   
    def zero_grad(self):
        self.grad = None

    def log(self):
        new_val = np.log(self.value)
        if np.inf in new_val or -np.inf in new_val:
            warnings.warn("inf in log, replacing with zero")
            new_val[new_val==np.inf] = 0
            new_val[new_val==-np.inf] = 0
        new_neuron = Neuron(new_val)
        temp = 1/self.value
        new_neuron.children = [self]
        new_neuron._local_backwards.append(lambda x: x * temp)
        new_neuron.op = 'log'
        return new_neuron
         
        
    def exp(self):
        # self,other_neuron = self._handle_back_add()
        new_neuron = Neuron(np.exp(self.value))
        temp = np.exp(self.value)
        new_neuron._local_backwards.append(lambda x: x *temp)
        new_neuron.children = [self]
        new_neuron.op = 'exp'
        return new_neuron

    def argmax(self,dim=None):
        return Neuron(self.value.argmax(axis=dim))        

    def broadcast(self, new_shape:int):
        assert 1 in self.shape(), "There must be a 1 to broadcast the neuron"
        # assert len(self.shape()) == 2, "Only supports broadcasting of 2d neurons"
        if self.shape()[0] == 1:
            new_neuron = Neuron(np.ones((new_shape,1))) @ self
        else: 
            new_neuron =  self @ Neuron(np.ones((1, new_shape)))
        new_neuron.op = 'broadcast'
        return new_neuron 
    
    def max(self, dim=None):
        new_neuron = Neuron(self.value.max(axis=dim, keepdims=True))
        new_neuron.children = [self]

        if dim is None:
            mask = np.zeros(self.value.shape)
            mask[np.unravel_index(self.value.argmax(), self.value.shape)] = 1
        else:
            expanded_indices = np.expand_dims(np.argmax(self.value, axis=dim), dim)
            mask = np.zeros_like(self.value)
            np.put_along_axis(mask, expanded_indices, 1, axis=dim)

        new_neuron._local_backwards.append(lambda x: x * mask)
        new_neuron.op = 'max'
        return new_neuron

 

    def _toposort(self):
        root = self
        stack = [root]
        visited = []
        indegree = {root:0}
        while len(stack) != 0:
            root = stack.pop(0)
            visited.append(root)
            for child in root.children:
                if child not in indegree:
                    indegree[child] = 0
                indegree[child] += 1
                # print(σchild, visited)
                if child not in visited:
                    stack.append(child)
        return indegree

    def make_graph(self):
        indegree  = self._toposort()
        dot = graphviz.Digraph(comment='Computation Graph')
        i = 0
        zero_indegree = [self]
        while len(zero_indegree) != 0:
            root = zero_indegree.pop(0)
            for child in root.children:
                dot.edge(root.op+str(root), child.op + str(child), label=str(i))
                indegree[child] -= 1
                if indegree[child] == 0:
                    zero_indegree.append(child)
                i += 1
        return dot 

    def backward(self):
        assert self.grad is None
        indegree  = self._toposort()
    
        if isinstance(self.value, np.ndarray):
            self.grad = np.ones_like(self.value)
        else:
            self.grad = 1

        zero_indegree = [self]
        while len(zero_indegree) != 0:
            root = zero_indegree.pop(0)
            for child, local_backwards in zip(root.children, root._local_backwards):
                # print(root, child)
                if not (child.grad is None): 
                    child.grad += local_backwards(root.grad)
                else:
                    child.grad = local_backwards(root.grad)
                indegree[child] -= 1
                if indegree[child] == 0:
                    zero_indegree.append(child)    
        
    def transpose(self):
        new_neuron = Neuron(self.value.T)
        new_neuron.children = [self]
        new_neuron._local_backwards.append(lambda x: x.T)
        new_neuron.op = 'transpose'
        return new_neuron 
        # root = self
        # stack = [root]
        # while len(stack) != 0:
        #     root = stack.pop(0)
        #     for child, local_backwards in zip(root.children, root._local_backwards):
        #         # print(root, child)
        #         if not (child.grad is None): 
        #             child.grad += local_backwards(root.grad)
        #         else:
        #             child.grad = local_backwards(root.grad)
        #         stack.append(child)

    def backward_zero_grad(self) -> None:
            self.grad = None
            root = self
            stack = [root]
            while len(stack) != 0:
                root = stack.pop(0)
                for child, local_backwards in zip(root.children, root._local_backwards):
                    # print(root, child)
                    child.grad = None
                    stack.append(child)


    def softmax(self, dim=0):
        y = self - self.max(dim).broadcast(self.shape()[dim])
        exp = y.exp()
        sum_exp = exp.sum(dim)
        return exp / sum_exp.broadcast(self.shape()[dim])

class LinearLayer:
    def __init__(self, f_in, f_out, bias=True):
        self.bias = bias
        self.w =  neuron = Neuron(np.random.uniform(low=-np.sqrt(1/f_in),
                                        high=np.sqrt(1/f_in), 
                                        size=(f_in, f_out)))
        if bias:
            self.b = Neuron(np.random.uniform(low=-np.sqrt(1/f_in),
                                        high=np.sqrt(1/f_in), 
                                        size=(1, f_out)))
    def forward(self, x):
        if self.bias:
            x = x @ self.w + self.b.broadcast(x.shape()[0])
        else:
            x = x @ self.w
        return x
    
    def update(self, lr):
        self.w.value -= lr * self.w.grad
        if self.bias:
            self.b.value -= lr * self.b.grad

    

def concatenate(x: Neuron, y:Neuron):
    new_neuron =  Neuron(np.concatenate((x.value, y.value), axis=1)) 
    new_neuron.children = [x,y]
    t1 = x.value.shape[1]
    t2 = y.value.shape[1]
    new_neuron._local_backwards.append(lambda x: x[:, :t1])
    new_neuron._local_backwards.append(lambda x: x[:, t1:])
    new_neuron.op = 'concatenate'
    return new_neuron

#helper funcs

def one_hot(x: Neuron, classes:int) -> Neuron:
    assert len(x.shape()) == 1, "one hot of 2d matrix not supported"
    a = np.zeros((len(x), classes))
    for i in range(len(x)):
        a[i][x[i]] = 1
    return Neuron(a)
    

def Sigmoid(x: Neuron):
    return 1/(1+(-1 * x).exp())

def Tanh(x: Neuron):
    return (2/(1+(-2 * x).exp())) - 1

def ReLU(x: Neuron)  -> Neuron:
    mask = Neuron(1 * (x.value > 0))
    return x * mask
    


def CrossEntropy(out_soft: Neuron, oh_label: Neuron) -> Neuron:
    return -(out_soft * oh_label).sum().log().sum(0)
