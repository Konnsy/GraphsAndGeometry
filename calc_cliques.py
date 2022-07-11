
def calcCliques(edges, nodes):
	""" 
	edges: idx-edges of connected elements
	nodes: all node idxs existent
	result: list of node ids for each clique
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
		
									
	return cliques