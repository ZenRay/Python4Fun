#coding:utf8
"""
逻辑回归算法
依据 李航统计学习方法第二版 搭建模型
* 继承 sci-kit learn 的类
"""
import numpy as np

from sklearn.base import BaseEstimator


def sigmoid(z):
    """Sigmoid Function

    Sigmoid 函数: \frac{\exp^z}{1+\exp^z}
    """
    numerator = np.exp(z)
    denominator = 1 + np.exp(z)
    return numerator / denominator

class Logist(BaseEstimator):
    """Losit Class
    
    Attributes:
    --------------
    coef_: 模型参数
    intercept_: 线性模型中的截距
    
    """

    def __init__(self) -> None:
        super().__init__()

        self.coef_ = None
        self.intercept_ = None

    
    def fit(self, X, y):
        """Fit Model"""
        pass


    def predict(self, X, y=None):
        pass