import numpy as np
# 这里用于用户自定义一个将原数据转化为矩阵的方法
class Converter:
    def __init__(self, file_name, k:int):
        self.file_name = file_name
        self.data = self.convert(file_name)
        self.k = k
    # 得到文件矩阵
    def convert(self, file_name)->np.array:
        # todo 
        return np.random.randn(90)
    # 将向量分为l份, 这里要保证每份数据都是大小为k * x的，这样才可以用于(n, k)-EC
    def get_packetization_data(self, sub_packetization_level: int)->np.array:
        item_size = len(self.data) / sub_packetization_level
        packetization_data = [np.random.randn(self.k, 2) for _ in range(sub_packetization_level)]
        data = np.array(packetization_data)
        return data