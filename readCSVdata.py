import time
from multiprocessing import Pool
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import calendar
import picklefileRW as pk

### parameters ###
directory = "./2019/"  # データがあるディレクトリ
timedelta = "10T"       # 抽出する時間間隔（5分なら"5T"、1時間なら"H"）


def read_bemsData(filename, YY, MM, DD):

    # CSVファイルの読み込み
    df = pd.read_csv(filepath_or_buffer=filename, sep=",", header=0)
    # 月日を足す。
    df["DateTime"] = pd.to_datetime(YY + '/' + MM + '/' + DD + ' ' + df['Time'])
    # indexの設定
    df = df.set_index("DateTime")

    return df


def main():

	# 初期化
	df_csv1 = pd.DataFrame()
	df_csv2 = pd.DataFrame()
	df_csv3 = pd.DataFrame()
	df_csv4 = pd.DataFrame()

	for mm in range(1,13):

		# 各月の日数
		_, lastday = calendar.monthrange(2019,mm)

		for dd in range(1,lastday+1):

			YY = "2019"
			MM = str(mm).zfill(2)  # 月（01、02、・・・）
			DD = str(dd).zfill(2)  # 日（01、02、・・・）

			print( MM + '月' + DD +'日 の処理を実行中')

			df1 = read_bemsData(directory + str(mm) + "/" + str(dd) + "-1.csv", YY, MM, DD)
			df_csv1 = pd.concat([df_csv1, df1.asfreq(freq=timedelta)])

			df2 = read_bemsData(directory + str(mm) + "/" + str(dd) + "-2.csv", YY, MM, DD)
			df_csv2 = pd.concat([df_csv2, df2.asfreq(freq=timedelta)])

			df3 = read_bemsData(directory + str(mm) + "/" + str(dd) + "-3.csv", YY, MM, DD)
			df_csv3 = pd.concat([df_csv3, df3.asfreq(freq=timedelta)])

			df4 = read_bemsData(directory + str(mm) + "/" + str(dd) + "-4.csv", YY, MM, DD)
			df_csv4 = pd.concat([df_csv4, df4.asfreq(freq=timedelta)])        


	# バイナリファイルで保存
	pk.pickle_dump(df_csv1, 'WCCBO_BEMSdata_CSV1.binaryfile')
	pk.pickle_dump(df_csv2, 'WCCBO_BEMSdata_CSV2.binaryfile')
	pk.pickle_dump(df_csv3, 'WCCBO_BEMSdata_CSV3.binaryfile')
	pk.pickle_dump(df_csv4, 'WCCBO_BEMSdata_CSV4.binaryfile')


if __name__ == '__main__':

	ts = time.time()   # 計算開始時刻の記録

	main()

	te = time.time()   # 計算終了時刻の記録
	print("実行時間は " + str(te-ts) + " 秒です")
