import xml.etree.ElementTree as ET
from xml.dom import minidom

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

# def parse_data(lines):
#     layers = []
#     current_layer = {}
#     for line in lines:
#         if line.strip().startswith("Layer S7COMM"):
#             if current_layer:
#                 layers.append(current_layer)
#                 current_layer = {}
#             current_layer['Header'] = line.strip().split(":")[1].strip("(").strip(")").strip()
#         else:
#             key, value = line.split(": ")
#             current_layer[key.strip()] = value.strip()
#     if current_layer:
#         layers.append(current_layer)
#     return layers

# def parse_data(lines):
#     layers = []
#     current_layer = {}
#     for line in lines:
#         line = line.strip()  # 移除首尾空白字符
#         if not line:  # 跳过空行
#             continue
#         if line.startswith("Layer S7COMM"):
#             if current_layer:
#                 layers.append(current_layer)
#                 current_layer = {}
#             # 提取Header信息
#             header_info = line.split(":")[1].strip("()")
#             current_layer['Header'] = header_info
#         else:
#             parts = line.split(": ")
#             if len(parts) == 2:  # 确保行包含键和值
#                 key, value = parts
#                 current_layer[key.strip()] = value.strip()
#             else:
#                 # 处理没有冒号或者格式不正确的行
#                 # 可以在这里添加日志记录或者错误处理
#                 print(f"Skipping line with unexpected format: {line}")
#     if current_layer:
#         layers.append(current_layer)
#     return layers

# def parse_data(lines):
#     layers = []
#     current_layer = {}
#     for line in lines:
#         line = line.strip()  # 移除首尾空白字符
#         if not line:  # 跳过空行
#             continue
#         if line.startswith("Layer S7COMM"):
#             if current_layer:
#                 layers.append(current_layer)
#                 current_layer = {}
#             # 提取Header信息
#             parts = line.split(":")
#             if len(parts) > 1:
#                 header_info = parts[1].strip().strip("(").strip(")")
#                 current_layer['Header'] = header_info
#             else:
#                 print(f"Skipping line with unexpected format: {line}")
#         else:
#             parts = line.split(": ")
#             if len(parts) == 2:  # 确保行包含键和值
#                 key, value = parts
#                 current_layer[key.strip()] = value.strip()
#             else:
#                 # 处理没有冒号或者格式不正确的行
#                 # 可以在这里添加日志记录或者错误处理
#                 print(f"Skipping line with unexpected format: {line}")
#     if current_layer:
#         layers.append(current_layer)
#     return layers

def parse_data(lines):
    layers = []
    current_layer = {}
    for line in lines:
        line = line.strip()  # 移除首尾空白字符
        if not line:  # 跳过空行
            continue
        if line.startswith("Layer S7COMM"):
            if current_layer:
                layers.append(current_layer)
                current_layer = {}
            # 提取Header信息
            parts = line.split(":")
            if len(parts) > 1:
                header_info = parts[1].strip().strip("(").strip(")")
                current_layer['Header'] = header_info
            else:
                print(f"Skipping line with unexpected format: {line}")
        elif line.startswith("Data (S7COMM fragment id="):
            # 处理Data行
            parts = line.split(":")
            if len(parts) > 1:
                data_info = parts[1].strip()
                current_layer['Data'] = data_info
            else:
                print(f"Skipping line with unexpected format: {line}")
        else:
            parts = line.split(": ")
            if len(parts) == 2:  # 确保行包含键和值
                key, value = parts
                current_layer[key.strip()] = value.strip()
            else:
                # 处理没有冒号或者格式不正确的行
                print(f"Skipping line with unexpected format: {line}")
    if current_layer:
        layers.append(current_layer)
    return layers

def create_pit(layers):
    # 创建PIT文件的根元素
    pit = ET.Element("Peach")
    pit.set("xmlns", "http://peachfuzzer.com/Peach")
    pit.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    pit.set("xsi:schemaLocation", "http://peachfuzzer.com/Peach ../peach.xsd")
    
    # 数据模型
    data_model = ET.SubElement(pit, "DataModel")
    data_model.set("name", "S7CommDataModel")
    
    # 为每个字段添加一个条目
    for layer in layers:
        for key, value in layer.items():
            field = ET.SubElement(data_model, "Field")
            field.set("name", key)
            field.set("type", "string")
            field.set("value", value)
    
    # 状态模型
    state_model = ET.SubElement(pit, "StateModel")
    state_model.set("name", "S7CommStateModel")
    state_model.set("initialState", "Initial")
    
    state_initial = ET.SubElement(state_model, "State")
    state_initial.set("name", "Initial")
    
    action_connect = ET.SubElement(state_initial, "Action")
    action_connect.set("type", "connect")
    
    action_update_session = ET.SubElement(state_initial, "Action")
    action_update_session.set("type", "updateSession")
    payload = ET.SubElement(action_update_session, "Payload")
    data_model_ref = ET.SubElement(payload, "S7CommDataModel")
    
    action_close = ET.SubElement(state_initial, "Action")
    action_close.set("type", "close")
    
    # 测试
    test = ET.SubElement(pit, "Test")
    test.set("name", "S7CommTest")
    test_state_model = ET.SubElement(test, "StateModel")
    test_state_model.set("ref", "S7CommStateModel")
    
    publisher = ET.SubElement(test, "Publisher")
    publisher.set("class", "File")
    file_name = ET.SubElement(publisher, "Parameter")
    file_name.set("name", "FileName")
    file_name.set("value", "s7comm_output.txt")
    
    return pit

# def write_pit(pit, file_name):
#     ET.indent(pit, space='\t')  # 格式化输出
#     tree = ET.ElementTree(pit)
#     tree.write(file_name)

def write_pit(pit, file_name):
    # 将ElementTree转换为字符串
    rough_string = ET.tostring(pit, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    # 格式化输出
    pretty_xml = reparsed.toprettyxml(indent="\t")
    # 写入文件
    with open(file_name, 'w') as f:
        f.write(pretty_xml)

# 读取文件
lines = read_file("s7comm_output.txt")

# 解析数据
layers = parse_data(lines)

# 创建PIT文件
pit = create_pit(layers)

# 写入PIT文件
write_pit(pit, "s7comm_pit.xml")

print("PIT文件已生成：s7comm_pit.xml")