#coding:utf8
"""
构造 KD tree
"""
import numpy as np
from queue import PriorityQueue, LifoQueue


class Node:
    """
    节点

    属性包括父节点、左右子节点以及当前节点数据值
    """

    def __init__(self, **kwargs) -> None:
        self.left = kwargs.get("left")
        self.right = kwargs.get("right")
        self.point = kwargs.get("point")


    def __str__(self) -> str:
        fmt = f"<Node at {hex(id(self))}>"
        return fmt
    
    
    def __repr__(self) -> str:
        if len(self.point) > 0:
            value = ", ".join(str(i) for i in self.point)
        elif isinstance(self.point, (str, int, float)):
            value = self.point
        else:
            raise TypeError(f"Point value is {type(self.point)}, need array, "
                            "int, str")
        # 存在左右子节点输出
        if self.left is not None:
            left = " Left child: Node;"
        else:
            left = ""
        
        if self.right is not None:
            right = " Right child: Node;"
        else:
            right = ""

        fmt = f"<Node value: ({value});{left}{right}>"
        
        return fmt


    def has_left(self):
        """判断是否有左子节点"""
        return isinstance(self.left, Node)

    
    def has_right(self):
        """判断是有右子节点"""
        return isinstance(self.right, Node)

class KDTree:
    def __init__(self, values=None):
        self.split_dim = 0

        if values is None:
            self.root = None
        else:
            self.root = self.build(values)
        

    def build(self, values, depth=0):
        """构造 KD 树

        """
        # 如果数据使用完时，终止构建，并将设置当前索引为 0 
        if len(values) == 0:
            return

        # 根据 $l=j(mod k) + 1$ 方式来确认需要选择的数据维度，j 为 depth， k 为 values
        # 的维度。实际应用中，因为索引以 0 为起始，所以不再加 1
        dim = depth % values.shape[1] 
        # 使用中位数拆分数据
        sorted_index = np.argsort(values[:, dim])
        median = len(sorted_index) // 2
        node = Node(point=values[sorted_index[median], :])
        
        # 获取左右子节点数据并分别将数据给到左右子节点
        left_values = values[sorted_index[:median]]
        right_valus = values[sorted_index[median+1:]]
        
        node.left = self.build(values=left_values, depth=depth + 1)
        node.right = self.build(values=right_valus, depth=depth + 1)

        return node



    def search(self, X, k=1):
        """搜索KD树

        查找数据点 X 的 K 近邻节点
        """
        # TODO: 查找“最近”叶节点
        if not isinstance(X, np.ndarray):
            X = np.array(X)
        
        node = self.root
        
        stack = LifoQueue()
        stack.put_nowait(node)
        # 树深度
        depth = 1
        while True:
            # 左节点为空，存在右节点相反情况时直接将节点修改为对应子节点，左右节点都存在时再比较
            if node.left is None and node.right:
                node = node.right
            elif node.right is None and node.left:
                node = node.left
            else:
                dim = depth // X.shape[0]
                if X[dim] <= node.point[dim]:
                    node = node.left
                else:
                    node = node.right
            stack.put_nowait(node)
            # 终止条件为达到叶节点
            if node.left is None and node.right is None:
                break
            
            depth += 1
        
        # TODO: 回退搜搜
        result = PriorityQueue(maxsize=k)
        # 检查叶节点，将叶节点作为最近邻 node
        node = stack.get_nowait()
        distance = np.linalg.norm(node.point - X)
        queried = [node]

        # 优先队列是按照从小达到排序，保证最终结果保留最小值，所以将距离取逆作为 priority
        result.put_nowait((-1 * distance, node))
        
        while not stack.empty():
            node = stack.get_nowait()
            # 检查父节点下另一子节点是否为最近节点，将节点给到 stack 进行循环以实现对子节点
            # 的搜索
            if node.has_left() and node.left not in queried:
                stack.put_nowait(node)
                node = node.left
                
            elif node.has_right() and node.right not in queried:
                stack.put_nowait(node)
                node = node.right
                

            if node in queried:
                continue
            # 添加到已访问列表
            queried.append(node)
            distance = np.linalg.norm(node.point - X)
            
            # 如果结果队列没有满，那么直接将节点添加到队列中
            if not result.full():
                result.put_nowait((-1 * distance, node))
                continue
            
            # 如果队列满了，那么取队列中到 priority 作为判断队列是否更新到门槛
            current_distance, current_node = result.get_nowait()

            if -1 * current_distance >= distance:
                result.put_nowait((-1 * distance, node))
            else:
                result.put_nowait((current_distance, current_node))

        return result



if __name__ == "__main__":
    values = np.array([[7,2], [5, 4], [9, 6], [2,3], [4,7], [8,1]])

    node = KDTree(values)
    t = node.search([8,1], 1)
    print(t.get_nowait()[1])
