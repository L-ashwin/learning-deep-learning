import numpy as np
from tqdm import tqdm
class Linear:
    def __init__(self):
        self.W = None
        self.b = None

    def train(self, X_data, y_data, no_classes, lr=1e-2, epochs=10):
        """
        Trains a linear classifier with given data and stores weights curresponding
        to lowest loss epoch.

        X_data : feature array with shape [number of examples, number of feature]
        y_data : integer encoded labels / targets array with shape [number of examples, ]
        lr     : learning rate
        epochs  : number of epochs
        """

        n, m = X_data.shape # number of examples, feature dimensions
        c = no_classes # number of classes

        W, b = self.initialize_parameters(m, c)

        best_loss = np.inf
        for epoch in tqdm(range(epochs)):
            # calculate class scores
            S = X_data@W.T + b

            # softmax on scores
            A = self.softmax(S)

            # cross entropy loss
            loss = -np.sum(np.log(A[np.arange(n), y_data]))
            #print(f'for epoch:{epoch} => training loss:{loss}')

            # calculate gradients
            dS = A # d_loss/d_score
            dS[np.arange(n), y_data] -= 1

            dW = dS.T@X_data #d_loss/d_W
            db = dS.sum(axis=0)

            # update weights
            W -= lr*dW
            b -= lr*db

            if loss < best_loss:
                best_loss = loss
                self.W, self.b = W, b

    def predict(self, X):
        """
        reutrns predicted class for input featureset.

        X : feature array with shape [number of examples, number of feature]
        """
        S = X@self.W.T + self.b
        pred = np.argmax(S, axis=1)
        return pred

    def softmax(self, S):
        # subtract max from each example for numerical stability
        S -= np.max(S, axis=1, keepdims=True)
        S_exp   = np.exp(S)
        softmax = (S_exp + 1e-6)/(np.sum(S_exp, axis=1, keepdims=True) + len(S_exp)*1e-6)
        return softmax

    def initialize_parameters(self, m, c):
        W = np.random.rand(c, m)*0.01
        b = np.zeros(c)
        return W, b
