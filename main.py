import math
import pandas as pd
import csv

def to_int(str):
    try:
        int(str)
        return int(str)
    except ValueError: #报类型错误，说明不是整型的
        try:
            float(str) #用这个来验证，是不是浮点字符串
            return int(float(str))
        except ValueError:  #如果报错，说明即不是浮点，也不是int字符串。   是一个真正的字符串
            return False

def npmi_cal(px, py, pxy):
    if px and py and pxy != 0:
        Mxy = abs(math.log(pxy / (px * py)) / (-math.log(pxy)))
    else:
        Mxy = 0
    return Mxy

# 空字典用来记名字
pose_dic = {"未知姿态":0, "站":0, "立":0, '坐':0, '趴':0, '躺卧':0, '侧卧':0}
action_dic = {"未知动作":0, "持续躺":0, "持续站":0, "持续坐":0, "持续趴":0, "跑":0, "行走":0, "攀爬":0, "蹭":0, "打滚":0, "后退":0, "持续立":1}
activity_dic = {"未知活动":0, "喝水":0, "取食":0, "运动":0, "休息":0, "探究":0, "玩耍":0, "标记":0, "排遗":0, "修饰":0}
pregnant_dic = {"未知":0, "妊娠抓":0, "舔胸腹":0, "舔外阴":0, "蜷缩":0, "蹭阴":0}

# 记录csv
with open("new姿态123.csv", "r") as f:
    csv_file = csv.reader(f)
    csv_pose = list(csv_file)
with open("new动作123.csv", "r") as f:
    csv_file = csv.reader(f)
    csv_action = list(csv_file)
with open("new活动123.csv", "r") as f:
    csv_file = csv.reader(f)
    csv_activity = list(csv_file)

# 从字典获得名字
list_pose_name = list(pose_dic.keys())
list_action_name = list(action_dic.keys())
list_activity_name = list(activity_dic.keys())
# 统计px py
pose_posi = pose_dic
action_posi = action_dic
activity_posi = activity_dic
for pose, action, activity in zip(csv_pose, csv_action, csv_activity):
    # 得到数字
    pose_i = to_int(pose[6])
    action_i = to_int(action[6])
    activity_i = to_int(activity[6])
    # # 把数字转译成字符标签
    # print(action)
    # print(activity_i, pose_i, len(list_activity_name), len(list_pose_name), activity[0])
    pose_posi[list_pose_name[pose_i]] += 1
    action_posi[list_action_name[action_i]] += 1
    activity_posi[list_activity_name[activity_i]] += 1

for k, v in pose_posi.items():
    pose_posi[k] = round(pose_posi[k] / 14944, 3)
for k, v in action_posi.items():
    action_posi[k] = round(action_posi[k] / 14944, 3)
for k, v in activity_posi.items():
    activity_posi[k] = round(activity_posi[k] / 14944, 3)

# 统计pxy
# 创建pair表
# 创建3个互相关表，统计   数量/总数  总数=14944
pose_action = {}
pose_activity = {}
action_activity = {}
for q in list_pose_name:
    for k in list_action_name:
        pose_action[q+'-'+k] = 0
    for v in list_activity_name:
        pose_activity[q+'-'+v] = 0
for q in list_action_name:
    for k in list_activity_name:
        action_activity[q+'-'+k] = 0



pose_i = 0
action_i = 0
activity_i = 0
for pose, action, activity in zip(csv_pose, csv_action, csv_activity):
    # 得到数字
    pose_i = to_int(pose[6])
    action_i = to_int(action[6])
    activity_i = to_int(activity[6])
    pose_action[list_pose_name[pose_i] + "-" + list_action_name[action_i]] += 1
    pose_activity[list_pose_name[pose_i] + "-" + list_activity_name[activity_i]] += 1
    action_activity[list_action_name[action_i] + "-" + list_activity_name[activity_i]] += 1

for k, v in pose_action.items():
    pose_action[k] = round(pose_action[k] / 14944, 3)
for k, v in action_activity.items():
    action_activity[k] = round(action_activity[k] / 14944, 3)
for k, v in pose_activity.items():
    pose_activity[k] = round(pose_activity[k] / 14944, 3)

# print(pose_action, action_activity, pose_activity)
pose_action_npmi = pose_action
action_activity_npmi = action_activity
pose_activity_npmi = pose_activity
for pose in pose_posi.keys():
    for action in action_posi.keys():
        pose_action_npmi[pose + "-" + action] = npmi_cal(pose_posi[pose], action_posi[action], pose_action[pose + "-" + action])
for pose in pose_posi.keys():
    for activity in activity_posi.keys():
        pose_activity_npmi[pose + "-" + activity] = npmi_cal(pose_posi[pose], activity_posi[activity], pose_activity[pose + "-" + activity])
for action in action_posi.keys():
    for activity in activity_posi.keys():
        action_activity_npmi[action + "-" + activity] = npmi_cal(action_posi[action], activity_posi[activity], action_activity[action + "-" + activity])
print(pose_action_npmi)
print(pose_activity_npmi)
print(action_activity_npmi)




















# # 获取所有概率 pose1:xx,pose2:xx,pose3 action1，action2,action3 gesture1,gesture2,gesture3  需要构造字典，输入动作直到停止，自动统计个数。按我们的项目需求弄4个出来
# # 遍历
# # 需求————统计一个标签与同一类NPMI的最大值和不同类的NPMI的最大值
#
# import matplotlib
# import math
# import pandas
# # pose, action, activity都是字典，输入的形参都是**kwag
#
#
# class NPMI:
#     def __init__(self, pose, action, activity, pregnant):
#             self.pose_layer = pose
#             self.action_layer = action
#             self.activity_layer = activity
#             self.pregnant_layer = pregnant
#             self.record = []
#
#     def mutual_cor(self, bag):
#         tongjilist = []
#         px, py, pxy = unzip(bag)
#         Mxy = math.log(pxy/(px*py))/(-math.log(pxy))
#         tongjilist.append(Mxy)
#         tongjilist.sort()
#         return Mxy
#
#     def output(self):
#         return 0
#
#
# pose_dic = {"站", "立", '坐', '趴', '躺卧', '侧卧'}
# action_dic = {"持续躺", "持续站", "持续趴", "持续立", "跑", "行走", "攀爬", "蹭", "打滚", "后退"}
# activity_dic = {"喝水", "取食", "运动", "休息", "探究", "玩耍", "标记", "排遗", "修饰"}
# pregnant_dic = {"妊娠抓", "舔胸腹", "舔外阴", "蜷缩", "蹭阴"}
# list_of_all = [pose_dic, action_dic, activity_dic, pregnant_dic]
#
# pose_num = {"站":1,"立":2, '坐':3, '趴':1, '躺卧':1, '侧卧':1}
# action_num = {"持续躺":1, "持续站":2, "持续趴":3, "持续立":4, "跑":1, "行走":1, "攀爬":1, "蹭":1, "打滚":1, "后退":1}
# activity_num = {"喝水":1, "取食":1, "运动":1, "休息":1, "探究":1, "玩耍":1, "标记":1, "排遗":1, "修饰":1}
# pregnant_num = {"妊娠抓":1, "舔胸腹":1, "舔外阴":1, "蜷缩":1, "蹭阴":1}
#
# # 统计
# for dic in list_of_all:
#     for k,v in dic.items():
#         dic[k] =
#
#
# # 计算
# for k,v in dic.items():
#
# pose_pos = pose_dic
# action_pos = action_dic
# activity_pos = activity_dic
# pregnant_pos = pregnant_dic
#
#
# # 转化成 名字+个数（个数需要统计）
# # 转化成 名字+概率
# # 代公式 每个x，对不同层的y计算，然后得出最大的NPMI
# # 存数据 把每个label对应的NPMI存入字典中
# markdic1 = {'站': 1,
#             '立': 2,
#             '坐': 3,
#             '趴': 4,
#             '躺卧': 5,
#             '侧卧': 6
#             }
# markdic2 = {'持续躺': 1,
#             '持续站': 2,
#             '持续坐': 3,
#             '持续趴': 4,
#             '跑': 5,
#             '行走': 6,
#             '攀爬': 7,
#             '蹭': 8,
#             '打滚': 9,
#             '后退': 10,
#             '持续立': 11,
#             }
# markdic3 = {'喝水': 1,
#             '取食': 2,
#             '运动': 3,
#             '休息': 4,
#             '探究': 5,
#             '玩耍': 6,
#             '标记': 7,
#             '排遗': 8,
#             '修饰': 9,
#             }
# markdic4 = {'妊娠抓': 1,
#             '舔胸腹': 2,
#             '舔外阴': 3,
#             '蜷缩': 4,
#             '蹭阴': 5,
#             }
#
# cpdd = NPMI(pose_dic, action_dic, activity_dic, pregnant_dic)
# cpdd.mutual_cor()
# cpdd.output()
#
#
# # if __name__ == "__main__":
# #     main()
#

# for i in range(len(list_of_num)):
#     dic = list_of_num[i]
#     posi = list_of_posi[i]
#     all = 0
#     for value in dic.values():
#         all += value
#     for k,v in posi.items():
#         posi[k]
#         dic[k]
#     possibility_list = [value in dic.values()]
#     print(possibility_list)


# for i in range(len(action_num)):
#     Mxy = math.log(pxy / (px * py)) / (-math.log(pxy))
#  tangbinbin sunjincheng