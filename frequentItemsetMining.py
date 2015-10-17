"""Frequent Itemset Mining的Apriori算法实现
原始数据集为transactions，包含n条transaction
由1-itemsets开始，递归找出frequent k-itemsets，并由此生成candidate (k+1)-itemsets
使用level-wise pruning trick对candidate (k+1)-itemsets进行剪枝
使用由candidate (k+1)-itemsets生成的hash tree，遍历transactions
得到candidate (k+1)-itemsets中每个itemset的support值，过滤不满足要求的itemset
从而生成frequent (k+1)-itemsets，继续递归直到frequent itemsets为空
则所有找到的符合support要求的itemset即为结果
结果写入到同级文件夹下result.txt文件
"""
"""
在Python 3.5(x64)下测试成功，理论上适合所有Python 3.x版本
"""


class Node():

    """hash tree节点类
    用来构建hash tree
    """

    def __init__(self, level):
        """必要的变量声明和赋值
        """
        Node.digree = 4  # 树的度
        Node.max_leaf = 6  # 叶子节点下itemset个数最大值
        self.isleaf = True  # 此节点是否为叶子节点
        self.level = level  # 此节点所在层级，树由上至下从0开始
        self.children = [None]*Node.digree  # 内部节点指向其子节点
        self.data = []  # 叶子节点中存储的itemset

    def add(self, t):
        """向此节点插入itemset
        递归过程，若确定插入到其子节点，则调用add_to_children()
        """
        if not self.isleaf:  # 此节点为内部节点则直接插入到子节点中
            self.add_to_children(t)
        else:
            if len(self.data) != Node.max_leaf:  # 如果叶子节点itemset未满则直接插入
                self.data.append(t)
                self.data.sort()  # 对itemset排序，为查找提供便利
            else:
                self.data.append(t)  # 将新itemset临时加入到data中，统一处理
                self.isleaf = False  # 变更为内部节点
                for t in self.data:  # 将此节点下所有itemset插入到其子节点中
                    self.add_to_children(t)
                self.data = []  # 清空此节点的data

    def add_to_children(self, t):
        """与add()相互调用的递归过程
        """
        mod = t[self.level] % Node.digree  # 求余运算确定插入到哪个子节点
        if not self.children[mod]:  # 子节点不存在则创建
            self.children[mod] = Node(self.level+1)
        self.children[mod].add(t)

    def query(self, t, width, part=[]):
        """在树中查找指定transaction的所有匹配的itemset
        递归过程
        返回所有符合的itemset，实际就是此transaction的子集
        part和t共同组成原始的transaction，因在树中查找时每下降一层，transaction中前一部分item即已经确定
        为了递归的方便，将已经确定的“头”保存在part中，未确定的部分保存在t中
        当找到叶子节点时，首先对“头”即part进行匹配，只有part匹配成功的才继续确定叶子节点中数据后面部分是否都在t中
        width为itemset的长度，为后面划分递归提供方便
        """
        result = []
        if self.isleaf:
            for data in self.data:
                flag_after = 0  # 因data中itemset有序，找到所有匹配项后就不必继续查找
                if data[:len(part)] == part:  # 因使用hash tree，此层需要匹配的前几个item是确定的
                    flag_after = 1
                    # 判断此itemset中后几个item是否全都在transaction中（此时transaction前一部分已经被移到part中）
                    flag_all_in = 1
                    for item in data[len(part):]:
                        if not item in t:
                            # 如果itemset中存在item不在transaction中，则不是其子集
                            flag_all_in = 0
                    if flag_all_in:
                        result.append(data)  # 如果都在transaction中，则加入到结果list中
                elif flag_after:
                    break
        else:  # 为内部节点则向下递归
            for index in range(len(t)+len(part)-width+1):  # 分成所有的子类
                temp = part[:]  # 防止python对list传递引用，此时确保为值传递，不对part造成影响
                temp.append(t[index])  # 向下递归一层则“头”又有一个item是确定的，将其加到part中
                mod = t[index] % Node.digree
                if self.children[mod]:  # 如果其对应子节点不存在则一定不存在匹配项，不考虑
                    result.extend(
                        self.children[mod].query(t[index+1:], width, temp))
        return result


class FreItemMining():

    """Frequent Itemset Mining
    包含Apriori算法的全部实现
    """

    def __init__(self, minsup):
        """初始化
        必要的变量声明和赋值
        读取原始数据并进行处理
        """
        self.minsup = minsup  # support阈值
        self.item_count = 0  # item数目
        self.trans = []  # 保存transactions
        self.trans_count = 0  # 保存所有transaction的个数
        self.get_trans()
        self.result = []  # 保存最终结果

    def get_trans(self):
        """读取原始数据并处理
        将原始数据读取为包含全部itemset的list
        如[[1,5],[2,5,6],...]
        """
        file_name = 'assignment2-data.txt'
        with open(file_name, 'r') as f:
            # 得到item名字的list，为了处理方便，将item值减1
            self.items = [int(x)-1 for x in f.readline().split()]
            self.item_count = len(self.items)
            for line in f:
                self.trans_count += 1  # 计算transaction个数
                t = []
                for index, item in enumerate(line.split()):
                    if item == '1':
                        t.append(self.items[index])
                if t:
                    self.trans.append(t)
        return self.trans

    def get_frequent_1(self):
        """找出frequent 1-itemsets
        首先找到candidate 1-itemsets
        遍历transacions，统计每个itemset出现次数
        将大于support阈值的itemset加入到结果，即为frequent 1-itemsets
        """
        c1 = {}  # candidate 1-itemsets
        for item in self.items:
            c1[item] = 0
        for t in self.trans:  # 遍历transacions
            for item in t:
                c1[item] += 1
        f1 = []  # frequent 1-itemsets
        for item in c1:
            support = c1[item]/self.trans_count  # 计算support
            if support >= self.minsup:
                f1.append([item])
                # 将满足要求的itemset同时加入到最终结果中
                self.result.append(([item], support))
        return sorted(f1)

    def get_candidate(self, freq):
        """对指定的frequent k-itemsets，找到candidate (k+1)-itemsets
        因itemsets有序，只需要比较itemset中的前k-1项，相同则分别加入两项的最后一个item，形成(k+1)-itemset
        两层循环即可
        """
        candi = []  # candidate (k+1)-itemsets
        length = len(freq[0])-1  # k-1
        for first in range(len(freq)-1):
            for second in range(first+1, len(freq)):
                # 两个k-itemset的前(k-1)项是否匹配
                if freq[first][0:length] == freq[second][0:length]:
                    new = freq[first][0:length]  # 临时变量
                    f = freq[first][length]  # 前一项的最后一个item
                    s = freq[second][length]  # 后一项的最后一个item
                    # 排序并加入到临时变量中，形成(k+1)-itemset
                    if f < s:
                        new.extend([f, s])
                    else:
                        new.extend([s, f])
                    candi.append(new)
                else:
                    break
        return candi

    def prune(self, candi, freq):
        """level-wise pruning trick
        对生成的candidate (k+1)-itemsets进行剪枝
        candidate (k+1)-itemsets中任一(k+1)-itemset的长度为k的子集即k-itemsets必在frequent k-itemsets中
        否则不满足candidate的定义，这样可以对candidate进行剪枝
        """
        for c in candi:
            for i in range(len(c)):  # 遍历此(k+1)-itemset的所有k-itemset子集
                temp = c[:i]+c[i+1:]  # 消去第i个item
                if temp:
                    # 如果存在k-itemset不在frequent k-itemsets中则在candidate中删去
                    if temp not in freq:
                        candi.remove(c)
                        break
        return candi

    def support(self, candi):
        """计算candidate中所有itemset的support值
        返回满足support要求的itemsets，即为frequent
        """
        if not candi:  # candidate为空则直接返回
            return
        tree = Node(0)  # 建立hash tree根节点
        for c in candi:  # 遍历candidate建树
            tree.add(c)

        counts = [0]*len(candi)  # 创建一个和candidate一样长的list，记录对应itemset的匹配次数
        for t in self.trans:  # 遍历transactions
            # 如果此transaction中item个数比candidate中item个数还少则不可能匹配
            if len(t) >= len(candi[0]):
                res = tree.query(t, len(candi[0]))  # 得到此transaction的所有匹配项
                for c in res:  # 在counts中计数
                    counts[candi.index(c)] += 1
        f = []  # frequent itemsets
        for index, count in enumerate(counts):
            support = count/self.trans_count  # 计算support
            if support >= self.minsup:
                f.append(candi[index])
                # 将满足要求的itemset同时加入到最终结果中
                self.result.append((candi[index], support))
        return f

    def write_out_result(self):
        """将最终满足support要求的所有结果及其support值写入到文件
        """
        file_name = 'result.txt'
        with open(file_name, 'w') as f:
            for res, support in sorted(self.result):
                for item in res:
                    item += 1  # 修正item值
                    f.write('%i ' % item)
                f.write('%.3f\n' % support)
        print('write the result to %s success.' % file_name)

    def apriori(self):
        """Apriori算法
        """
        frequent = self.get_frequent_1()  # 得到frequent 1-itemsets
        while frequent:  # frequent k-itemsets不为空则继续
            # 通过frequent k-itemsets找到candidate (k+1)-itemsets
            candidate = self.get_candidate(frequent)
            # 使用level-wise pruning trick对candidate (k+1)-itemsets剪枝
            candidate = self.prune(candidate, frequent)
            # 计算candidate (k+1)-itemsets的support值，返回满足条件的frequent
            # (k+1)-itemsets
            frequent = self.support(candidate)
        self.write_out_result()  # 将最终结果写入到文件
if __name__ == '__main__':
    mining = FreItemMining(minsup=0.144)  # 指定minsup
    mining.apriori()
