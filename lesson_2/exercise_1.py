# %% Imports
import numpy as np
import sys
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from adaline import Adaline
import utils

sys.path.insert(1, "../utils")
from separate_indexes_by_ratio import separateIndexesByRatio

# %% Initialize data
filePrefix = "Ex2"
xDimension = 3
tol = 1e-14
maxIterations = 100
trainSamplesRatio = 0.7

timeSamples = utils.getFileData(f"data/{filePrefix}_t", (1))

xSamples = utils.getFileData(f"data/{filePrefix}_x", tuple(range(1, xDimension + 1)))
if xDimension == 1:
    xSamples = xSamples.reshape(len(xSamples), 1)

adalineXSamples = utils.addConstantTerm(xSamples)

ySamples = utils.getFileData(f"data/{filePrefix}_y", (1))

trainIndexes, testIndexes = separateIndexesByRatio(len(timeSamples), 0.7)


# %% Initialize and Train Adaline
adaline = Adaline([0] * (xDimension + 1), 0.1)

xTrain = adalineXSamples[trainIndexes]
yTrain = ySamples[trainIndexes]
adaline.train(xTrain, yTrain, tol, maxIterations)


# %% Test
xTest = adalineXSamples[testIndexes]
yTest = ySamples[testIndexes]
testResult = adaline.test(xTest, yTest)
print(f"Mean Squared Error: {testResult}")


# %% Plot
adalineApproxYArr = adaline.evaluate(adalineXSamples)

fig = make_subplots(x_title="t", y_title="y")

# for xSample in xSamples.T:
#     fig.add_trace(go.Scatter(x=timeSamples, y=xSample, name="Entrada"))

fig.add_trace(go.Scatter(x=timeSamples, y=ySamples, name="Saida", mode='lines+markers'))

fig.add_trace(go.Scatter(x=timeSamples, y=adalineApproxYArr, name="Adaline", mode='lines+markers'))

fig.show()

# %%
adaline.printDetails()
