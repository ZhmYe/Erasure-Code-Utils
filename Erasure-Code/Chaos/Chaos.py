from Network.Network import Network
# 这里模拟网络出现状况
def inject_chaos(network:Network):
    # todo
    # 这里模拟网路中的前m个节点直接down
    m = network.m
    for i in range(m):
        network.nodes[i].down()