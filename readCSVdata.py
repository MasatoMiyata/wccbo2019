import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import calendar
import pickle

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


def read_bemsData(filename, YY, MM, DD):

    # CSVファイルの読み込み
    df = pd.read_csv(filepath_or_buffer=filename, sep=",", header=0)
    # 月日を足す。
    df["DateTime"] = pd.to_datetime(YY + '/' + MM + '/' + DD + ' ' + df['Time'])
    # indexの設定
    df = df.set_index("DateTime")

    return df


#----------
# 初期化（変数のサイズが 4GBを超えないように4つに分割）
df_csv1 = pd.DataFrame()
df_csv2 = pd.DataFrame()
df_csv3 = pd.DataFrame()
df_csv4 = pd.DataFrame()

for mm in range(1,13):

    # 各月の日数
    _, lastday = calendar.monthrange(2019,mm)

    for dd in range(1,lastday+1):

        print( str(mm).zfill(2) + '月' + str(dd).zfill(2) +'日 の処理を実行中')

        df1 = read_bemsData("./2019/"+str(mm)+"/"+str(dd)+"-1.csv", "2019", str(mm).zfill(2), str(dd).zfill(2))
        df2 = read_bemsData("./2019/"+str(mm)+"/"+str(dd)+"-2.csv", "2019", str(mm).zfill(2), str(dd).zfill(2))
        df3 = read_bemsData("./2019/"+str(mm)+"/"+str(dd)+"-3.csv", "2019", str(mm).zfill(2), str(dd).zfill(2))
        df4 = read_bemsData("./2019/"+str(mm)+"/"+str(dd)+"-4.csv", "2019", str(mm).zfill(2), str(dd).zfill(2))

        df_csv1 = pd.concat([df_csv1, df1])
        df_csv2 = pd.concat([df_csv2, df2])
        df_csv3 = pd.concat([df_csv3, df3])
        df_csv4 = pd.concat([df_csv4, df4])        

# バイナリファイルで保存
pickle_dump(df_csv1, 'WCCBO_BEMSdata_CSV1.binaryfile')
pickle_dump(df_csv2, 'WCCBO_BEMSdata_CSV2.binaryfile')
pickle_dump(df_csv3, 'WCCBO_BEMSdata_CSV3.binaryfile')
pickle_dump(df_csv4, 'WCCBO_BEMSdata_CSV4.binaryfile')
