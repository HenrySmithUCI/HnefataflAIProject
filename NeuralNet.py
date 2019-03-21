import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection

def sigmoid(x, der = False):
  sig = 1. / (1. + np.exp(-np.clip(x, -700, 700))) #clipped to prevent overflow
  if der:
    return (sig * (1. - sig)) * 2.
  return (sig * 2.) - 1. # Recentering so range is [-1, 1]

def NNFromFile(path = "Network.txt"):
  with open(path) as f:
    shape = f.readline()[:-2]
    shape = [int(s) for s in shape.split(" ")]
    ret = NN(shape)
    for l in range(len(shape)-1):
      line = f.readline()[:-2]
      line = [np.float64(s) for s in line.split(" ")]
      ret.weights[l] = np.reshape(line, (shape[l+1], shape[l]))
  return ret

class NN:
  def __init__(self, shape, activation = sigmoid):
    self.activation = activation
    self.shape = shape
    self.weights = []
    for i in range(len(shape) - 1):
      self.weights.append(np.random.rand(shape[i+1], shape[i]) * 2 - 1)

  def Forward(self, inputArray): # used for final output
    layer = inputArray
    for mat in self.weights:
      layer = np.matmul(mat, layer) #forward propagation
      layer = self.activation(layer) #activation layer
    return layer

  def ForwardAll(self, inputArray): # used for training, stores middle layer states
    layers = [inputArray]
    for mat in self.weights:
      layers.append(np.matmul(mat, layers[-1])) #forward propagation
      layers.append(self.activation(layers[-1]))#activation layer
    return layers

  def __str__(self):
    ret = ""
    for s in self.shape:
      ret += str(s) + " "
    ret += "\n"
    for lay in self.weights:
      for n in lay.flatten():
        ret += str(n) + " "
      ret += "\n"
    return ret

def MSError(network, X, Y):
  return np.sum(((Y - network.Forward(X))) ** 2) / X.shape[1] # sum(y_i - y'_i^2)/n

def deltaWeights(network, InputMatrix, OutputMatrix):
  forwardAll = network.ForwardAll(InputMatrix)
  deltas = []

  midDelta = -(OutputMatrix - forwardAll[-1]) * network.activation(forwardAll[-2], True) #calculate gradient
  deltas.append(np.dot(midDelta, forwardAll[-3].T))

  for layer in range(2, len(network.weights)+1):
    midDelta = np.dot(network.weights[-layer+1].T, midDelta) * network.activation(forwardAll[-layer*2],True) #propogate gradients for each layer
    deltas.append(np.dot(midDelta, forwardAll[-layer*2-1].T))

  deltas.reverse() #gradient generated from end to front, so reversing necessary
  return deltas

def UpdateWeights(network, deltas, coef = -0.0001):
  for l in range(len(network.weights)):
    network.weights[l] += deltas[l] * coef

Xtr = None
Ytr = None
Xte = None
Yte = None
network = None
RecordX = []
RecordY = []
trainedCount = 0

def TrainNew(InputsPath = "data/Xtr.txt", OutputsPath = "data/Ytr.txt", hiddenLayerShape = [70,50], outputFile = "Network.txt", TrainCount = 10, StepSize = -0.0001):
  global Xtr
  global Ytr
  global network
  global trainedCount
  if(type(Xtr) == type(None)):
    Xtr = np.genfromtxt(InputsPath, delimiter = None)
  if(type(Ytr) == type(None)):
    Ytr = np.genfromtxt(OutputsPath, delimiter = None)
  
  def getColumnCount(array):
    try:
      return len(array[0])
    except:
      return 1
    
  iSize = getColumnCount(Xtr)
  oSize = getColumnCount(Ytr)

  Xtr = Xtr.T
  Ytr = Ytr.T
  
  network = NN([iSize] + hiddenLayerShape + [oSize])

  for i in range(TrainCount):
    deltas = deltaWeights(network, Xtr, Ytr)
    UpdateWeights(network, deltas, StepSize)

  trainedCount += TrainCount
  RecordX.append(trainedCount)
  RecordY.append(Test())

  StoreNetwork(outputFile)

def TrainExisting(InputsPath = "data/Xtr.txt", OutputsPath = "data/Ytr.txt", networkFile = "Network.txt", TrainCount = 10, StepSize = -0.0001):
  global Xtr
  global Ytr
  global network
  global trainedCount
  if(type(Xtr) == type(None)):
    Xtr = np.genfromtxt(InputsPath, delimiter = None).T
  if(type(Ytr) == type(None)):
    Ytr = np.genfromtxt(OutputsPath, delimiter = None).T

  if(network == None):
    network = NNFromFile(networkFile)
  
  for i in range(TrainCount):
    deltas = deltaWeights(network, Xtr, Ytr)
    UpdateWeights(network, deltas, StepSize)

  trainedCount += TrainCount
  RecordX.append(trainedCount)
  RecordY.append(Test())

  StoreNetwork(networkFile)

def StoreNetwork(fileName):
  global network
  with open(fileName, "w") as f:
    f.write(str(network))

def TrainFull(MakeNew = True):
  eps = 0.000001
  if(MakeNew):
    TrainNew(TrainCount = 0)
    prev = Test()
    print(prev)
    TrainExisting(TrainCount = 100)
    current = Test()
    print(current)
  else:
    prev = 10
    current = Test()
    print(current)
  while(np.abs(prev - current) > eps):
    StoreNetwork("OldNetwork.txt")
    TrainExisting(StepSize = -current/1000)
    prev = current
    current = Test()
    print(current)
  display()

def Test(testInputs = "data/Xte.txt", testOutputs = "data/Yte.txt", networkFile = "Network.txt"):
  global Xte
  global Yte
  global network
  if(type(Xte) == type(None)):
    Xte = np.genfromtxt(testInputs, delimiter = None).T
  if(type(Yte) == type(None)):
    Yte = np.genfromtxt(testOutputs, delimiter = None).T
  if(network == None):
    network = NNFromFile(networkFile)
  return MSError(network, Xte, Yte)

def display():
  with open("record.txt", "a") as f:
    f.write(str(RecordX) + "\n")
    f.write(str(RecordY) + "\n")
  plt.plot(RecordX, RecordY)
  plt.show()

def splitData(InputsPath = "data/Inputs.txt", OutputsPath = "data/Outputs.txt", XtrFile = "data/Xtr.txt", XteFile = "data/Xte.txt", YtrFile = "data/Ytr.txt", YteFile = "data/Yte.txt"):
  global Xtr
  global Ytr
  global Xte
  global Yte
  Inputs = np.genfromtxt(InputsPath, delimiter = None)
  Outputs = np.genfromtxt(OutputsPath, delimiter = None)
  Xtr, Xte, Ytr, Yte = model_selection.train_test_split(Inputs, Outputs, test_size=0.25, shuffle = True)
  
  def makeFile(path, array):
    with open(path, "w") as f:
      try:
        for line in array:
          f.write(" ".join([str(n) for n in line]))
          f.write("\n")
      except:
        for line in array:
          f.write(str(line))
          f.write("\n")
  
  makeFile(XtrFile, Xtr)
  makeFile(XteFile, Xte)
  makeFile(YtrFile, Ytr)
  makeFile(YteFile, Yte)
  
  Xtr = Xtr.T
  Ytr = Ytr.T
  Xte = Xte.T
  Yte = Yte.T
