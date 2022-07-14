import sys

def boxIoU(boxA, boxB):
    """
	Calculates the Intersection over Union value between to boxes.
	box format: [x1, y1, x2, y2]
	"""
	# compute the area of the intersecting rectangle
	dx = min(boxA[2], boxB[2]) - max(boxA[0], boxB[0])
	dy = min(boxA[3], boxB[3]) - max(boxA[1], boxB[1])
	if dx < 0 or dy < 0:
		return 0.0
	else:
		interArea = dx * dy

	# compute the area of both the prediction and ground-truth rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

	iou = interArea / float(boxAArea + boxBArea - interArea)
	return iou
