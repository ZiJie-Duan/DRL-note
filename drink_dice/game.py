import numpy as np

from pprint import pprint
from collections import Counter


class DrinkDice:

    def __init__(self, people_num, dice_num) -> None:
        self.people_num = people_num
        self.dice_num = dice_num

    def play(self):
        results = np.random.randint(1, 7, (self.people_num, self.dice_num))
        return results


class DrinkAnalyzer:

    def __init__(self, game) -> None:
        self.game = game

    def cal_exp_sdv(self, sim_num=10000):
        result = [0] * 6
        acc_res = [[] for _ in range(6)]
        sdv = [0] * 6

        for _ in range(sim_num):
            res = self.game.play().flatten()
            counts = Counter(res)
            counts = [int(v) for k, v in counts.items()]
            counts.sort(reverse=True)

            if len(counts) < 6: # 6 surface dice
                counts += [0] * (6-len(counts))
            
            for i in range(6):
                result[i] += counts[i]
                acc_res[i].append(counts[i])

        for i in range(6):
            mean = sum(acc_res[i]) / sim_num
            result[i] = result[i] / sim_num
            sdv[i] = float(np.sqrt(sum([(c - mean)**2 for c in acc_res[i]])/sim_num))

        return result, sdv
    
    def zero_cal_exp_sdv(self, sim_num=10000):
        result = [0] * 6
        acc_res = [[] for _ in range(6)]
        sdv = [0] * 6

        for _ in range(sim_num):
            res = self.game.play().flatten() 
            one_count = np.sum(res == 1)  # 计算结果中有多少个1
            res = res[res != 1]  # 移除所有的零
            counts = Counter(res)
            counts = [int(v) + int(one_count) for k, v in counts.items()]
            counts.append(float(one_count))
            counts.sort(reverse=True)
            
            if len(counts) < 6: # 6 surface dicr
                counts += [0] * (6-len(counts))
            
            for i in range(6):
                result[i] += counts[i]
                acc_res[i].append(counts[i])

        for i in range(6):
            mean = sum(acc_res[i]) / sim_num
            result[i] = result[i] / sim_num
            sdv[i] = float(np.sqrt(sum([(c - mean)**2 for c in acc_res[i]])/sim_num))

        return result, sdv
    

dd = DrinkDice(6,5)
da = DrinkAnalyzer(dd)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 输入数据
positions, stds = da.zero_cal_exp_sdv(10000)

# 生成x轴范围
max_range = max(positions) + 3 * max(stds)
min_range = min(positions) - 3 * max(stds)
x = np.linspace(min_range, max_range, 1000)

plt.figure(figsize=(10, 6))

# 为每个位置绘制正态分布曲线
colors = plt.cm.viridis(np.linspace(0, 1, len(positions)))  # 使用渐变色
pdfs = []  # 用于存储所有正态分布的概率密度函数

for mu, sigma, color in zip(positions, stds, colors):
    label = f'μ={mu:.2f}, σ={sigma:.2f}'
    pdf = norm.pdf(x, mu, sigma)
    pdfs.append(pdf)
    plt.plot(x, pdf, color=color, label=label, alpha=0.7)

# 计算重叠区域
overlap = np.zeros_like(x)  # 用于存储重叠区域的透明度
for i in range(len(pdfs)):
    for j in range(i+1, len(pdfs)):
        # 计算每对曲线的重叠部分
        overlap += np.minimum(pdfs[i], pdfs[j])  # 取每对曲线的最小值来表示重叠

# 计算重叠区域的积分 (即重叠的面积)
overlap_area = np.trapezoid(overlap, x)

# 归一化重叠区域，使其积分为1
overlap_normalized = overlap / overlap_area

# 填充重叠区域
plt.fill_between(x, overlap_normalized, color='gray', alpha=0.3, label='Overlapping Area')

plt.title('Normal Distributions with Normalized Overlap Highlighted')
plt.xlabel('Position')
plt.ylabel('Probability Density')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # 将图例放在图表外右侧
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('my_plot_with_normalized_overlap.png')