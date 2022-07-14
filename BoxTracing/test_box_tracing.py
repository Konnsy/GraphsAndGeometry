import numpy as np
from box_tracing import BoxTracer

def test_BoxTracer1():
    bbt = BoxTracer(minLenTraces=2, iouThreshold=0.1, distTolerance=0)
    
    b1 = [0,0,1,1]
    b2 = [2,2,3,3]
    b3 = [4,4,5,5]

    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1,b2])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([b2,b3])
    assert len(bbt.calculateTraces()) == 2
    bbt.addToTraces([b3])
    assert len(bbt.calculateTraces()) == 3


def test_BoxTracer2():
    bbt = BoxTracer(minLenTraces=2, iouThreshold=0.1, distTolerance=0)
    
    b1 = [0,0,1,1]
    b2 = [2,2,3,3]
    b3 = [4,4,5,5]
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b2])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b3])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0


def test_BoxTracer3():
    bbt = BoxTracer(minLenTraces=3, iouThreshold=0.1, distTolerance=0)
    
    b1 = [0,0,1,1]
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 1


def test_BoxTracer4():
    bbt = BoxTracer(minLenTraces=1, iouThreshold=0.1, distTolerance=1)
    
    b1 = [0,0,1,1]
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 1


def test_BoxTracer5():
    bbt = BoxTracer(minLenTraces=2, iouThreshold=0.1, distTolerance=2)
    
    b1 = [0,0,1,1]
    b2 = [2,2,3,3]
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1,b2])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 1
    bbt.addToTraces([b2])
    assert len(bbt.calculateTraces()) == 2


def test_BoxTracer6():
    bbt = BoxTracer(minLenTraces=3, iouThreshold=0.1, distTolerance=3)
    
    b1 = [0,0,1,1]
    b2 = [2,2,3,3]
    bbt.addToTraces([b1,b2])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b1,b2])
    assert len(bbt.calculateTraces()) == 2


def test_BoxTracer7():
    bbt = BoxTracer(minLenTraces=2, iouThreshold=0.1, distTolerance=2)
    
    b1 = [0,0,1,1]
    b2 = [2,2,3,3]
    b3 = [4,4,5,5]
    b4 = [5,5,6,6]
    bbt.addToTraces([b1])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b2])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b3])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b4])
    assert len(bbt.calculateTraces()) == 0
    bbt.addToTraces([b2, b1, b3, b4])  # b1 out of reach
    assert len(bbt.calculateTraces()) == 3


def test_BoxTracer_speed():
    import random
    import time

    bbt = BoxTracer(minLenTraces=7, iouThreshold=0.1, distTolerance=5)

    numBoxesTotal = 0

    numFrames = 1000
    for _ in range(numFrames):
        numBoxes = random.randint(0, 100)
        numBoxesTotal += numBoxes
        for _ in range(numBoxes):
            sideLen = 10
            x1 = random.randint(0, 800-sideLen-1)
            y1 = random.randint(0, 600-sideLen-1)
            bbt.addToTraces([[x1, y1, x1+sideLen, y1+sideLen]])

    tBegin = time.time()
    numTraces = len(bbt.calculateTraces())
    tDiff = time.time() - tBegin

    print("calculated {:d} traces for {:d} boxes on {:d} frames in {:.3f}s".format(
        numTraces, numBoxesTotal, numFrames, tDiff))


test_BoxTracer1()
test_BoxTracer2()
test_BoxTracer3()
test_BoxTracer4()
test_BoxTracer5()
test_BoxTracer6()
test_BoxTracer7()
test_BoxTracer_speed()