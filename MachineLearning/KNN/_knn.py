#coding:utf8
"""
KNN 算法
"""
import numpy as np
import operator
from collections import Counter
from numpy.lib.arraysetops import isin

from sklearn.base import BaseEstimator, TransformerMixin


class KNN(TransformerMixin, BaseEstimator):
    """
    K 邻近算法
    """
    def __init__(self, k, metric="euclidean", algorithm="brute"):
        """初始化对象

        args:
        -------
        k: 邻近数据数量
        metric: 邻近算法指标，默认计算指标为欧式距离，'euclidean'
        algorithm: 构建模型的方法，默认是 'brute'，直接暴力计算
        """
        self.k = k

        self._metric = metric
        self._algorithm = algorithm


    def fit(self, X, y):
        self.X = X
        self.y = y
        return self


    def _brute(self, X):
        """暴力计算
        """
        pass


    def _euclidean(self, point):
        """计算数据之间的欧式距离

        Args:
        -------
        point: 单数据点
        """
        if not isinstance(point, np.ndarray):
            point = np.array(point)
            
        assert len(point.shape) == 1, "数据点维度必须为 1"
        assert point.shape[0] == self.X.shape[1], "数据点的特征数量和数据特征维度不一致"
        # 构造重复数据 (N, 1)
        points = np.tile(point, (self.X.shape[0], 1))

        distance = np.sqrt(np.sum(np.power(self.X - points, 2), axis=1))
        sorted_index = distance.argsort()

        class_count = {}
        for index in sorted_index[:self.k]:
            label = self.y[index]
            if label not in class_count:
                class_count[label] = 1
            else:
                class_count[label] += 1
        
        result = sorted(
            class_count.items(), key=operator.itemgetter(1), reverse=True
        )[0][0]
        return result


