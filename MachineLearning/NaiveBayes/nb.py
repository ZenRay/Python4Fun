#coding:utf8
"""
朴素贝叶斯算法
"""
from collections import defaultdict, namedtuple
from sklearn.base import TransformerMixin, BaseEstimator

# 定义条件概率的键类型，分别记录了:
# action: 反应类型，这里指条件概率的 P(A|B) 中的 A
# condition: 条件类型，这里指条件概率 P(A|B) 中的 B
# index: 维度索引
field = namedtuple("cp", "action condition index")

class NaiveBayes(TransformerMixin, BaseEstimator):
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
        
        for axis in X.shape[1]:
            for action, condition in zip(X[:, axis], y):
                self.condition_[field(action, condition, axis)] += (
                                            1 / len(y) / self.prior_[condition])

        return self

    
    

if __name__ == "__main__":
    import io
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
    
    