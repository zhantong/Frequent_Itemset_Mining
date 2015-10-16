MINSUP=0.144
def trick():
	txt=''
	with open('assignment2-data.txt','r') as f:
		txt=[x.strip().replace(' ','') for x in f]
	txt=txt[1:]
	length=len(txt[0])
	n=1<<length
	ways=[]
	for i in range(1,n):
		ways.append(bin(i)[2:].zfill(length))
	for way in ways:
		count=0
		for line in txt:
			if int(line,2)&int(way,2)==int(way,2):
				count+=1
		if count>=MINSUP*len(txt):
			print(way,count/len(txt))
if __name__=='__main__':
	trick()