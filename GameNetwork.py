import NeuralNet as Net
import numpy as np
import BoardGame

NetworkPath = "Network.txt"
network = None

def Predict(gameBoard):
  global network
  global networkPath
  if network == None:
    network = Net.NNFromFile(NetworkPath)
  return network.Forward(InputFromBoardState(gameBoard))

def InputFromBoardState(gameBoard):
  black = []
  white = []
  king = []
  for x in gameBoard.Board:
    for y in x:
      if y == None:
        black += [0]
        white += [0]
        king += [0]
      elif y.Team == BoardGame.BLACK:
        black += [1]
        white += [0]
        king += [0]
      else:
        black += [0]
        white += [0]
        if y.IsKing:
          king += [1]
        else:
          king += [0]
  return np.array(black + white + king)
