#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import json
import picklefileRW as pk
from datetime import time

# グラフ文字化け対策（環境に合わせてフォント名を変えてください）
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5


def makeplot(df, tag, name, ylabel):

    fig = plt.figure(figsize=(10,6))
    plt.plot(df.index, df[tag])
    plt.title(name)
    plt.grid()
    plt.ylabel(ylabel)
    fig.savefig(name +'.png', dpi=300)

    return fig

#%%

# バイナリファイルの読み込み
df01 = pk.pickle_load("WCCBO_BEMSdata_CSV1.binaryfile")
df02 = pk.pickle_load("WCCBO_BEMSdata_CSV2.binaryfile")
df03 = pk.pickle_load("WCCBO_BEMSdata_CSV3.binaryfile")
df04 = pk.pickle_load("WCCBO_BEMSdata_CSV4.binaryfile")


#%%

# 一次エネルギー換算係数
ekw1 = 9.97  # 9.970 MJ/kWh　＜8時から22時まで＞
ekw2 = 9.28  # 9.280 MJ/kWh　＜22時から8時まで＞
ekw3 = 9.76  # 9.760 MJ/kWh　＜終日＞
egs  = 45     # 45 MJ/Nm3

# 各設備のエネルギー消費量
E_ref   = df01['Electricity of heat source system [kW]']
E_ahu   = df01['Electricity of air conditioning system [kW]']
E_plg   = df01['Electricity of Tenant Plug [kW]']
E_light = df01['Electricity of Tenant Lighting [kW]']
E_gas   = df01['Absorption Chiller Gas Consumption [m3/h]']

# 全体の一次エネルギー消費量 [GJ/min]（ただし、一次エネルギー換算係数は終日の値。また、本当は水のエネルギーも足す必要がある。）
df01['Primary Energy Use [GJ/min]'] = ( (E_ref + E_ahu + E_plg + E_light) / 60 * ekw3  + E_gas * egs /60 ) /1000


#%% 

# グラフリスト（json）の読み込み
with open('graphList.json', encoding='utf-8') as f:
    figurelist = json.load(f)

# グラフを生成
for item in figurelist:

    if figurelist[item][0] == "csv1":
        fig = makeplot(df01, figurelist[item][1], item, figurelist[item][2])
    elif figurelist[item][0] == "csv2":
        fig = makeplot(df02, figurelist[item][1], item, figurelist[item][2])
    elif figurelist[item][0] == "csv3":
        fig = makeplot(df03, figurelist[item][1], item, figurelist[item][2])
    elif figurelist[item][0] == "csv4":
        fig = makeplot(df04, figurelist[item][1], item, figurelist[item][2])

plt.show()
