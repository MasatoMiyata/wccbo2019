#%%
import pandas as pd
import numpy as np
import pickle
from datetime import time
import matplotlib.pyplot as plt
import matplotlib as mpl
import json

# グラフ文字化け対策（環境に合わせてフォント名を変えてください）
mpl.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.5

# Macで4GB以上のバイナリファイルを読み込むための措置
class MacOSFile(object):

    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        # print("reading total_bytes=%s" % n, flush=True)
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                # print("done.", flush=True)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        print("writing total_bytes=%s..." % n, flush=True)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            print("writing bytes [%s, %s)... " % (idx, idx + batch_size), end="", flush=True)
            self.f.write(buffer[idx:idx + batch_size])
            print("done.", flush=True)
            idx += batch_size

def pickle_dump(obj, file_path):
    with open(file_path, "wb") as f:
        return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def pickle_load(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(MacOSFile(f))


def makeplot(df, tag, name, ylabel):

    fig = plt.figure(figsize=(10,6))
    plt.plot(df.index, df[tag])
    plt.title(name)
    plt.grid()
    plt.ylabel(ylabel)
    fig.savefig(name +'.png', dpi=300)

    return fig

#%%

# 一次エネルギー換算係数
ekw1 = 9.97  # 9.970 MJ/kWh　＜8時から22時まで＞
ekw2 = 9.28  # 9.280 MJ/kWh　＜22時から8時まで＞
ekw3 = 9.76  # 9.760 MJ/kWh　＜終日＞
egs  = 45     # 45 MJ/Nm3

# データの読み込み
df01 = pickle_load("WCCBO_BEMSdata_CSV1.binaryfile")
# df02 = pickle_load("WCCBO_BEMSdata_CSV2.binaryfile")
# df03 = pickle_load("WCCBO_BEMSdata_CSV3.binaryfile")
# df04 = pickle_load("WCCBO_BEMSdata_CSV4.binaryfile")


#%%

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
    fig = makeplot(df01, figurelist[item][0], item, figurelist[item][1])

plt.show()
