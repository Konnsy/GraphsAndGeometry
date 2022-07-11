from statistics import mean

def interpolateBoxes(boxes):
	return [ mean([t[0] for t in boxes]),
			mean([t[1] for t in boxes]),
			mean([t[2] for t in boxes]),
			mean([t[3] for t in boxes]),
		]

def interpolateTwoBoxes(box1, box2, weightBox1=0.5):
    """
    weightBox1: higher values will consider box 1 stronger 
                than box 2. Must be a value between 0 and 1.
                Choose 0.5 for equal contribution.
    """
	return [box1[0]*weightBox1 + box2[0]*(1.0-weightBox1),
			box1[1]*weightBox1 + box2[1]*(1.0-weightBox1),
			box1[2]*weightBox1 + box2[2]*(1.0-weightBox1),
			box1[3]*weightBox1 + box2[3]*(1.0-weightBox1)]