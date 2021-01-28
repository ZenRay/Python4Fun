#coding:utf8
"""
朴素贝叶斯算法
"""
from collections import defaultdict, namedtuple
from sklearn.base import TransformerMixin, BaseEstimator
import numpy as np
from functools import reduce
# 定义条件概率的键类型，分别记录了:
# action: 反应类型，这里指条件概率的 P(A|B) 中的 A
# condition: 条件类型，这里指条件概率 P(A|B) 中的 B
# index: 维度索引
field = namedtuple("cp", "action condition index name", defaults=[None])

class NaiveBayes(BaseEstimator):
    def __init__(self) -> None:
        super().__init__()

    
    def fit(self, X, y):
        """根据传入数据计算先验概率和条件概率"""
        self._X = X
        self._y = y
        self.prior_ = defaultdict(float)
        self.condition_ = defaultdict(float)

        for label in y:
            self.prior_[label] += 1 / len(y)
        # 计算条件概率
        for axis in range(X.shape[1]):
            for action, condition in zip(X[:, axis], y):
                self.condition_[field(action, condition, axis)] += (
                                            1 / len(y) / self.prior_[condition])

        return self

    
    def predict(self, X):
        result = np.full((len(X), 1), np.nan)
        labels = list(self.prior_.keys())
        for row, point in enumerate(X):
            index = np.argmax(self.single_point(point))
            result[row, 0] = labels[index]
        return result

    
    def single_point(self, point):
        """预测单个数据点分类"""
        result = []
        for label in self.prior_:
            # 拆分计算 $\prod_{j=1}^n=P(x^{(j)}|y=\text{label})$ 
            value = reduce(lambda x, y: x* y, [self.condition_[field(action, label, index)]
                 for index, action in enumerate(point)]
            )
            # 计算该分类下的得分——不同类别的各特征条件概率的乘积再与先验概率相乘得到各个
            result.append(self.prior_[label] * value)
        return result

    

if __name__ == "__main__":
    import io
    import pandas as pd
    data = io.StringIO("""x1,x2,y
    1,S,-1
    1,M,-1
    1,M,1
    1,S,1
    1,S,-1
    2,S,-1
    2,M,-1
    2,M,1
    2,L,1
    2,L,1
    3,L,1
    3,M,1
    3,M,1
    3,L,1
    3,L,-1
    """)
    df = pd.read_csv(data)
    X = df.iloc[:2, :].to_numpy()
    y = df.loc[:, "y"].to_numpy()
    
    model = NaiveBayes()
    model.fit(X, y)
    result = model.predict(np.array([[2, "S"]]))
    print(result)