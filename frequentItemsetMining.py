MINSUP=0.144
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
	def apriori(self):
		frequent=self.get_frequent_1()
		#print(frequent)
		while frequent:
			candidate=self.get_candidate(frequent)
			print(candidate)
if __name__=='__main__':
	test=FreItemMining()
	res=test.apriori()
	print(res)