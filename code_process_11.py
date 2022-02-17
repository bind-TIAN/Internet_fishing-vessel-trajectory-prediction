# 求渔船id为1的在围网期间每日速度均值
from icecream import ic
import matplotlib.pyplot as plt

if __name__ == "__main__":
    list1, list2 = [], []
    dict, res = {}, {}
    cnt = 0
    for i in range(1, 18330):
        ic(i)
        filename = 'D:/dataset1/' + str(i) + '.csv'
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                temp = line.replace('\n', '').split(',')
                if temp[0] == '1':  # 渔船编号
                    list1 = temp[5].split(' ')[0].split('-')  # 对日期做进一步分割
                    list2 = temp[5].split(' ')[1].split(':')  # 对时刻做进一步分割
                    key = list1[2]  # 渔船第几天
                    if key not in dict:
                        dict[key] = [float(temp[3]), float(temp[3]), float(temp[3]), 1, 1, 1]  # 初始化字典
                    else:
                        if int(list2[0]) >= 0 and int(list2[0]) < 8:
                            dict[key] = [dict[key][0] + float(temp[3]), dict[key][1], dict[key][2], dict[key][3] + 1,
                                         dict[key][4], dict[key][5]]
                        elif int(list2[0]) >= 8 and int(list2[0]) < 16:
                            dict[key] = [dict[key][0], dict[key][1] + float(temp[3]), dict[key][2], dict[key][3],
                                         dict[key][4] + 1, dict[key][5]]
                        else:
                            dict[key] = [dict[key][0], dict[key][1], dict[key][2] + float(temp[3]), dict[key][3],
                                         dict[key][4], dict[key][5] + 1]
    f.close()
    for key in dict:
        res[key] = [dict[key][0] / dict[key][3], dict[key][1] / dict[key][4], dict[key][2] / dict[key][5]]  # 求速度均值
    ic(res)
    plt.plot([i for i in range(len(res))], [res[key][0] for key in res], color='r')
    plt.plot([i for i in range(len(res))], [res[key][1] for key in res], color='g')
    plt.plot([i for i in range(len(res))], [res[key][2] for key in res], color='b')
    plt.show()
