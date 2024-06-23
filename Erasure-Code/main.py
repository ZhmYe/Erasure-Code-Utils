from Network import Network
from Chaos import Chaos
# 这里建立了一个n=4, k=2, sub_packetization=4也就是分4层的网络
network = Network.Network(4, 2, 4)
# 模拟上传了一个文件，这里文件会被转化为矩阵，然后被分为4个部分分别到一个"packet_sub_net"中用于纠删码
# 每层使用纠删码(目前仅支持(n, k)-RS-Code)将原数据编码为n个数据块并存于n个节点的对应packet中
is_success, origin_data = network.upload_file("testfile")
if not is_success:
    print("Upload File Failed!!!")
else:
    print("Upload File Success...")
    print("origin data: ")
    print(origin_data)
    print()
    # 展示网络出现混沌前的状态
    network.detail()
    print("")
    print("Start Inject Chaos...")
    # 这里注入混沌模拟，模拟网络出现问题，自定义
    Chaos.inject_chaos(network=network)
    print()
    # 展示网络出现混沌后的状态
    network.detail()
    # 出现混沌后尝试得到一个完整的文件
    # 这里会说明文件是否已损坏, 缺失了哪些小块，还剩下的可还原数据
    # 这里给出的是每一层的数据，比如第l层(n, k)-RS已经无法还原了，那么miss_indexes包含l
    # 由于并未实现MSR，目前的还原方式就是每一层都用RS去还原，换句话说这里的d = k, beta = alpha的MSR
    # 修复带宽为k * alpha
    is_broken, miss_indexes, remain_file_datas = network.get_file_data("testfile")
    if is_broken:
        print("File Has Miss Some Packets: ", miss_indexes)
    else:
        print("File is still Complete, data: ")
        print(remain_file_datas)