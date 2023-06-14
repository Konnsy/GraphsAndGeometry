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


def isBoxContained(boxA, boxB):
	"""
	Checks if boxA contains boxB
	box format: [x1, y1, x2, y2]
	"""
	return isPointContained(boxA, (boxB[0], boxB[1])) and isPointContained(boxA, (boxB[2], boxB[3]))


def isPointContained(box, point):
	"""
	Checks if box contains (x,y)-coordinate tuple point
	box format: [x1, y1, x2, y2], point format: [x,y]
	"""
	return point[0] >= box[0] and point[0] <= box[2] and point[1] >= box[1] and point[1] <= box[3]


def mergeBoxesByIoU(boxes, iouThreshold):
	"""
	Merges boxes from a list. A merged box will replace a set of boxes that have 
	an IoU value greater than iouThreshold with each other.
	box format: [x1, y1, x2, y2]
	"""
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


def calcCliques(edges, nodes):
	"""
	Calculates cliques in a graph given by a list of edges and a list of nodes.

	edges: edges of connected elements, format: (idx node 1, idx node 2)
	nodes: all node idxs existent, format: int as id
	result: sorted list of node ids for each clique


	Example usage:
		> edges = [[1,2], [2,5], [3,0], [5,6]]
		> nodes = [0,1,2,3,4,5,6]

		> cliques = calcCliques(edges, nodes)
		=> cliques returns [[1, 2, 5, 6], [0, 3], [4]]
	"""
	nodes.sort()
	
	# initialize connections directory
	con = {}
	for (a,b) in edges:
		if a in con:
			con[a].add(b)
		else:
			con[a] = set()
			con[a].add(b)

	# merge until nothing to merge is found
	changed = True
	while changed:
		changed = False

		for idx1 in range(len(nodes)-1, 0, -1):			
			for idx2 in range(min(len(nodes), idx1)):								
				if nodes[idx1] in con and nodes[idx2] in con and nodes[idx1] in con[nodes[idx2]]:
					con[nodes[idx2]].update(con[nodes[idx1]])
					del con[nodes[idx1]]
					changed = True
	
	inClique = set()
	for valList in con.values():
		inClique.update(valList)	
	inClique.update(con.keys())

	cliques = []
	for node in nodes:
		if node in con:
			cliques.append([node]+list(con[node]))
		elif not (node in inClique):
			cliques.append([node])

	for idx in range(len(cliques)):
		cliques[idx].sort()

	return cliques