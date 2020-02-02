import sys
import time


class SplayTree(object):
	def __init__(self):
		self.root = None

	def splay(self, node):

		node_value = node.value
		zig_zig = self.zig_zig
		zig_zag = self.zig_zag
		zig = self.zig

		while node_value != self.root.value:

			parent = node.parent
			parent_value = parent.value

			if self.root.value == parent_value:
			# single rotation
				zig(node, parent)
			else:
				grand_parent = parent.parent
				x = parent_value - node_value
				y = grand_parent.value - parent_value
				if x*y > 0:
					#zig zig
					#if x > 0:
					#right rotation first
					zig_zig(node, parent, grand_parent, x)
				else:
					#zig zag
					#if x > 0:
					#right rotation first
					zig_zag(node, parent, grand_parent, x)
		self.root.parent = None

	def delete(self, value):
		# now to delete the node in root
		# then splay max node in left subtree and replace
		node = self.find(value)
		self.splay(node)
		right = node.right

		if node.left is None:
			self.root = right
			self.root.parent = None
			#min_node = self.find_min()
			#self.splay(min_node)
		else:
			self.root = node.left
			self.root.parent = None
			max_node = self.find_max()
			self.splay(max_node)
			if right is not None:
				right.parent = max_node
				max_node.right = right

	def find(self, value):
		node = self.root
		while True:
			if node.value == value:
				return node
			else:
				if node.value > value:
					node = node.left
				else:
					node = node.right

	def find_max(self):
		node = self.root
		while True:
			if node.right is None:
				return node
			else:
				node = node.right

	def l_rotate(self, node, parent):
		if node.left is None:
			parent.right = None
		else:
			node.left.parent = parent
			parent.right = node.left

		if parent.parent is None:
			self.root = node
		else:
			node.set_parent(parent.parent)
		parent.parent = node
		node.left = parent

	def r_rotate(self, node, parent):
		if node.right is None:
			parent.left = None
		else:
			node.right.parent = parent
			parent.left = node.right
		if parent.parent is None:
			self.root = node
		else:
			node.set_parent(parent.parent)
		parent.parent = node
		node.right = parent

	def zig(self, node, parent):
		if parent.value < node.value:
			# left rotation
			if node.left is None:
				parent.right = None
			else:
				node.left.parent = parent
				parent.right = node.left
			self.root = node
			parent.parent = node
			node.left = parent
		else:
			# right rotation
			if node.right is None:
				parent.left = None
			else:
				node.right.parent = parent
				parent.left = node.right
			self.root = node
			parent.parent = node
			node.right = parent

	def zig_zig(self, node, parent, grandparent, flag):
		if flag > 0:
			#self.r_rotate(parent, grandparent)
			if parent.right is None:
				grandparent.left = None
			else:
				parent.right.parent = grandparent
				grandparent.left = parent.right

			if grandparent.parent is None:
				grandparent.parent = parent
				parent.right = grandparent
				# self.r_rotate(node, parent)
				if node.right is None:
					parent.left = None
				else:
					node.right.parent = parent
					parent.left = node.right
				self.root = node
				parent.parent = node
				node.right = parent

			else:
				parent.set_parent(grandparent.parent)
				grandparent.parent = parent
				parent.right = grandparent
				# self.r_rotate(node, parent)
				if node.right is None:
					parent.left = None
				else:
					node.right.parent = parent
					parent.left = node.right
				node.set_parent(parent.parent)
				parent.parent = node
				node.right = parent
			#self.r_rotate(node, parent)
		else:
			#self.l_rotate(parent, grandparent)
			if parent.left is None:
				grandparent.right = None
			else:
				parent.left.parent = grandparent
				grandparent.right = parent.left

			if grandparent.parent is None:
				#self.root = node
				grandparent.parent = parent
				parent.left = grandparent
				# self.l_rotate(node, parent)
				if node.left is None:
					parent.right = None
				else:
					node.left.parent = parent
					parent.right = node.left
				self.root = node
				parent.parent = node
				node.left = parent
			else:
				parent.set_parent(grandparent.parent)
				grandparent.parent = parent
				parent.left = grandparent
				# self.l_rotate(node, parent)
				if node.left is None:
					parent.right = None
				else:
					node.left.parent = parent
					parent.right = node.left
				node.set_parent(parent.parent)
				parent.parent = node
				node.left = parent

	def zig_zag(self, node, parent, grandparent, flag):
		if flag > 0:
			#self.r_rotate(node, parent)
			if node.right is None:
				parent.left = None
			else:
				node.right.parent = parent
				parent.left = node.right

			#node.set_parent(parent.parent)
			node.parent = grandparent
			grandparent.right = node

			parent.parent = node
			node.right = parent
			#self.l_rotate(node, grandparent)
			if node.left is None:
				grandparent.right = None
			else:
				node.left.parent = grandparent
				grandparent.right = node.left

			if grandparent.parent is None:
				self.root = node
			else:
				node.set_parent(grandparent.parent)

			grandparent.parent = node
			node.left = grandparent
		else:
			#self.l_rotate(node, parent)
			if node.left is None:
				parent.right = None
			else:
				node.left.parent = parent
				parent.right = node.left

			#node.set_parent(parent.parent)
			node.parent = grandparent
			grandparent.left = node

			parent.parent = node
			node.left = parent

			#self.r_rotate(node, grandparent)
			if node.right is None:
				grandparent.left = None
			else:
				node.right.parent = grandparent
				grandparent.left = node.right
			if grandparent.parent is None:
				self.root = node
			else:
				node.set_parent(grandparent.parent)
			grandparent.parent = node
			node.right = grandparent

	def get_depth(self):
		depth = -1
		if self.root is None:
			return depth
		else:
			step = [self.root]
			while step:
				next_step = []
				for node in step:
					if node.left is not None:
						next_step.append(node.left)
					if node.right is not None:
						next_step.append(node.right)
				depth += 1
				step = next_step
		return depth

	def insert(self, value):
		node = self.root
		while True:
			if value > node.value:
				if node.right is None:
					node.right = SplayNode(value)
					node.right.parent = node
					self.splay(node.right)
					break
				else:
					#self.right.insert(value, tree)
					node = node.right
			else:
				if node.left is None:
					node.left = SplayNode(value)
					node.left.parent = node
					self.splay(node.left)
					break
				else:
					#self.left.insert(value, tree)
					node = node.left

	# def get_string(self):
	# 	if self.root is not None:
	# 		step = [self.root]
	# 		result = ""
	# 		while step:
	# 			next_step = []
	# 			for node in step:
	# 				result += "{}".format(node.value) + " "
	# 				if node.left is not None:
	# 					next_step.append(node.left)
	# 				if node.right is not None:
	# 					next_step.append(node.right)
	# 			result += "\n"
	# 			step = next_step
	# 	else:
	# 		result = ""
	# 	return result


class ZigSplayTree(SplayTree):
	def splay(self, node):
		zig = self.zig
		node_value = node.value
		while node_value != self.root.value:
			# single rotation
			zig(node, node.parent)
		self.root.parent = None

	def zig(self, node, parent):
		if parent.value < node.value:
			# left rotation
			if node.left is None:
				parent.right = None
			else:
				node.left.parent = parent
				parent.right = node.left
			if parent.parent is None:
				self.root = node
			else:
				node.set_parent(parent.parent)
			parent.parent = node
			node.left = parent
		else:
			# right rotation
			if node.right is None:
				parent.left = None
			else:
				node.right.parent = parent
				parent.left = node.right

			if parent.parent is None:
				self.root = node
			else:
				node.set_parent(parent.parent)
			parent.parent = node
			node.right = parent


class SplayNode:

	def __init__(self, value=None):
		self.left = None
		self.right = None
		self.value = value
		self.parent = None

	def set_parent(self, parent):
		self.parent = parent
		if parent.value < self.value:
			parent.right = self
		else:
			parent.left = self


def get_input():
	N = int(sys.stdin.readline())
	input = sys.stdin.readline()
	commands = input.split(" ")
	return commands


if __name__ == "__main__":
	start = time.time()

	tree = SplayTree()
	zig_tree = ZigSplayTree()
	commands = get_input()

	tree.root = SplayNode(int(commands[0]))
	zig_tree.root = SplayNode(int(commands[0]))

	max_commands = len(commands)

	delete = tree.delete
	zig_delete = zig_tree.delete

	for i in range(1, max_commands):
		command = int(commands[i])
		if command > 0:
			tree.insert(command)
			zig_tree.insert(command)
		else:
			delete(abs(command))
			zig_delete(abs(command))

	# for i in range(1, max_commands):
	# 	command = int(commands[i])
	# 	if command > 0:
	# 		zig_tree.insert(command)
	# 		pass
	# 	else:
	# 		zig_delete(abs(command))
	# 		pass

	depth = tree.get_depth()
	depth_zig = zig_tree.get_depth()
	print("{} {}".format(depth, depth_zig))
	end = time.time()
	print("Total time: {} s".format(end - start))
