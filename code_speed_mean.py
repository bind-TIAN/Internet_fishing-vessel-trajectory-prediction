from icecream import ic

if __name__ == "__main__":
    cnt = 0  # 计数变量
    dict, res = {}, {}  # 初始化字典
    speed_mean = 0.0  # 初始化速度均值
    for i in range(1, 18330):
        ic(i)
        filename = 'D:/dataset1/' + str(i) + '.csv'
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                temp = line.replace('\n', '').split(',')
                if temp[6] == '围网':  # 统计捕鱼类型为围网的所有捕鱼船的速度平均值
                    key = temp[0]
                    if key not in dict:
                        dict[key] = [float(temp[3]), 1]
                    else:
                        dict[key] = [dict[key][0] + float(temp[3]), dict[key][1] + 1]
        f.close()
    for key in dict:
        res[key] = dict[key][0] / dict[key][1]
    for key in res:
        speed_mean += res[key]
    ic(speed_mean / float(len(res)))
