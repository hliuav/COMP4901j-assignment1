import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  for i in xrange(num_train):
    scores = X[i].dot(W)
    log_c = np.max(scores)
    scores -=log_c
    sum_exp=0.0
    for s in scores:
      sum_exp +=np.exp(s)
    for j in xrange(num_classes):
      exp_j = np.exp(scores[j])
      dW[:,j] += (1.0/sum_exp * exp_j-(j==y[i]))*X[i];
    loss += -scores[y[i]]+np.log(sum_exp);
  loss /= num_train
  dW /= num_train

  loss += 0.5 * reg *np.sum(W*W)
  dW += reg*W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_classes = W.shape[1]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  scores = X.dot(W)
  scores -= np.max(scores)
  
  sum_exp = np.sum(np.exp(scores),axis = 1)
  correct_class_score = scores[np.arange(0,X.shape[0]),y].reshape(scores.shape[0],1)
  loss += -np.sum(correct_class_score)+np.sum(np.log(sum_exp))
  

  y_mat = np.zeros(shape=(num_train,num_classes))
  y_mat[range(num_train),y]=1
  sum_1 = (1.0/sum_exp).reshape(X.shape[0],1)
  dW = np.exp(scores)*sum_1
  dW = np.dot(X.T,dW)
  dW -=np.dot(X.T,y_mat)
  

  loss /= num_train
  dW /= num_train

  loss += 0.5 * reg *np.sum(W*W)
  dW += reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

