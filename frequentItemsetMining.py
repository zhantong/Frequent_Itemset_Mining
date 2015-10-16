class FreItemMining():
	def __init__(self):
		self.item_count=None
		self.trans=[]
		self.get_trans()
	def get_trans(self):
		with open('assignment2-data.txt','r') as f:
			val=[int(x) for x in f.readline().split()]
			self.item_count=len(val)
			for line in f:
				t=[]
				for index,item in enumerate(line.split()):
					if item=='1':
						t.append(val[index])
				if t:
					self.trans.append(t)
				#print(trans)
		#print(len(self.trans))
		return self.trans
	def get_frequent_1(self):
		f1=[]
		for t in self.trans:
			for item in t:
				if [item] not in f1:
					f1.append([item])
			if len(f1)==self.item_count:
				break
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

	def apriori(self):
		frequent=self.get_frequent_1()
		while frequent:
			candidate=self.get_candidate(frequent)
			print(candidate)
if __name__=='__main__':
	test=FreItemMining()
	res=test.apriori()
	print(res)