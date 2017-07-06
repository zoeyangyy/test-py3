# -*- coding: utf-8 -*-

"""

@author: zoeyang

@contact: zoeyang@163.com

@file: kNN.py

@time: 2017/7/3 下午4:00

@desc: 第二章 k-邻近算法

"""
import numpy
import operator
from os import listdir
import matplotlib
import matplotlib.pyplot as plt


def createDataSet():
    group = numpy.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet

    # sqDiffMat = diffMat**2
    # sqDistances = sqDiffMat.sum(axis=1)
    # distances = sqDistances**0.5
    # or
    distances = numpy.sqrt(numpy.sum(numpy.square(diffMat),axis=1))

    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0)+1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename, 'r')
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = numpy.zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip().split('\t')
        returnMat[index] = line[0:3]
        classLabelVector.append(int(line[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = numpy.zeros(numpy.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - numpy.tile(minVals, (m,1))
    normDataSet = normDataSet/numpy.tile(ranges, (m,1))
    return normDataSet, ranges, minVals


def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('ml-in-action/Ch02/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("the total error rate is: %f" % (errorCount/float(numTestVecs)))


def draw_plot():
    datingDataMat, datingLabels = file2matrix('ml-in-action/Ch02/datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*numpy.array(datingLabels),15.0*numpy.array(datingLabels))
    plt.show()


def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input("video games?"))
    ffMiles = float(input("flier miles?"))
    iceCream = float(input("ice cream?"))
    datingDataMat, datingLabels = file2matrix('ml-in-action/Ch02/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = numpy.array([ffMiles, percentTats, iceCream])
    classifyresult = classify0((inArr-minVals)/ranges, normMat, datingLabels, 3)
    print("result: " + resultList[classifyresult-1])


def img2vector(filename):
    returnVect = numpy.zeros((1, 1024))
    fr = open(filename,'r')
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i+j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('ml-in-action/Ch02/digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = numpy.zeros((m,1024))
    for i in range(m):
        file = trainingFileList[i].split('.')[0]
        classNumStr = int(file.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i] = img2vector('ml-in-action/Ch02/digits/trainingDigits/'+trainingFileList[i])
    testFileList = listdir('ml-in-action/Ch02/digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        file = testFileList[i].split('.')[0]
        classNumStr = int(file.split('_')[0])
        vectorUnderTest = img2vector('ml-in-action/Ch02/digits/testDigits/'+testFileList[i])
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        # print("classifier is %d, the real answer is %d" % (classifierResult, classNumStr))
        if classNumStr != classifierResult:
            errorCount += 1
    print("error number is "+ str(errorCount))
    print("error rate is"+ str(errorCount/mTest))

handwritingClassTest()
