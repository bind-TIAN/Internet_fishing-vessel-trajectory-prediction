from icecream import ic
from pandas.core.frame import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from collections import Counter
import csv

if __name__ == "__main__":
    cnt = 0  # 计数变量打印统计的条目数
    list_lat, list_lon, speed, rotation, type_value = [], [], [], [], []  # 五个列表分别存储纬度，经度，速度，方向和捕鱼船类型
    dict = {}  # 用于生成pandas数据类型的暂存字典
    for i in range(1, 18330):  # 遍历训练集数据
        ic(i)  # 打印遍历的数据条目数
        filename = 'D:/dataset1/' + str(i) + '.csv'  # 读文件
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                temp = line.replace('\n', '').split(',')
                if temp[6] == 'type':  # 去除文件中的第一条信息（该信息是坏数据因此需要去除）
                    continue
                list_lat.append(float(temp[1]))  # 存放纬度
                list_lon.append(float(temp[2]))  # 存放经度
                speed.append(float(temp[3]))  # 存放速度
                rotation.append(float(temp[4]))  # 存放方向信息
                if temp[6] == '围网':  # 对捕鱼船的不同类型分别设置参数，其中0表示围网，1表示拖网，2表示刺网
                    type_value.append(0)
                if temp[6] == '拖网':
                    type_value.append(1)
                if temp[6] == '刺网':
                    type_value.append(2)
        f.close()
    dict = {"lat": list_lat, "lon": list_lon, "speed": speed, "rotation": rotation, "type": type_value}  # 将列表元素放入字典中
    data = DataFrame(dict)  # 把字典类型转成pandas类型
    data_boss = data[['lat', 'lon', 'speed', 'rotation', 'type']]  # data_boss存储选出想用的信息（以字典键值作为遴选依据）
    train_data, test_data = train_test_split(data_boss, test_size=0.3, random_state=101)  # 采用函数分割数据集为训练集、测试集
    train_x = train_data[['lat', 'lon', 'speed', 'rotation']]  # 选出训练集
    train_y = train_data.type  # 选出训练集标签
    model = DecisionTreeClassifier()  # 采用决策树模型
    model.fit(train_x, train_y)  # 模型预训练
    # 经过以上各步骤，可以得到一个训练模型
    count = 0  # 计数变量
    dict2, result, memory_value, save_dict = {}, {}, {}, {}  # 初始化字典
    for i in range(18330, 22364):  # 遍历测试数据
        count += 1
        ic(count)
        filename = 'D:/test_dataset/' + str(i) + '.csv'
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                temp = line.replace('\n', '').split(',')
                if temp[1] == 'lat' and temp[2] == 'lon':
                    continue
                key = temp[0]  # 以渔船id作为字典键值
                if key not in dict2:
                    dict2[key] = [[float(temp[1])], [float(temp[2])], [float(temp[3])],
                                  [float(temp[4])]]  # 向dict2字典中填入4个数组，分别表示纬度、经度、速度和方向
                else:
                    result[key] = [dict2[key][0].append(float(temp[1])), dict2[key][1].append(float(temp[2])),
                                   dict2[key][2].append(float(temp[3])),
                                   dict2[key][3].append(float(temp[4]))]  # 将上述4个信息根据id填入到对应字典键值中
        f.close()
    for key in dict2:  # 遍历上述填入的字典键值，以便针对每个渔船id，预测该渔船的类型
        memory_value = {'lat': dict2[key][0], 'lon': dict2[key][1], 'speed': dict2[key][2],
                        'rotation': dict2[key][3]}  # memory_value暂存字典
        data = DataFrame(memory_value)  # 将memory_value这个字典转成pandas数据结构
        test_data2 = data[['lat', 'lon', 'speed', 'rotation']]  # 遴选出想要的数据放到test_data2中作为测试集
        prediction = model.predict(test_data2)  # 采用上述训练好的模型去预测新的测试数据
        res = Counter(prediction)  # 由于prediction返回的是一个列表，采用counter统计列表中元素出现的次数，返回一个字典类型
        list_result = sorted(res.items(), key=lambda x: x[1], reverse=True)  # 对字典中的元素按照键值对应的value值的大小降序排序
        save_dict[key] = list_result[0][0]  # 将键值对对应的value值保存在一个新的字典中
    # 生成csv文件
    filename = "C:/Users/tbdhd/Desktop/submission.csv"  # 告知将要写入文件的目录位置
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csv_file:  # 以UTF-8格式写入文件
        writer = csv.writer(csv_file)
        writer.writerow(['渔船ID', 'type'])
        for key in save_dict:  # 遍历字典，将字典键值对应位置转成汉字写入到csv中，其中0表示围网，1表示拖网，2表示刺网
            if save_dict[key] == 0:
                writer.writerow([key, '围网'])
            if save_dict[key] == 1:
                writer.writerow([key, '拖网'])
            if save_dict[key] == 2:
                writer.writerow([key, '刺网'])
        csv_file.close()
