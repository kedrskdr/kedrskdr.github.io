from suffix_tree import *
class AhoNode:
	# Вспомогательный класс для построения дерева
	
	def __init__(self,number):#Self ссылается на экземпляр класса для которого вызывается метод.
		global COUNT
		self.goto = {} # goto g (s, a) указывает, в какое состояние переходить из данного состояния s при просмотре символа a.
		self.out = [] #out (s) выдает множество шаблонов, которые обнаруживаются при переходе в состояние s.
		self.fail = None #f (s) указывает, в какое состояние переходить при просмотре неподходящего символа
		self.zeile = number
	def __repr__(self):
		return str(self.zeile)
	
	def __str__(self):
		return str(self.zeile)

class fsa:
	
	def __init__(self):
		self.out = []
		self.root = AhoNode(len(self.out))
		self.out.append(self.root)
		
	#for all sys calls
	def aho_create_forest(self,patterns):
		#Создать бор - дерево паттернов
		
		
		for i in range (len(patterns)):
			node=self.root
			path = patterns[i]
			st = SuffixTree(patterns[i])
			
			
			 #alle wege von erstem element
			
			q = [] #indexsuff tree
			q.append((0, self.root)) #index suff, root
			while len(q) != 0:
				symbol = q.pop() # (0,root)
				print("size of self.out ", len(self.out))
				mas_symb = []
				for g in st.edges.keys():
					if g[0] == symbol[0]:
						mas_symb.append(g)
					
				for j in range(len(mas_symb)):
					key_mas = st.edges[mas_symb[j]] #(0,0,0,0)
					curr_node = symbol[1] #[1] current state
					for jj in range(key_mas.first_char_index,key_mas.last_char_index+1):
						if patterns[i][jj] in curr_node.goto:
							curr_node = curr_node.goto[patterns[i][jj]]
						else:
							newnode = AhoNode(len(self.out))
							curr_node.goto[patterns[i][jj]] = newnode  
							self.out.append(newnode) #alle state 
					q.append((key_mas.dest_node_index,curr_node))		
	
	def addpattern(self,patterns):
			#Создать автомат Ахо-Корасика.
	#Фактически создает бор и инициализирует fail-функции
	#всех узлов, обходя дерево в ширину.
	
	# Создаем бор, инициализируем
	# непосредственных потомков корневого узла
	
		self.aho_create_forest(patterns)
		queue = []
		for node in self.root.goto.values():
			queue.append(node)
			node.fail = self.root
			#print(root.goto.values())
		# Инициализируем остальные узлы:
		# 1. Берем очередной узел (важно, что проход в ширину)
		# 2. Находим самую длинную суффиксную ссылку для этой вершины - это и будет fail-функция
		# 3. Если таковой не нашлось - устанавливаем fail-функцию в корневой узел
		while len(queue) > 0:
			rnode = queue.pop(0)
			
			for key, unode in rnode.goto.items():
				queue.append(unode)
				fnode = rnode.fail
				while fnode is not None and key not in fnode.goto:
					fnode = fnode.fail
				unode.fail = fnode.goto[key] if fnode else self.root
				unode.out += unode.fail.out

	def getnodecount(self):
		return len(self.out)
	
	def durchgehen(self,s):
		node = self.root
		for i in range (len(s)) :
			if s[i] in node.goto.keys():
				node = node.goto[s[i]]
			else:
				return False
		return True
				
		
		
		
		
			



