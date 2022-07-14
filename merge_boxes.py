import sys
from calc_cliques import calcCliques
from calc_iou import boxIoU

def mergeBoxes(boxes):
	"""
	Merges a list of boxes.
	box format: [x1, y1, x2, y2]
	"""
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