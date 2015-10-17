class Node():
	def __init__(self,level):
		Node.digree=4
		Node.max_leaf=6
		self.isleaf=True
		self.level=level
		self.children=[None]*Node.digree
		self.data=[]
	def add(self,t):
		if not self.isleaf:
			self.add_to_children(t)
		else:
			if len(self.data)!=Node.max_leaf:
				self.data.append(t)
				self.data.sort()
			else:
				self.data.append(t)
				self.isleaf=False
				for t in self.data:
					self.add_to_children(t)
				self.data=[]
	def add_to_children(self,t):
		mod=t[self.level]%Node.digree
		if not self.children[mod]:
			self.children[mod]=Node(self.level+1)
		self.children[mod].add(t)

	def query(self,t,width,part=[]):
		result=[]
		if self.isleaf:
			for data in self.data:
				flag_after=0
				if data[:len(part)]==part:
					flag_after=1
					flag_all_in=1
					for item in data[len(part):]:
						if not item in t:
							flag_all_in=0
					if flag_all_in:
						result.append(data)
				elif flag_after:
					break
		else:
			for index in range(len(t)+len(part)-width+1):
				temp=part[:]
				temp.append(t[index])
				mod=t[index]%Node.digree
				if self.children[mod]:
					result.extend(self.children[mod].query(t[index+1:],width,temp))
		return result

class FreItemMining():
	def __init__(self,minsup):
		self.minsup=minsup
		self.item_count=0
		self.trans=[]
		self.trans_count=0
		self.get_trans()
		self.result=[]
	def get_trans(self):
		file_name='assignment2-data.txt'
		with open(file_name,'r') as f:
			self.items=[int(x)-1 for x in f.readline().split()]
			self.item_count=len(self.items)
			for line in f:
				self.trans_count+=1
				t=[]
				for index,item in enumerate(line.split()):
					if item=='1':
						t.append(self.items[index])
				if t:
					self.trans.append(t)
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
			support=c1[item]/self.trans_count
			if support>=self.minsup:
				f1.append([item])
				self.result.append(([item],support))
		return sorted(f1)

	def get_candidate(self,freq):
		candi=[]
		length=len(freq[0])-1
		for first in range(len(freq)-1):
			for second in range(first+1,len(freq)):
				if freq[first][0:length]==freq[second][0:length]:
					new=freq[first][0:length]
					f=freq[first][length]
					s=freq[second][length]
					if f<s:
						new.extend([f,s])
					else:
						new.extend([s,f])
					candi.append(new)
				else:
					break
		return candi
	def prune(self,candi,freq):
		for c in candi:
			for i in range(len(c)):
				temp=c[:i]+c[i+1:]
				if temp:
					if temp not in freq:
						candi.remove(c)
						break
		return candi
	def support(self,candi):
		if not candi:
			return
		tree=Node(0)
		for c in candi:
			tree.add(c)
		counts=[0]*len(candi)
		for t in self.trans:
			if len(t)>=len(candi[0]):
				res=tree.query(t,len(candi[0]))
				for c in res:
					counts[candi.index(c)]+=1
		f=[]
		for index,count in enumerate(counts):
			support=count/self.trans_count
			if support>=self.minsup:
				f.append(candi[index])
				self.result.append((candi[index],support))
		return f
	def write_out_result(self):
		file_name='result.txt'
		with open(file_name,'w') as f:
			for res,support in sorted(self.result):
				for item in res:
					f.write('%i '%item)
				f.write('%.3f\n'%support)
		print('write the result to %s success.'%file_name)

	def apriori(self):
		frequent=self.get_frequent_1()
		while frequent:
			candidate=self.get_candidate(frequent)
			candidate=self.prune(candidate,frequent)
			frequent=self.support(candidate)
		self.write_out_result()
if __name__=='__main__':
	mining=FreItemMining(minsup=0.144)
	mining.apriori()