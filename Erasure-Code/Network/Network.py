from MDS.RSCode import RSCode
from .Node import Node
from Converter.data_converter import Converter
import numpy as np
# 这里模拟节点网络
class Network:
    def __init__(self, n: int, k: int,  sub_packetization_level: int):
        # 所有的coder都必须要有encode和decode接口
        self.coder = RSCode(n, k)
        self.sub_packetization_level = sub_packetization_level
        self.nodes = [Node(id, sub_packetization_level) for id in range(n)]
        self.k = k
        self.n = n
        self.m = n - k
        self.full = False # 目前仅支持模拟一个文件，因此调用upload_file后将这里置为True   
        self.files = []
    # 模拟上传一个文件，然后返回该文件的矩阵表示
    def upload_file(self, file_name):
        if self.full:
            return False, None
        self.files.append(file_name)
        # 得到转化后的原数据矩阵
        converter = Converter(file_name, self.k)
        convert_data = converter.get_packetization_data(self.sub_packetization_level)
        # 使用纠删码进行encode，得到数据块和冗余块
        # todo 这里是直接按序存, 可以改成随机存储
        for i in range(len(convert_data)):
            packet_data = convert_data[i]
            encode_data = self.coder.encode(packet_data)
            for j in range(len(self.nodes)):
            # for j, node in self.nodes:
                node = self.nodes[j]
                node.set_packet(int(i), encode_data[j])
        return True, convert_data
    def detail(self):
        print("=========================Network Detailed=========================")
        for i in range(len(self.nodes)):
            node = self.nodes[i]
            for j in range(len(node.storage)):
                if not node.is_miss(j):
                    print("node {} packet {}: ".format(i, j), node.get_packet(j))
                else:
                    print("node {} packet {} is miss...".format(i, j))
        print("===========================Detailed End===========================")
    # 返回是否有缺失、缺失的index、未缺失的所有内容
    def get_file_data(self, file_name):
        # 目前仅有一个文件
        if file_name not in self.files:
            return False, list(range(self.sub_packetization_level)),None
        is_miss = False
        miss_indexes = []
        file_data = []
        for i in range(self.sub_packetization_level):
            count = 0
            # 可以是乱序的
            to_decoded_data_without_sort = []
            indexes = []
            for j in range(len(self.nodes)):
            # for j, node in self.nodes:
                node = self.nodes[j]
                if not node.is_miss(i):
                    count += 1
                    indexes.append(j)
                    to_decoded_data_without_sort.append(node.get_packet(i))
                # 只需要拿到k个即可，也可以更多，decode里可以支持
                if count == self.k:
                    break
            if count < self.k:
                is_miss = True
                miss_indexes.append(i)
            file_data.append(self.coder.decode(to_decoded_data_without_sort, indexes))
        return is_miss, miss_indexes, np.array(file_data)
