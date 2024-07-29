# 用途・目的

これらのファイルはマルチキャストに関するプログラムである．
クライアントはkisozikken_receiver.py，サーバはkisozikken_server.pyである．これらのプログラムの説明をする．
サーバはsendingFile_750kB.txtから1kBに分割し，750個のパケットを作成する．そのあと，クライアントに向けてマルチキャストをする．この動作を120回行う．

# プログラムの紹介

### kisozikken_server.py
クライアントに対し，マルチキャストでendingFile_750kB.txtから1kBに分割し，750個のパケットを送信するプログラムである．

### kisozikken_receiver.py
サーバから750個のパケットを受信するプログラムである．


## 使用言語
クライアントMicroPython言語で記述されている．
サーバはPythonで記述されている．

## 実行方法

クライアントはESP32を使い，MicroPythonのファームウェアはv1.22.2を使用している．プログラムの記述にはThonnyを用いた．

サーバはESXiに仮想環境を建て，そこにkisozikken_server.pyとsendingFile_750kB.txtを置いて実行している．仮想環境でPythonファイルを実行する時は，下記の方法からpowershell等で実行する．
```
Python3 ファイル名.py
```

## 注意点
Wi-Fi接続に必要なssidとpasswordを設定する．
マルチキャストアドレスとポートは適切なものを設定する．

## クライアントの実行結果
120回の内，1回目の部分を抜粋する．
![image](https://github.com/user-attachments/assets/d5d5def1-6107-4d60-9635-f4818c567ef7)

## サーバの実行結果
クライアントの実行結果と同様に120回の内，1回目の部分を抜粋する．
![image](https://github.com/user-attachments/assets/f58bd147-0cae-460f-91b4-9f87b6255c16)






