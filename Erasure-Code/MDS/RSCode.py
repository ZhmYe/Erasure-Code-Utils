import numpy as np
# (n, k) RS-Code
class RSCode:
    def __init__(self,n,k):
        self.n = n # 分块总量
        self.k = k # 原数据分块
        self.m = self.n - self.k # 冗余数据块
        self.generate_matrix = self.get_generate_matrix()
    def get_generate_matrix(self)->np.array:
        # 原数据为k * x，我们要得到n * x = (k + m) * x的encode_data
        # 那么乘的变换矩阵大小为(k + m) * k
        # 上面是k * k的单位阵
        E = np.eye(self.k)
        # 下面是一个m * k的范德蒙德矩阵
        # 这里需要指定范德蒙德矩阵每一行的x_i是多少
        # 这里就暂时写成1,2....
        x = np.array(list(range(1, self.m + 1)))
        vandor = np.vander(x, N=self.k, increasing=True)
        # print(E)
        # print(vandor)
        return np.vstack((E, vandor))
    def encode(self, data: np.array)->np.array:
        return np.dot(self.generate_matrix, data)
    def decode(self, encode_data:np.array, indexes: list)->np.array:
        # 这里我们需要知道encoded_data对应着哪几行,通过list给出
        assert(len(encode_data) == len(indexes)) # 如果长度不一样无法还原
        assert(len(encode_data) >= self.k) # 最少需要k个
        # 这里需要保证有序
        indexed_data = sorted(zip(indexes, encode_data), key=lambda x: x[0])
        # 提取排序后的encode_data
        # sorted_encode_data = [data for _, data in indexed_data]
        # 遍历所有index，我们只需要k个就可以
        decoded_matrix = []
        to_decoded_data = []
        for index, data in indexed_data[:self.k]:
            decoded_matrix.append(self.generate_matrix[index])
            to_decoded_data.append(data)
        decoded_matrix = np.array(decoded_matrix)
        to_decoded_data = np.array(to_decoded_data)
        return np.dot(np.linalg.inv(decoded_matrix), to_decoded_data) 
# r.get_generate_matrix()
# r = RSCode(9,6)
# print(r.decode(r.encode(np.array([1,2,3.46464,4,5,6])), list(range(9))))