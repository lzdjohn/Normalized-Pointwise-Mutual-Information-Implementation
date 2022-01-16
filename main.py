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
