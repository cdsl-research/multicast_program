# 用途・目的

これらのファイルはマルチキャストに関するプログラムである．
クライアントはkisozikken_receiver.py，サーバはkisozikken_server.pyである．これらのプログラムの説明をする．
サーバはsendingFile_750kB.txtから1kBに分割し，750個のパケットを作成する．そのあと，クライアントに向けてマルチキャストをする．この動作を120回行う．

# kisozikken_server.py
クライアントに対し，マルチキャストでendingFile_750kB.txtから1kBに分割し，750個のパケットを送信するプログラムである．

# kisozikken_receiver.py
サーバから750個のパケットを受信するプログラムである．





# 使用言語
クライアントMicroPython言語で記述されている．
サーバはPythonで記述されている．

# 実行方法

クライアントはESP32を使い，MicroPythonのファームウェアはv1.22.2を使用している．

サーバはESXiに仮想環境を建て，そこにkisozikken_server.pyとsendingFile_750kB.txtを置いて実行している．


サーバは各自で建て，実行する．
実行時，Wi-Fi接続を行ってからマルチキャスト送信を行う．

# 注意点
Wi-Fi接続に必要なssidとpasswordを設定する．
マルチキャストアドレスとポートは適切なものを設定する．


