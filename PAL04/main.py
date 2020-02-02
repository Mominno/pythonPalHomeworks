import sys
import math
import copy
from collections import deque


class Graph:
	def __init__(self, N, M):
		self.vertices = [[] for k in range(N)]
		self.labels = [None for k in range(N)]
		self.labelPile = [[] for k in range(N)]
		self.state = [0 for k in range(N)]
		self.previous = [0 for k in range(N)]
		self.step = [math.inf for k in range(N)]
		self.vertNum = N
		self.path = []
		self.cycleNodes = []

		self.notInCycle = [True for k in range(N)]

		for i in range(M):
			edgeString = sys.stdin.readline()
			splitList = edgeString.split(" ")
			j = int(splitList[0])
			k = int(splitList[1])
			self.vertices[j - 1].append(k - 1)
			self.vertices[k - 1].append(j - 1)

	def getValueString(self):
		root = self.findRootNode()
		cert = self.evaluateFromRoot(root)
		return cert

	def findRootNode(self):
		cycleNodes = self.getCycleNodes()
		for node in cycleNodes:
			self.notInCycle[node] = False

		vert = self.vertices

		for v in range(self.vertNum):
			if len(vert[v]) == 1:
				continue
			#elif v not in cycleNodes:
			elif self.notInCycle[v]:
				return v
		return None

	def getCycleNodes(self):
		vert = self.vertices
		for i in range(self.vertNum):
			self.path = []
			if len(vert[i]) == 1:
				continue
			elif self.state[i] == 0:
				self.DFS(i)
		return self.cycleNodes

	def DFS(self, v):
		self.path.append(v)
		self.state[v] = 1
		#prev = self.previous
		for i in self.vertices[v]:
			if self.state[i] == 1 and self.previous[v] != i and i not in self.cycleNodes:
				ind = self.path.index(i)
				self.cycleNodes += self.path[ind:]

			if self.state[i] == 0 and len(self.vertices[i]) != 1:
				self.previous[i] = v
				self.DFS(i)
		self.path.pop()

	def BFS(self, root):
		self.previous = [[] for k in range(self.vertNum)]
		self.state = [0 for k in range(self.vertNum)]
		queue = deque()
		queue.append(root)
		self.step[root] = 0
		layerList = []
		append = queue.append
		popleft = queue.popleft
		layerapp = layerList.append

		while queue:
			node = popleft()
			self.state[node] = 1
			if self.step[node] >= len(layerList):
				layerapp([node])
			else:
				layerList[self.step[node]].append(node)

			for i in self.vertices[node]:
				if self.state[i] == 0:
					self.previous[i].append(node)
					self.step[i] = self.step[node] + 1
					self.state[i] = 1
					append(i)
				elif self.state[i] == 1 and self.step[i] == self.step[node] + 1:
					self.previous[i].append(node)
		return layerList

	def evaluateFromRoot(self, root):
		layerList = self.BFS(root)
		layer = len(layerList)
		processLaterList = []
		processLaterDict = {}

		cyclenum = self.getCycleNumber
		evaluate = self.evaluateNode
		procappend = processLaterList.append
		reeval = self.reEvaluateNode
		prev = self.previous
		strJoin = "".join

		label = self.labels
		pile = self.labelPile

		while layer > 1:
			layer -= 1
			for node in layerList[layer]:
				if len(prev[node]) == 1:
					parent = prev[node][0]
					evaluate(node, parent, strJoin, label, pile)
				else:
					procappend(node)

		for node in processLaterList:
			cyclenumber = cyclenum(node)
			if cyclenumber in processLaterDict:
				processLaterDict[cyclenumber].append(node)
			else:
				processLaterDict[cyclenumber] = [node]

		processLaterKeys = list(processLaterDict.keys())
		processLaterKeys.sort(reverse=True)

		for key in processLaterKeys:
			nodeList = processLaterDict[key]

			for node in nodeList:
				parent1 = prev[node][0]
				parent2 = prev[node][1]
				next1 = prev[parent1][0]
				next2 = prev[parent2][0]

				branchList = [[parent1, next1],[parent2, next2]]
				while next1 != next2:
					next1 = prev[next1][0]
					next2 = prev[next2][0]
					branchList[0].append(next1)
					branchList[1].append(next2)

				if label[branchList[0][-2]] > label[branchList[1][-2]]:
					#parent1
					pile[node].sort()
					nodeLabels = ["0", *self.labelPile[node], "1"]

					label[node] = strJoin(nodeLabels)
					pile[parent1].append(label[node])

					startNode = parent1
					parent = prev[startNode][0]

					while len(prev[parent]) == 1:
						reeval(startNode, parent, strJoin)
						startNode = parent
						parent = prev[parent][0]
					if self.step[parent] == 1:
						evaluate(startNode, parent, label, pile)
						evaluate(parent, prev[parent], label, pile)
					else:
						pile[parent].append(label[startNode])

				else:
					#parent2
					self.labelPile[node].sort()
					nodeLabels = ["0", *self.labelPile[node], "1"]

					label[node] = strJoin(nodeLabels)
					pile[parent2].append(label[node])

					startNode = parent2
					parent = prev[startNode][0]
					while len(prev[parent]) == 1:
						reeval(startNode, parent, strJoin)
						startNode = parent
						parent = prev[parent][0]
					if self.step[parent] == 1:
						evaluate(startNode, parent, strJoin, label, pile)
						evaluate(parent, prev[parent], strJoin, label, pile)
					else:
						pile[parent].append(label[startNode])

		pile[root].append("1")
		pile[root].sort()
		pile[root].insert(0, "0")
		return "".join(pile[root])

	def reEvaluateNode(self, startNode, parentNode, strJ):
		self.labelPile[startNode].sort()
		nodeLabels = ["0", *self.labelPile[startNode], "1"]
		self.labelPile[parentNode].remove(self.labels[startNode])
		self.labels[startNode] = strJ(nodeLabels)
		self.labelPile[parentNode].append(self.labels[startNode])

	def getCycleNumber(self, node):
		prev = self.previous
		parent1 = prev[node][0]
		parent2 = prev[node][1]
		next1 = prev[parent1][0]
		next2 = prev[parent2][0]
		branchDict = {}
		branchDict[parent1] = [parent1, next1]
		branchDict[parent2] = [parent2, next2]
		while next1 != next2:
			next1 = prev[next1][0]
			next2 = prev[next2][0]
			branchDict[parent1].append(next1)
			branchDict[parent2].append(next2)
		return self.step[next1]

	def evaluateNode(self, node, parent, strJ, labels, pile):
		if pile[node]:
			pile[node].sort()
			nodeLabels = ["0", *pile[node], "1"]
			labels[node] = strJ(nodeLabels)
			pile[parent].append(labels[node])
		else:
			pile[parent].append("01")


class GraphIsomorphismSolver:
	def __init__(self):
		self.graphs = []
		self.cert = []
		self.graphNumber = 0
		self.getInput()

	def getInput(self):
		edge = sys.stdin.readline()
		T, N, M = edge.split(" ")
		T = int(T)
		N = int(N)
		M = int(M)
		self.graphNumber = T
		for i in range(T):
			self.graphs.append(Graph(N, M))
		self.cert = [None for i in range(T)]

	def solve(self):
		for i in range(self.graphNumber):
			self.cert[i] = self.graphs[i].getValueString()
		result = self.getGraphIsomorphisms()
		print(*result)

	def getGraphIsomorphisms(self):
		final = {}
		for cert in self.cert:
			if cert in final:
				final[cert] += 1
			else:
				final[cert] = 1
		finalVal = list(final.values())
		finalVal.sort()
		return finalVal


if __name__ == "__main__":
	g = GraphIsomorphismSolver()
	g.solve()
