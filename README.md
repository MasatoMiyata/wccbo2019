# wccbo2019 グラフ化支援ツール

What is WCCBO?  →　http://www.wccbo.org/

このプログラムは、wccbo2019用のエミュレータが出力した年間運転データ（BEMSデータ）をグラフ化するためのものです。

エミュレータを実行し、1年間分のデータが保存されてから、このプログラムを実行してください。  
1年間分揃っていない場合、エラーが出ます。

* 1年分のサンプルデータは以下でダウンロードできます。  
  http://www.wccbo.org/bems.zip

プログラムは２つに分かれています。  

[1] readCSVdata.py  

　エミュレータが出力したCSVファイルを読み込み、binary fileを生成するプログラムです。  
　binary fileを生成には時間がかかりますが、  
　一回生成しておけば、その後のグラフ化は効率良く実行することができます。  

 * 変数 directory に BEMSデータを保存したディレクトリを記してください。  
 * 変数 timedelta の値を変えることにより、抽出する時間間隔を変えることができます。  
   オリジナルデータは1分ですが、1分間隔のままbinary化するには3時間程度かかります。  
   10分間隔で抽出すると、15分程度でbinary化が完了します。  
 * macでは4GB以上のbinary fileが生成できない不具合があるため、mac用に「picklefileRW.py」を作成し読み込ませています。
   　→　このままのプログラムで　Windows 10 （python 3.7） でも正常に処理ができることを確認（2019/6/8追記）  
  
[2] makeFigures.py  

　binary fileを読み込んで、グラフ化をするプログラムです。  
　graphList.json にグラフ化をしたい項目に関する情報を追記し、  
　プログラムを実行すれば、グラフが保存されます。  
  
　graphList.json の構成は以下の通りとなっています。  
  
　 <保存する際のグラフの名称> :[  
    　　<CSVファイルの番号（csv1, csv2, csv3, csv4）>,  
    　　<CSVデータのカラム名>,  
    　　<グラフのy軸に表示される項目名>  
    ],  

