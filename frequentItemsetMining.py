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
				if item not in f1:
					f1.append(item)
			if len(f1)==self.item_count:
				break
		return sorted(f1)

	def get_candidate(self,freq):
		candi=[]
		length=len(freq[0])-1
		for index in len(freq)-1:
			if freq[index][0:length]==freq[index+1][0:length]:
				new=freq[index][0:length]
				if freq[index][length]<freq[index+1][length]:
					new.extend([freq[index][length],freq[index+1][length]])
				else:
					new.extend([freq[index+1][length],freq[index][length]])
				candi.append(new)
		return candi


if __name__=='__main__':
	test=FreItemMining()
	res=test.get_frequent_1()
	print(res)