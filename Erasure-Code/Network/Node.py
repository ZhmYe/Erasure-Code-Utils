import numpy as np
# 这里简单表示每个节点存储的packet
# 可以设置丢失状态
class Packet:
    def __init__(self, id):
        self.pid = id
        self.access = True
        self.data = None
    # Packet是否能访问到
    def is_access(self)->bool:
        return self.access
    # 设置packet存储的数据
    def set_data(self, data: np.array):
        self.data = data
    # 模拟修复当前packet，比较恢复后的数据和原数据是否一致
    def try_repair(self, repair_data)->bool:
        return self.data == repair_data
    # 模拟丢失
    def miss(self):
        self.access = False
# 这里表示网络中的节点
# 可以设置节点活跃状态和内部packet丢失状态
class Node:
    # Params:
        # id: 节点id
        # sub_packetization_level，表示每个节点存储几个sub_packetization
            # 每个sub_packetization对应一个MDS
    def __init__(self, id: int, sub_packetization_level: int):
        self.id = id
        self.level = sub_packetization_level
        self.storage = [Packet(id) for id in range(self.level)]
        self.active = True
    # 节点是否活跃
    def is_active(self)->bool:
        return self.active
    # 设置某个packet的数据
    def set_packet(self, pid: int, data: np.array):
        self.storage[pid].set_data(data)
    # 判断packet是否丢失
    def is_miss(self, pid)->bool:
        return not self.storage[pid].is_access()
    # 返回当前Node有哪些packet丢失
    def check_packet_miss(self)->list:
        if not self.is_active():
            return list(range(self.level))
        miss_list = []
        for i, packet in self.storage:
            if not packet.is_access:
                miss_list.append(i)
        return miss_list
    # 尝试修复packet
    def repair_packet(self, pid: int, repair_data: np.array)->bool:
        if self.storage[pid].is_access():
            return True
        return self.storage[pid].try_repair(repair_data=repair_data)
    # 判断节点是否有损坏的文件
    def check(self)->bool:
        for packet in self.storage:
            if not packet.access():
                return False
        return True
    def get_packet(self, pid: int)->np.array:
        if self.is_miss(pid):
            return None
        return self.storage[pid].data
    # 模拟节点down
    def down(self):
        for i in range(len(self.storage)):
            self.storage[i].miss()
        self.active = False