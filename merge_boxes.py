import sys
from calc_cliques import calcCliques
from calc_iou import boxIoU

def mergeBoxes(boxes):
	if len(boxes)==0:
		return boxes

	x1 = sys.float_info.max
	y1 = sys.float_info.max
	x2 = sys.float_info.min 
	y2 = sys.float_info.min

	for box in boxes:
		x1 = min(x1, box[0])
		y1 = min(y1, box[1])
		x2 = max(x2, box[2])
		y2 = max(y2, box[3])

	return [x1, y1, x2, y2]

def mergeBoxesByIoU(boxes, iouThreshold):
		# find pairs which have an iou greater than the given threshold
		pairsToMerge = []
		for i in range(len(boxes)):
			for j in range(i+1, len(boxes)):
				if boxIoU(boxes[i], boxes[j]) >= iouThreshold:
					pairsToMerge.append([i,j])
		
		# merge boxes within each clique
		resBoxes = []
		cliques = calcCliques(pairsToMerge, [i for i in range(len(boxes))])
		for clique in cliques:
			if len(clique) == 1:
				resBoxes.append(boxes[clique[0]])
			elif len(clique) > 1:
				cliqueBoxes = [boxes[id] for id in clique]
				resBoxes.append(mergeBoxes(cliqueBoxes))

		return resBoxes
