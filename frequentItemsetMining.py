MINSUP=0.144
DIGREE=4
MAX_LEAF=6
class Node():
	def __init__(self,level):
		self.isleaf=True
		self.level=level
		self.children=[None]*DIGREE
		self.data=[]
	def add(self,t):
		if not self.isleaf:
			mod=t[self.level]%DIGREE
			if not self.children[mod]:
				self.children[mod]=Node(self.level+1)
			self.children[mod].add(t)
		else:
			if len(self.data)!=MAX_LEAF:
				self.data.append(t)
				self.data.sort()
			else:
				self.data.append(t)
				self.isleaf=False
				#print(self.isleaf,self.level,self.children,self.data,t)
				for t in self.data:
					mod=t[self.level]%DIGREE
					if not self.children[mod]:
						self.children[mod]=Node(self.level+1)
					self.children[mod].add(t)
				self.data=[]
	def query(self,t,width,part=[]):
		result=[]
		if self.isleaf:
			for data in self.data:
#				print(part,t,data)
#				flag=1
#				if data[:self.level]==part:
#					for item in data[self.level:]:
#						if item not in t:
#							flag=0
#					if flag:
#						result.append(data)
				flag=1
				for item in data:
					if item not in t:
						flag=0
				if flag:
					result.append(data)
		else:
			for index in range(len(t)-width+1):
				mod=t[index]%DIGREE
				if self.children[mod]:
#					temp=part
#					temp.append(t[0])
#					result.extend(self.children[mod].query(t[1:],width,temp))
					result.extend(self.children[mod].query(t,width,part))
		return result
class Tree():
	def __init__(self):
		self.head=Node()

class FreItemMining():
	def __init__(self):
		self.item_count=None
		self.trans=[]
		self.trans_count=0
		self.get_trans()
	def get_trans(self):
		with open('assignment2-data.txt','r') as f:
			self.items=[int(x) for x in f.readline().split()]
			self.item_count=len(self.items)
			for line in f:
				self.trans_count+=1
				t=[]
				for index,item in enumerate(line.split()):
					if item=='1':
						t.append(self.items[index])
				if t:
					self.trans.append(t)
				#print(self.trans)
		#print(len(self.trans))
		return self.trans
	def get_frequent_1(self):
		c1={}
		for item in self.items:
			c1[item]=0
		for t in self.trans:
			for item in t:
				c1[item]+=1
		f1=[]
		for item in c1:
			if c1[item]/self.trans_count>=0.144:
				f1.append([item])
		return sorted(f1)

	def get_candidate(self,freq):
		candi=[]
		length=len(freq[0])-1
		for first in range(len(freq)-1):
			for second in range(first+1,len(freq)):
				if freq[first][0:length]==freq[second][0:length]:
					new=freq[first][0:length]
					if freq[first][length]<freq[second][length]:
						new.extend([freq[first][length],freq[second][length]])
					else:
						new.extend([freq[second][length],freq[first][length]])
					candi.append(new)
				else:
					break
		return candi
	def prune(self):
		pass
	def support(self,candi):
		print(candi)
		tree=Node(0)
		for c in candi:
			tree.add(c)
		support=[0]*len(candi)
		for t in self.trans:
			for c in tree.query(t,len(candi[0])):
				#print(c)
				support[candi.index(c)]+=1
		print(support)

	def apriori(self):
		frequent=self.get_frequent_1()
		#print(frequent)
		while frequent:
			candidate=self.get_candidate(frequent)
			self.support(candidate)
			break
if __name__=='__main__':
	test=FreItemMining()
	res=test.apriori()
	#print(res)