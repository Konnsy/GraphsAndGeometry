
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
