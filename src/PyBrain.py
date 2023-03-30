
import random

import PyDriverUtils as utils

class PyNetwork:

    def __init__(self, neurons):

        self.levels = []
        for i in range(0, len(neurons)-1):
            self.levels.append(PyNetworkLevel(n_of_inputs=neurons[i], n_of_output=neurons[i+1]))

    @staticmethod
    def feed_forward(inputs, network):

        outputs = PyNetworkLevel.feed_forward(inputs, network.levels[0])

        for i in range(1, len(network.levels)):
            outputs = PyNetworkLevel.feed_forward(outputs, network.levels[i])

        return outputs

    @staticmethod
    def mutate(network, amount=1):

        for level in network.levels:

            for i in range(0, len(level.biases)):
                level.biases[i] = utils.lerp(level.biases[i], random.randrange(-1, 1), amount)

            for i in range(0, len(level.weights)):

                for j in range(0, len(level.weights[i])):

                    level.weights[i][j] = utils.lerp(level.weights[i][j], random.randrange(-1, 1), amount)



class PyNetworkLevel:

    def __init__(self, n_of_inputs, n_of_output):

        self.inputs = [0] * n_of_inputs
        self.outputs = [0] * n_of_output
        self.biases = [0] * n_of_output

        self.weights = [0] * n_of_inputs
        for i in range(0, len(self.inputs)):
            self.weights[i] = [0] * n_of_output

        self = self.randomize(self)

    @staticmethod
    def randomize(level):

        for i in range(0, len(level.inputs)):
            for o in range(0, len(level.outputs)):
                level.weights[i][o] = random.randrange(-1, 1)

        for b in range(0, len(level.biases)):
            level.biases[b] = random.randrange(-1, 1)



    @staticmethod
    def feed_forward(inputs, level):
        for i in range(0, len(level.inputs)):
            level.inputs[i] = inputs[i]

        for o in range(0, len(level.outputs)):
            s = 0
            for i in range(0, len(level.inputs)):
                s += level.inputs[i]*level.weights[i][o]

            if s > level.biases[o]:
                level.outputs[o] = 1
            else:
                level.outputs[o] = 0

        return level.outputs


if __name__ == '__main__':
    n = PyNetworkLevel(n_of_inputs=2, n_of_output=2)
