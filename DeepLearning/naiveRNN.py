#coding:utf8
"""
简单的单一 RNN 结构模型实现:
result_i = tanh(dot(W_io, input_i) + dot(U_ho, hidden_i) + bias)
result = [result_1, result_2,..., result_t]
"""


import numpy as np
from numpy import ndarray



class NaiveRNN:
    def __init__(self, input_size: int, output_size: int):
        # initial weight about W_io, U_ho and bias
        self.weight_io = np.random.randn(output_size, input_size)
        self.weight_ho = np.random.randn(output_size, output_size)
        self.bias = np.random.random(size=(output_size, ))

    
    def forward(self, inputs:ndarray, hidden:ndarray=None):
        if hidden is None:
            hidden = np.zeros((self.weight_ho.shape[1], ))
        
        outputs = []
        for input_ in inputs:
            current_output = np.tanh(self.weight_io.dot(input_) + self.weight_ho.dot(hidden) + self.bias)
            outputs.append(current_output)

            # update hidden state value
            hidden = current_output

        # concate output
        result = np.stack(outputs, axis=0)

        return result, hidden



if __name__ == "__main__":
    timesteps = 100
    input_size = 32
    output_size = 64
    inputs = np.random.random((timesteps, input_size))

    rnn = NaiveRNN(input_size=input_size, output_size=output_size)

    U = np.copy(rnn.weight_ho)
    W = np.copy(rnn.weight_io)
    b = np.copy(rnn.bias)

    result, _ = rnn.forward(inputs)

    state_t = np.zeros((output_size,))
    successive_outputs = []
    for input_t in inputs:
        output_t = np.tanh(np.dot(W, input_t) + np.dot(U, state_t) + b)
        successive_outputs.append(output_t)
        state_t = output_t
    final_output_sequence = np.stack(successive_outputs, axis=0)

    np.testing.assert_array_equal(result, final_output_sequence, "Naive RNN Wrong")