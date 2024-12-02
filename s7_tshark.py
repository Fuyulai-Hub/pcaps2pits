import pyshark

# 指定 TShark 的路径
pyshark.config.get_config().tshark_path = '/usr/bin/tshark'

# 读取PCAP文件
pcap_file = '../S7.pcap'  # 替换为你的PCAP文件路径
cap = pyshark.FileCapture(pcap_file, display_filter='s7comm')

# 遍历数据包并提取MQTT数据包的MQTT层信息
s7comm_packets = []
for packet in cap:
    if 's7comm' in packet:
        s7comm_packets.append(packet.s7comm)

# 输出MQTT数据包的MQTT层信息
print("S7comm解析:")
for s7comm_layer in s7comm_packets:
    print(s7comm_layer)