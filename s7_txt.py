import pyshark
import re

# 指定 TShark 的路径
pyshark.config.get_config().tshark_path = '/usr/bin/tshark'

# 读取PCAP文件
pcap_file = '../S7.pcap'  # 替换为你的PCAP文件路径
cap = pyshark.FileCapture(pcap_file, display_filter='s7comm')

# 定义一个函数来移除ANSI转义序列
def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# 遍历数据包并提取MQTT数据包的MQTT层信息
s7comm_packets = []
for packet in cap:
    if 's7comm' in packet:
        s7comm_packets.append(packet.s7comm)

# 输出MQTT数据包的MQTT层信息，并保存到txt文件
output_file = 's7comm_output.txt'
with open(output_file, 'w') as file:
    file.write("s7comm解析:\n")
    for s7comm_layer in s7comm_packets:
        cleaned_s7comm_info = remove_ansi_escape_codes(str(s7comm_layer))
        file.write(cleaned_s7comm_info + '\n')

print(f"s7comm解析结果已保存到 {output_file}")