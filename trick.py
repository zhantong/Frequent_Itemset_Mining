"""Frequent Itemset Mining的另外一种方法
这就是很原始的方法，但得益于快速生成全排列和位运算，速度也是相当快
"""
MINSUP = 0.144


def trick():
    txt = ''
    with open('assignment2-data.txt', 'r') as f:
        txt = [x.strip().replace(' ', '')
               for x in f]  # 以每一行作为list中一个元素，并去除所有空格
    txt = txt[1:]  # 删去第一行说明
    length = len(txt[0])  # 得到每行item个数
    """
	下面是得出长度为length的全组合的所有情况
	"""
    n = 1 << length  # 位运算，得到十进制的n
    ways = []  # 存储所有组合情况
    for i in range(1, n):
        ways.append(bin(i)[2:].zfill(length))  # 将十进制转换为二进制字符串，消去前导0b，填充0对齐
    for way in ways:  # 对每种组合情况，计算出现次数（子集）
        count = 0
        for line in txt:  # 遍历提供的数据中的所有情况
            if int(line, 2) & int(way, 2) == int(way, 2):  # 转换为二进制整数，进行位运算
                count += 1
        if count >= MINSUP*len(txt):  # 如果达到最低support要求则输出
            print(way, count/len(txt))
if __name__ == '__main__':
    trick()
