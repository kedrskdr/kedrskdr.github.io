class onemoreSuffixAutomaton(): 
	def __init__(self):
		pass



	def SuffixAutomaton(self,s):
		edges = []  #: the labeled edges from node i
		link = []			#// link[i]   : the parent of i
		length = []		  #// length[i] : the length of the longest string in the ith class
					   #// the index of the equivalence class of the whole string

		# add the initial node
		edges.append({})
		link.append(-1)
		length.append(0)
		last = 0

		for i in range (len(s)):
		# construct r
			edges.append({})
			length.append(i+1)
			link.append(0)
			r = len(edges)- 1

# add edges to r and find p with link to q
			p = last;
			while p >= 0 and not s[i] in edges[p]:
				edges[p][s[i]] = r
				p = link[p]

			if p != -1:
				q = edges[p][s[i]]
				if length[p] + 1 == length[q]: 
				# we do not have to split q, just set the correct suffix link
					link[r] = q
				else:
					# we have to split, add q'
					edges.append(edges[q]) # copy edges of q
					length.append(length[p] + 1)
					link.append(link[q]) # copy parent of q
					qq = len(edges)-1
					# add qq as the new parent of q and r
					link[q] = qq
					link[r] = qq
					# move short classes pointing to q to point to q'
					print(edges[p])
					while p >= 0 and edges[p][s[i]] == q:  
						edges[p][s[i]] = qq
						p = link[p]
						print("\t",edges[p])
				  
			
			last = r
		return edges

