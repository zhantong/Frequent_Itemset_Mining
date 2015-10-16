def get_trans():
	trans=[]
	with open('assignment2-data.txt','r') as f:
		val=f.readline().split()
		for line in f:
			t=[]
			for index,item in enumerate(line.split()):
				if item=='1':
					t.append(val[index])
			trans.append(t)
	return trans
if __name__=='__main__':
	get_trans()