from numpy import *
import operator

def createDataSet():
    # create a matrix: each row as a sample
    group = array([[1.0, 0.9], [1.0, 1.0], [0.0, 0.1],[0.1, 0.2]])
    labels = ['A', 'A', 'B', 'B']  # four samples and two classes
    return group, labels

def kNNClassify(newInput, dataSet, labels, k):
    numSamples = dataSet.shape[0]
    diff = tile(newInput, (numSamples, 1)) - dataSet
    squaredDiff = diff ** 2
    squaredDist = sum(squaredDiff, axis=1)
    distance = squaredDist ** 0.5
    sortedDistIndices = argsort(distance)
    print(sortedDistIndices)
    print(distance)
    classCount = {}
    for i in xrange(k):
        voteLabel = labels[sortedDistIndices[i]]
        print(sortedDistIndices[i])
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1
    maxCount = 0
    for key, value in classCount.items():
        if value > maxCount:
            maxCount = value
            maxIndex = key

    return maxIndex

if __name__ =='__main__':

    dataSet, labels = createDataSet()

    testX = array([1.2, 1.0])
    outputLabel = kNNClassify(testX, dataSet, labels, 3)
    print "Your input is:", testX, "and classified to class: ", outputLabel
